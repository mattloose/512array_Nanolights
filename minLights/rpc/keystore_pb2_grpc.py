# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from minLights.rpc import keystore_pb2 as minknow_dot_rpc_dot_keystore__pb2


class KeyStoreServiceStub(object):
  """Allows arbitrary data to be associated with this MinKNOW instance.

  This can be used by the protocol to communicate information to the outside world (including a
  user interface), for example.

  Value names should be stored in the form <product>:<name>, where <product> is the name of the
  product that has decided what form the value should take (generally either the software that is
  setting the value, or the software that is consuming it).

  In particular, the prefixes "minknow:", "bream:", "protocol:" and "gui:" are reserved for MinKNOW
  and the software that ships with MinKNOW. Names starting with ":" are also reserved for
  "well-known" values that will be listed in this or related documentation.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.store = channel.unary_unary(
        '/ont.rpc.keystore.KeyStoreService/store',
        request_serializer=minknow_dot_rpc_dot_keystore__pb2.StoreRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_keystore__pb2.StoreResponse.FromString,
        )
    self.remove = channel.unary_unary(
        '/ont.rpc.keystore.KeyStoreService/remove',
        request_serializer=minknow_dot_rpc_dot_keystore__pb2.RemoveRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_keystore__pb2.RemoveResponse.FromString,
        )
    self.get_one = channel.unary_unary(
        '/ont.rpc.keystore.KeyStoreService/get_one',
        request_serializer=minknow_dot_rpc_dot_keystore__pb2.GetOneRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_keystore__pb2.GetOneResponse.FromString,
        )
    self.get = channel.unary_unary(
        '/ont.rpc.keystore.KeyStoreService/get',
        request_serializer=minknow_dot_rpc_dot_keystore__pb2.GetRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_keystore__pb2.GetResponse.FromString,
        )
    self.watch = channel.unary_stream(
        '/ont.rpc.keystore.KeyStoreService/watch',
        request_serializer=minknow_dot_rpc_dot_keystore__pb2.WatchRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_keystore__pb2.WatchResponse.FromString,
        )


class KeyStoreServiceServicer(object):
  """Allows arbitrary data to be associated with this MinKNOW instance.

  This can be used by the protocol to communicate information to the outside world (including a
  user interface), for example.

  Value names should be stored in the form <product>:<name>, where <product> is the name of the
  product that has decided what form the value should take (generally either the software that is
  setting the value, or the software that is consuming it).

  In particular, the prefixes "minknow:", "bream:", "protocol:" and "gui:" are reserved for MinKNOW
  and the software that ships with MinKNOW. Names starting with ":" are also reserved for
  "well-known" values that will be listed in this or related documentation.
  """

  def store(self, request, context):
    """Store one or more values.

    Anyone watching those values will be notified of the change. If they are watching several of
    the values in a single watch() call, all the updates will be sent in a single message.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def remove(self, request, context):
    """Remove a value from the store.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def get_one(self, request, context):
    """Get a single value.

    This is a convenient alternative to get() when you only want a single value. If you want
    multiple values, it is more efficient to request them all in a single get() call.

    If the requested value is not in the store, this will return an error.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def get(self, request, context):
    """Get any number of values.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def watch(self, request, context):
    """Watch for values being updates.

    On calling this, you will get a message containing the current values, and then messages with
    updates as and when store() is called. The updates will only contain those values that
    changed.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_KeyStoreServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'store': grpc.unary_unary_rpc_method_handler(
          servicer.store,
          request_deserializer=minknow_dot_rpc_dot_keystore__pb2.StoreRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_keystore__pb2.StoreResponse.SerializeToString,
      ),
      'remove': grpc.unary_unary_rpc_method_handler(
          servicer.remove,
          request_deserializer=minknow_dot_rpc_dot_keystore__pb2.RemoveRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_keystore__pb2.RemoveResponse.SerializeToString,
      ),
      'get_one': grpc.unary_unary_rpc_method_handler(
          servicer.get_one,
          request_deserializer=minknow_dot_rpc_dot_keystore__pb2.GetOneRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_keystore__pb2.GetOneResponse.SerializeToString,
      ),
      'get': grpc.unary_unary_rpc_method_handler(
          servicer.get,
          request_deserializer=minknow_dot_rpc_dot_keystore__pb2.GetRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_keystore__pb2.GetResponse.SerializeToString,
      ),
      'watch': grpc.unary_stream_rpc_method_handler(
          servicer.watch,
          request_deserializer=minknow_dot_rpc_dot_keystore__pb2.WatchRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_keystore__pb2.WatchResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ont.rpc.keystore.KeyStoreService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))