import grpc
import threading

try:
    # Python 2
    from Queue import Queue
except ImportError:
    # Python 3
    from queue import Queue

class StreamingRequestThread(threading.Thread):
    """A thread to run a streaming gRPC request on.

    Streaming gRPC requests block when next() is called on their iterator, making it difficult to
    cancel the call, or to poll in between doing other work. This helper pumps the call's response
    queue on a separate thread, and provides a convenience method (stop()) to cancel the call.

    This should either be used in a ``with`` statement, or start() and stop() should be used to
    start and stop the thread.

    Args:
        name: An optional name for the thread.
        request: The request method. This is normally a bound method on a gRPC service stub (either
            gRPC's native stub or the service wrapper). It will be called when the thread starts.
        args: A tuple of arguments to call ``request`` with.
        kwargs: A dictionary of keyword arguments to call ``request`` with.
        call: An in-flight RPC. This can be provided instead of request and args.

    Attributes:
        queue (Queue.Queue): A queue that responses will be placed onto. If the call fails, a
            grpc.RpcError instance will be placed on the queue. If the call ends normally (with an
            OK response), None will be placed on the queue to signal this.
    """

    def __init__(self, request=None, args=None, kwargs=None, call=None, name=None):
        super(StreamingRequestThread, self).__init__(name=name)

        self.queue = Queue()
        self._call = call
        if call is None:
            if request is None:
                raise ValueError("Either request or call must be provided")
            self._request = request
            self._args = args if args is not None else ()
            self._kwargs = kwargs if kwargs is not None else {}

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *exc):
        self.stop()
        self.join()
        return False

    def run(self):
        """Overload from threading.Thread. Do not call directly - use start() instead."""
        try:
            if self._call is None:
                self._call = self._request(*self._args, **self._kwargs)
            for msg in self._call:
                self.queue.put(msg)
            self.queue.put(None) # end signal
        except grpc.RpcError as e:
            self.queue.put(e)

    def stop(self):
        """Cancel the call.

        This will cause the thread to end (join() can be used to wait for this).

        Note that this thread may block program exit if you do not either call this or set the
        thread's ``daemon`` attribute to True.
        """
        if self._call:
            self._call.cancel()

    def get(self, *args, **kwargs):
        """Convenience wrapper around queue.get().

        This calls queue.get() with the provided arguments, and re-raises any RpcErrors that were
        queued.
        """
        item = self.queue.get(*args, **kwargs)
        if isinstance(item, grpc.RpcError):
            raise item
        return item

class StatusWatcher(object):
    """
    Convenience wrapper for monitoring acquisition status.

    To use this class, simply call watcher.wait() as if looping through a generator, then
    after you are done with the watcher, call watcher.stop() (within the loop still) and then
    wait for the generator to close and it will exit the loop.

    If you break out of the loop then the cpp side may use some extra resources as it will not
    be immediately notified that the stream has been cancelled

    >>> watcher = StatusWatcher(rpc_connection)
    >>> msgs = minLights.rpc.acquisition_service
    >>> for status in status_watcher.wait():
    >>>     if status.status == msgs.PROCESSING:
    >>>         connection.acquisition.stop(data_action_on_stop=msgs.StopRequest.STOP_KEEP_ALL_DATA, wait_until_ready=True)
    >>>     elif status.status == msgs.READY:
    >>>         watcher.stop()

    """

    def __init__(self, connection):
        self.connection = connection
        self.is_stopped = False
        self.cv = threading.Condition()

    def wait(self):
        self.iterable = self.connection.acquisition.watch_for_status_change(self._wait_for_stop())
        return self.iterable

    def stop(self):
        self.cv.acquire()
        self.is_stopped = True
        self.cv.notify()
        self.cv.release()
        self.iterable.cancel()

    def _wait_for_stop(self):
        self.cv.acquire()
        while not self.is_stopped:
            self.cv.wait()
        self.cv.release()
        req = self.connection.acquisition._pb.WatchForStatusChangeRequest()
        req.stop = True
        yield req
