# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from minLights.rpc import basecaller_pb2 as minknow_dot_rpc_dot_basecaller__pb2


class BasecallerStub(object):
  """Basecall reads files from previous sequencing runs.

  NB: this is not available from a MinKNOW device instance. It should be accessed on its own
  connection, using one of the ports provided by the
  minLights.rpc.manager.ManagerService.basecaller_api() method.

  Since 3.5
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.list_configs_by_kit = channel.unary_unary(
        '/ont.rpc.basecaller.Basecaller/list_configs_by_kit',
        request_serializer=minknow_dot_rpc_dot_basecaller__pb2.ListConfigsByKitRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_basecaller__pb2.ListConfigsByKitResponse.FromString,
        )
    self.start = channel.unary_unary(
        '/ont.rpc.basecaller.Basecaller/start',
        request_serializer=minknow_dot_rpc_dot_basecaller__pb2.StartRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_basecaller__pb2.StartResponse.FromString,
        )
    self.cancel = channel.unary_unary(
        '/ont.rpc.basecaller.Basecaller/cancel',
        request_serializer=minknow_dot_rpc_dot_basecaller__pb2.CancelRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_basecaller__pb2.CancelResponse.FromString,
        )
    self.get_info = channel.unary_stream(
        '/ont.rpc.basecaller.Basecaller/get_info',
        request_serializer=minknow_dot_rpc_dot_basecaller__pb2.GetInfoRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_basecaller__pb2.GetInfoResponse.FromString,
        )
    self.watch = channel.unary_stream(
        '/ont.rpc.basecaller.Basecaller/watch',
        request_serializer=minknow_dot_rpc_dot_basecaller__pb2.WatchRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_basecaller__pb2.WatchResponse.FromString,
        )


class BasecallerServicer(object):
  """Basecall reads files from previous sequencing runs.

  NB: this is not available from a MinKNOW device instance. It should be accessed on its own
  connection, using one of the ports provided by the
  minLights.rpc.manager.ManagerService.basecaller_api() method.

  Since 3.5
  """

  def list_configs_by_kit(self, request, context):
    """List the available basecalling configurations sorted by flow cell and kit.

    Since 3.5
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def start(self, request, context):
    """Start basecalling reads files.

    Since 3.5
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def cancel(self, request, context):
    """Stop a basecalling that was started by start_basecalling_reads().

    Since 3.5
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def get_info(self, request, context):
    """Gets information about one or more basecalling operations.

    Since 3.5
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def watch(self, request, context):
    """Monitors basecalls, returning messages when basecalls are started, stopped or receive
    progress updates.

    The current state of all currently-running basecalls will be returned in the initial set of
    messages. Optionally, the state of all already-finished runs can be included. Note that this
    initial state may be split among several responses.

    Note that progress updates may be rate limited to avoid affecting performance.

    Since 3.5
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_BasecallerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'list_configs_by_kit': grpc.unary_unary_rpc_method_handler(
          servicer.list_configs_by_kit,
          request_deserializer=minknow_dot_rpc_dot_basecaller__pb2.ListConfigsByKitRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_basecaller__pb2.ListConfigsByKitResponse.SerializeToString,
      ),
      'start': grpc.unary_unary_rpc_method_handler(
          servicer.start,
          request_deserializer=minknow_dot_rpc_dot_basecaller__pb2.StartRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_basecaller__pb2.StartResponse.SerializeToString,
      ),
      'cancel': grpc.unary_unary_rpc_method_handler(
          servicer.cancel,
          request_deserializer=minknow_dot_rpc_dot_basecaller__pb2.CancelRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_basecaller__pb2.CancelResponse.SerializeToString,
      ),
      'get_info': grpc.unary_stream_rpc_method_handler(
          servicer.get_info,
          request_deserializer=minknow_dot_rpc_dot_basecaller__pb2.GetInfoRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_basecaller__pb2.GetInfoResponse.SerializeToString,
      ),
      'watch': grpc.unary_stream_rpc_method_handler(
          servicer.watch,
          request_deserializer=minknow_dot_rpc_dot_basecaller__pb2.WatchRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_basecaller__pb2.WatchResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ont.rpc.basecaller.Basecaller', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))