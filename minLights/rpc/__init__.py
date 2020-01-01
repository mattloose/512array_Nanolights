"""
MinKNOW RPC Access
==================

Provides access to MinKNOW via RPC.

This RPC system is gRPC-based. You might want to look at the `gRPC
documentation <http://www.grpc.io/grpc/python/>`_ for more information, but most
of the detail is hidden by the code in this module.

The RPC system is divided into services, covering related units of functionality
like controlling the device or managing data acquisition.

The core class is :py:class:`Connection` - this provides a connection to MinKNOW, with a
property for each service.

For each service, the related Protobuf messages are available from
``minLights.rpc.<service>_service``, or as ``connection.<service>._pb``
(if ``connection`` is a Connection object).


.. _rpc-services:

Services
--------

The available services are:

acquisition
    Control data acquisition. This includes setting up the analysis configuration. See
    :py:class:`acquisition_service.AcquisitionService` for a description of the available methods.
device
    Get information about and control the attached device. This useful presents information and
    settings in a device-independent way, so it can be used on PromethIONs as easily as on MinIONs.
    See :py:class:`device_service.DeviceService` for a description of the available methods.
instance
    Get information about the instance of MinKNOW you are connected to (eg: software version).
    See :py:class:`instance_service.InstanceService` for a description of the available methods.
minion_device
    MinION-specific device interface. This exposes low-level settings for MinIONs and similar
    devices (eg: GridIONs). See :py:class:`minion_device_service.MinionDeviceService` for a
    description of the available methods.
protocol
    Control protocol scripts. See :py:class:`protocol_service.ProtocolService` for a description of
    the available methods.


Convenience Wrappers
--------------------

The :py:class:`StatusWatcher` class provides a more convenient interface to the
:py:meth:`acquisition.AcquisitionService.watch_for_status_change` method.

"""

import grpc
import logging

import os

#
# Services
#
_services = {
    'acquisition': ['AcquisitionService'],
    'analysis_configuration': ['AnalysisConfigurationService'],
    'data': ['DataService'],
    'device': ['DeviceService'],
    'keystore': ['KeyStoreService'],
    'instance': ['InstanceService'],
    'log': ['LogService'],
    'minion_device': ['MinionDeviceService'],
    'protocol': ['ProtocolService'],
    'production': ['ProductionService'],
    'promethion_device': ['PromethionDeviceService'],
    'statistics': ['StatisticsService'],
}
_optional_services = ['production']


#
# Module meta-information
#

__all__ = [svc + '_service' for svc in _services] + [
    'Connection',
    'StatusWatcher',
    'StreamingRequestThread',
    'grpc_credentials',
    'manager',
    'basecaller',
]


#
# Submodule imports
#

from .wrappers import StatusWatcher, StreamingRequestThread

# Convenience imports for each service
import importlib

# The reason this _load function has to be here (and not just run as part of the init setup) is because trying
# to import the grpc services will eventually try to access the minLights.rpc submodule before we have created it.
#
# For example, acquisition_service.py will load acquisition_pb2_grpc.py, which will try to run:
#       `import minLights.rpc.acquisition_pb2 as minknow_dot_rpc_dot_acquisition__pb2`
#
# The `import minLights.rpc` part is the problem here. Because we are in the rpc module's __init__.py, we are trying to create the module,
# so naturally trying to reference that module before it has been fully loaded results in an AttributeError saying the minknow module has no
# attribute 'rpc'
#
# The fix is to first load the rpc module and and then call this _load() function which will load the services after the rpc module.
def _load():
    for svc in _services:
        try:
            # effectively does `import .{svc}_service as {svc}_service`
            importlib.import_module('.{}_service'.format(svc), __name__)
        except ImportError:
            if svc not in _optional_services:
                raise


logger = logging.getLogger(__name__)

#
# Position-independent RPCs
#

def grpc_credentials():
    """Get a grpc.ChannelCredentials object for connecting to secure versions of MinKNOW"s gRPC
    services.

    Use like:

    >>> import grpc
    >>> channel = grpc.secure_channel("127.0.0.1:9502", grpc_credentials())
    """
    try:
        return grpc_credentials.cached_credentials
    except AttributeError:
        cert_path = os.path.join(_minknow_path(), "conf", "rpc-certs", "ca.crt")
        with open(cert_path, "r") as file_obj:
            grpc_credentials.cached_credentials = grpc.ssl_channel_credentials(file_obj.read())
        return grpc_credentials.cached_credentials

def manager(host="localhost", port=9502, use_tls=True):
    """Connect to the manager.

    Args:
        host (str): the hostname to connect to (note that IP addresses will not work for TLS
            connections)
        port (int): override the port to connect to
        use_tls (bool): set to False to use an insecure channel connection

    Returns:
        minLights.rpc.manager_service.ManagerService: a proxy object for the manager; it will have a
        host attribute set to match the host argument.
    """
    import minLights.rpc.manager_service
    if use_tls:
        channel = grpc.secure_channel(host + ":" + str(port), grpc_credentials())
    else:
        channel = grpc.insecure_channel(host + ":" + str(port))
    service = minLights.rpc.manager_service.ManagerService(channel)
    service.host = host # needed to find other services
    return service

