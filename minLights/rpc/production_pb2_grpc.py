# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from minLights.rpc import production_pb2 as minknow_dot_rpc_dot_production__pb2


class ProductionServiceStub(object):
  """Methods used in production.

  These might modify the device or flowcell permanently. They are not available
  in non-production contexts.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.write_flowcell_data = channel.unary_unary(
        '/ont.rpc.production.ProductionService/write_flowcell_data',
        request_serializer=minknow_dot_rpc_dot_production__pb2.WriteFlowcellDataRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_production__pb2.WriteFlowcellDataResponse.FromString,
        )
    self.write_flowcell_id = channel.unary_unary(
        '/ont.rpc.production.ProductionService/write_flowcell_id',
        request_serializer=minknow_dot_rpc_dot_production__pb2.WriteFlowcellIdRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_production__pb2.WriteFlowcellIdResponse.FromString,
        )
    self.write_wells_per_channel = channel.unary_unary(
        '/ont.rpc.production.ProductionService/write_wells_per_channel',
        request_serializer=minknow_dot_rpc_dot_production__pb2.WriteWellsPerChannelRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_production__pb2.WriteWellsPerChannelResponse.FromString,
        )
    self.write_product_code = channel.unary_unary(
        '/ont.rpc.production.ProductionService/write_product_code',
        request_serializer=minknow_dot_rpc_dot_production__pb2.WriteProductCodeRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_production__pb2.WriteProductCodeResponse.FromString,
        )
    self.write_temperature_offset = channel.unary_unary(
        '/ont.rpc.production.ProductionService/write_temperature_offset',
        request_serializer=minknow_dot_rpc_dot_production__pb2.WriteTemperatureOffsetRequest.SerializeToString,
        response_deserializer=minknow_dot_rpc_dot_production__pb2.WriteTemperatureOffsetResponse.FromString,
        )


class ProductionServiceServicer(object):
  """Methods used in production.

  These might modify the device or flowcell permanently. They are not available
  in non-production contexts.
  """

  def write_flowcell_data(self, request, context):
    """Writes data to the EEPROM on the attached flowcell.

    This call will fail with FAILED_PRECONDITION if there is no device connected or no flowcell
    attached.

    Very little checking of the provided values is done, and no attempt is made to preserve
    existing data. Use the other methods on this service for that.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def write_flowcell_id(self, request, context):
    """Write the flowcell ID to the flowcell EEPROM.

    Flowcell IDs over 8 characters or containing unprintable characters will be rejected with
    INVALID_ARGUMENT. An empty string effectively clears the flowcell ID.

    If nothing is currently written on the flowcell EEPROM, it will write the data in a suitable
    format. If the EEPROM contains a data version that supports this field, it will be updated,
    and all other fields will be preserved. If the EEPROM contains a data version that doesn't
    support this field, this call will fail with FAILED_PRECONDITION and the EEPROM will not be
    changed.

    This call will fail with FAILED_PRECONDITION if there is no device connected or no flowcell
    attached, or if the flowcell's EEPROM is corrupt or has data in an unknown version.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def write_wells_per_channel(self, request, context):
    """Write the number of wells to the flowcell EEPROM.

    Well counts greater than the number supported by the hardware will be rejected. Passing zero
    will effectively set it to the default for this device.

    If nothing is currently written on the flowcell EEPROM, it will write the data in a suitable
    format. If the EEPROM contains a data version that supports this field, it will be updated,
    and all other fields will be preserved. If the EEPROM contains a data version that doesn't
    support this field, this call will fail with FAILED_PRECONDITION and the EEPROM will not be
    changed.

    This call will fail with FAILED_PRECONDITION if there is no device connected or no flowcell
    attached, or if the flowcell's EEPROM is corrupt or has data in an unknown version.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def write_product_code(self, request, context):
    """Write the product code to the flowcell EEPROM.

    This is the code presented to customers in the shop, eg: "FLO-MIN106".

    Produce codes over 10 characters or containing unprintable characters will be rejected with
    INVALID_ARGUMENT. An empty string effectively clears the product code.

    If nothing is currently written on the flowcell EEPROM, it will write the data in a suitable
    format. If the EEPROM contains a data version that supports this field, it will be updated,
    and all other fields will be preserved. If the EEPROM contains a data version that doesn't
    support this field, this call will fail with FAILED_PRECONDITION and the EEPROM will not be
    changed.

    This call will fail with FAILED_PRECONDITION if there is no device connected or no flowcell
    attached, or if the flowcell's EEPROM is corrupt or has data in an unknown version.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def write_temperature_offset(self, request, context):
    """Write the temperature offset to the flowcell EEPROM.

    The temperature offset is specified in hundreths of a degree Celsius, and can range from
    -327.67 degrees Celsius to 327.67 degrees Celsius. The value -32767 will be accepted, but
    will cause the temperature offset to cleared, just as though no value had been provided at
    all.

    If nothing is currently written on the flowcell EEPROM, it will write the data in a suitable
    format. If the EEPROM contains a data version that supports this field, it will be updated,
    and all other fields will be preserved. If the EEPROM contains a data version that doesn't
    support this field, this call will fail with FAILED_PRECONDITION and the EEPROM will not be
    changed.

    This call will fail with FAILED_PRECONDITION if there is no device connected or no flowcell
    attached, or if the flowcell's EEPROM is corrupt or has data in an unknown version.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ProductionServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'write_flowcell_data': grpc.unary_unary_rpc_method_handler(
          servicer.write_flowcell_data,
          request_deserializer=minknow_dot_rpc_dot_production__pb2.WriteFlowcellDataRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_production__pb2.WriteFlowcellDataResponse.SerializeToString,
      ),
      'write_flowcell_id': grpc.unary_unary_rpc_method_handler(
          servicer.write_flowcell_id,
          request_deserializer=minknow_dot_rpc_dot_production__pb2.WriteFlowcellIdRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_production__pb2.WriteFlowcellIdResponse.SerializeToString,
      ),
      'write_wells_per_channel': grpc.unary_unary_rpc_method_handler(
          servicer.write_wells_per_channel,
          request_deserializer=minknow_dot_rpc_dot_production__pb2.WriteWellsPerChannelRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_production__pb2.WriteWellsPerChannelResponse.SerializeToString,
      ),
      'write_product_code': grpc.unary_unary_rpc_method_handler(
          servicer.write_product_code,
          request_deserializer=minknow_dot_rpc_dot_production__pb2.WriteProductCodeRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_production__pb2.WriteProductCodeResponse.SerializeToString,
      ),
      'write_temperature_offset': grpc.unary_unary_rpc_method_handler(
          servicer.write_temperature_offset,
          request_deserializer=minknow_dot_rpc_dot_production__pb2.WriteTemperatureOffsetRequest.FromString,
          response_serializer=minknow_dot_rpc_dot_production__pb2.WriteTemperatureOffsetResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ont.rpc.production.ProductionService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))