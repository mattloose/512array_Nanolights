# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from minLights.rpc import log_pb2 as minknow_dot_rpc_dot_log__pb2


class LogServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.get_user_messages = channel.unary_stream(
        '/ont.rpc.log.LogService/get_user_messages',
        request_serializer=minknow_dot_rpc_dot_log__pb2.GetUserMessagesRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_log__pb2.UserMessage.FromString,
        )
    self.send_user_message = channel.unary_unary(
        '/ont.rpc.log.LogService/send_user_message',
        request_serializer=minknow_dot_rpc_dot_log__pb2.SendUserMessageRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_log__pb2.SendUserMessageResponse.FromString,
        )
    self.send_ping = channel.unary_unary(
        '/ont.rpc.log.LogService/send_ping',
        request_serializer=minknow_dot_rpc_dot_log__pb2.SendPingRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_log__pb2.SendPingResponse.FromString,
        )


class LogServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def get_user_messages(self, request, context):
    """Get a stream of user messages, updated with new messages as the are emitted in minknow.

    Since 1.11
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def send_user_message(self, request, context):
    """Send a log message to any listeners of messages (see get_user_messages)

    Any historical user messages are first sent to the caller,

    Since 1.11
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def send_ping(self, request, context):
    """Send a ping to the configured ping server (see system config for ping server url)

    The tracking_id and context_data section of the ping are filled in automatically by MinKNOW.

    The ping is queued internally for sending immediately, if MinKNOW fails to send the message it
    stores the message to send when possible.

    Since 1.11
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_LogServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'get_user_messages': grpc.unary_stream_rpc_method_handler(
          servicer.get_user_messages,
          request_deserializer=minknow_dot_rpc_dot_log__pb2.GetUserMessagesRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_log__pb2.UserMessage.SerializeToString,
      ),
      'send_user_message': grpc.unary_unary_rpc_method_handler(
          servicer.send_user_message,
          request_deserializer=minknow_dot_rpc_dot_log__pb2.SendUserMessageRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_log__pb2.SendUserMessageResponse.SerializeToString,
      ),
      'send_ping': grpc.unary_unary_rpc_method_handler(
          servicer.send_ping,
          request_deserializer=minknow_dot_rpc_dot_log__pb2.SendPingRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_log__pb2.SendPingResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ont.rpc.log.LogService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))