def basecaller(manager=None, host=None, port=None, use_tls=True):
    """Connect to the basecaller service.

    This service allows directories of reads files to be basecalled.

    If no manager object or port is provided, a connection to the manager will be attempted.

    Args:
        manager (minLights.rpc.manager_service.ManagerService): a manager object
        host (str): the host to connect to (not required if ``manager`` has the ``host`` attribute)
        port (int): override the port for the basecaller service (instead of querying the manager)
        use_tls (bool): set to False to use an insecure channel connection

    Returns:
        minLights.rpc.basecaller_service.Basecaller: a proxy object for the basecaller
    """
    import minLights.rpc.basecaller_service
    if host is None:
        if manager is not None:
            host = manager.host
        else:
            host = "localhost"
    if port is None:
        if manager is None:
            manager = globals()['manager'](host)
        if use_tls:
            port = manager.basecaller_api().secure
        else:
            port = manager.basecaller_api().insecure
    if use_tls:
        channel = grpc.secure_channel(host + ":" + str(port), grpc_credentials())
    else:
        channel = grpc.insecure_channel(host + ":" + str(port))
    return minLights.rpc.basecaller_service.Basecaller(channel)

#
# Connection class
#

class Connection(object):
    """A connection to a MinKNOW sequencing position via RPC.

    Note that this only provides access to the new RPC system. The old one is
    available via the minknow.engine_client module.

    Each service is available as a property of the same name on the Connection
    object. See :ref:`rpc-services` for a list.

    Given a connection object ``connection``, for each service,
    ``connection.<service>`` is a "service object". This exposes the RPC methods
    for that service in a more convenient form than gRPC's own Python bindings
    do.

    For example, when calling ``start_protocol`` on the ``protocol`` service,
    instead of doing

    >>> protocol_service.start_protocol(
    >>>     protocol_service._pb.StartProtocolMessage(path="my_script"))

    you can do

    >>> connection.protocol.start_protocol(path="my_script")

    Note that you must use keyword arguments - no positional parameters are
    available.

    This "unwrapping" of request messages only happens at one level, however. If
    you want to change the target temperature settings on a MinION, you need to do
    something like

    >>> temp_settings = connection.minion_device._pb.TemperatureRange(min=37.0, max=37.0)
    >>> connection.minion_device.change_settings(
    >>>     temperature_target=temp_settings)
    """

    def __init__(self, port=None, host='127.0.0.1', use_tls=False):
        """Connect to MinKNOW.

        The port for a given instance of MinKNOW is provided by the manager
        service.

        If no port is provided, it will attempt to get the port from the
        MINKNOW_RPC_PORT environment variable (set for protocol scripts, for
        example). If this environment variable does not exist (or is not a
        number), it will raise an error.

        :param port: the port to connect on (defaults to ``MINKNOW_RPC_PORT`` environment variable)
        :param host: the host MinKNOW is running on (defaults to localhost)
        """
        import grpc, os, time

        self.host = host
        if port is None:
            port = int(os.environ['MINKNOW_RPC_PORT'])
        self.port = port

        channel_opts = [
            ('grpc.max_send_message_length', 16 * 1024 * 1024),
            ('grpc.max_receive_message_length', 16 * 1024 * 1024),
            ('grpc.http2.min_time_between_pings_ms', 1000),
        ]

        error = None
        retry_count = 5
        for i in range(retry_count):
            if use_tls:
                self.channel = grpc.secure_channel("{}:{}".format(host, port),
                                                   credentials=grpc_credentials(),
                                                   options=channel_opts)
            else:
                self.channel = grpc.insecure_channel("{}:{}".format(host, port), options=channel_opts)

            # One entry for each service
            for name, svc_list in _services.items():
                for svc in svc_list:
                    try:
                        # effectively does `self.{name} = {name}_service.{svc}(self.channel)`
                        setattr(self, name, getattr(globals()[name + '_service'], svc)(self.channel))
                    except KeyError:
                        if name not in _optional_services:
                            raise

            # Ensure channel is ready for communication
            try:
                self.instance.get_version_info()
                error = None
                break
            except grpc.RpcError as e:
                logger.info("Error received from rpc")
                if (e.code() == grpc.StatusCode.INTERNAL and
                        e.details() == "GOAWAY received"):
                    logger.warning("Failed to connect to minknow instance (retry %s/%s): %s", i+1, retry_count, e.details())
                elif (e.code() == grpc.StatusCode.UNAVAILABLE):
                    logger.warning("Failed to connect to minknow instance (retry %s/%s): %s", i+1, retry_count, e.details())
                else:
                    raise
                error = e
                time.sleep(0.5)

        if error:
            raise error


import platform
def _minknow_path(operating_system=platform.system()):
    return {
        "Darwin": os.path.join(os.sep, "Applications", "MinKNOW.app", "Contents", "Resources"),
        "Linux": os.path.join(os.sep, "opt", "ONT", "MinKNOW"),
        "Windows": os.path.join(os.sep, "C:\\Program Files", "OxfordNanopore", "MinKNOW"),
    }.get(operating_system, None)
