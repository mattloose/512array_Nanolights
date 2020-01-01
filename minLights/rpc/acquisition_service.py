### THIS FILE IS AUTOGENERATED. DO NOT EDIT THIS FILE DIRECTLY ###
from .acquisition_pb2_grpc import *
from . import acquisition_pb2
from minLights.rpc.acquisition_pb2 import *
from minLights.rpc._support import MessageWrapper, ArgumentError
import time
import logging

__all__ = [
    "AcquisitionService",
    "StartRequest",
    "StartResponse",
    "StopRequest",
    "StopResponse",
    "WatchForStatusChangeRequest",
    "WatchForStatusChangeResponse",
    "CurrentStatusRequest",
    "CurrentStatusResponse",
    "GetProgressRequest",
    "GetProgressResponse",
    "GetAcquisitionRunInfoRequest",
    "AcquisitionYieldSummary",
    "ChannelStateInfo",
    "AcquisitionConfigSummary",
    "AcquisitionRunInfo",
    "ListAcquisitionRunsRequest",
    "ListAcquisitionRunsResponse",
    "GetCurrentAcquisitionRunRequest",
    "WatchCurrentAcquisitionRunRequest",
    "SetSignalReaderRequest",
    "SetSignalReaderResponse",
    "MinknowStatus",
    "ERROR_STATUS",
    "READY",
    "STARTING",
    "PROCESSING",
    "FINISHING",
    "Option",
    "AUTO",
    "DISABLE",
    "FORCE",
    "Purpose",
    "OTHER_PURPOSE",
    "SEQUENCING",
    "CALIBRATION",
    "AcquisitionState",
    "ACQUISITION_STARTING",
    "ACQUISITION_RUNNING",
    "ACQUISITION_FINISHING",
    "ACQUISITION_COMPLETED",
    "AcquisitionStopReason",
    "STOPPED_NOT_SET",
    "STOPPED_USER_REQUESTED",
    "STOPPED_NO_DISK_SPACE",
    "STOPPED_DEVICE_STOPPED_ACQUISITION",
    "STOPPED_STARTING_ANOTHER_RUN",
    "STOPPED_PROTOCOL_ENDED",
    "STOPPED_DEVICE_ERROR",
    "FinishingState",
    "FINISHING_UNKNOWN",
    "FINISHING_PROCESSING_DEVICE_SIGNAL",
    "FINISHING_BASECALLING_READS",
    "FINISHING_SAVING_DATA",
]

class AcquisitionService(object):
    def __init__(self, channel):
        self._stub = AcquisitionServiceStub(channel)
        self._pb = acquisition_pb2

    def start(self, _message=None, _timeout=None, **kwargs):
        """
        Starts reading data from the device

        Some setup calls will need to be made before starting data acquisition: particularly setting the analysis configuration, 
        calibration, read writer and bulk writer config and some device calls such as setting the sampling frequency

        If acqusition is already running (even in the FINISHING state), this call will fail.

        On MinIONs and GridIONs, this will enable the ASIC power supply if it is not already enabled.
        See StopRequest.keep_power_on for more details about the implications of this.

        :param wait_until_processing:
            Wait for MinKNOW to enter the PROCESSING state before returning.

            Defaults to false, which will cause this call to return as soon as MinKNOW enters the
            STARTING state.
        :param dont_wait_for_device_ready:
            Prevent waiting until the device is ready before starting acquisition.

            Defaults to false.

            By default, MinKNOW will block in the start() call for the device and flow cell to be ready
            for acquisition (which may take several seconds after plugging in the flow cell on some
            devices). Setting this option will cause the call to return with an error if the device is
            not already prepared to acquire data.

            Since 1.14
        :param generate_report:
            Generate duty time and throughput reports.

            Note that this setting will be ignored (and no reports will be generated) if no protocol is
            running at the time acquisition is started.

            The default setting (AUTO) will only generate reports if purpose is set to SEQUENCING.

            Since 3.0
        :param send_sequencing_read_metrics:
            Whether sequencing read metrics should be reported to Oxford Nanopore.

            These are performance metrics that are used to improve the sequencing technology. They do not
            include any actual sequencing data, only statistics about read lengths, duty time and similar
            generic performance information.

            The default setting (AUTO) will only send metrics if purpose is set to SEQUENCING.

            Since 3.0
        :param send_basecalling_metrics:
            Whether basecalling metrics should be reported to Oxford Nanopore.

            These are performance metrics that are used to improve the sequencing technology. They do not
            include any actual sequencing data, only statistics about basecalling performance.

            The default setting (AUTO) will only send metrics if purpose is set to SEQUENCING.

            NB: this setting is ignored if live basecalling is not enabled, since there will be no
            metrics to send.

            Since 3.2
        :param purpose:
            Specify the purpose of this acquisition period.

            This affects various defaults (see the Purpose enum documentation for more details). It may
            also affect how the user interface presents the state of the protocol.

            Since 3.2
        :param analysis:
            Perform analysis for this acquisition period.

            If this is disabled, no reads, no events, no channel states and no basecalls will be
            generated. Any RPCs that depend on any of these will fail. No reads-based files will be
            produced at all, regardless of any other settings.

            This is mostly useful for calibration (although you should normally use the purpose field
            rather than setting this explicitly).

            The default setting (AUTO) will use the persistent setting from the analysis_configuraiton
            service, unless the purpose is set to CALIBRATION.

            Since 3.2
        :param file_output:
            Allow file output for this acquisition period.

            If this is disabled, the file output settings will be ignored for this acquisition period,
            and no data files will be produced. Note that reports are NOT managed by this setting.

            Note that setting this to FORCE will simply make file output respect the bulk and read writer
            configurations. If each file output type is disabled, you will still get no file output.

            This is mostly useful for calibration (although you should normally use the purpose field
            rather than setting this explicitly).

            The default setting (AUTO) will only suppress file output if purpose is set to CALIBRATION.

            Since 3.2
        :param generate_final_summary:
            Write a final_summary.txt file.

            If file_output is disabled, the final_summary.txt file will not be written regardless of
            this setting.

            The default setting (AUTO) will only enable writing a final_summary.txt file if the purpose
            is set to SEQUENCING.

            Since 3.5 (NB: in 3.3 and 3.4, final_summary.txt was always written out if file_output was
            enabled).
        :rtype: StartResponse
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.start(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.start. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = StartRequest()

        if 'wait_until_processing' in kwargs:
            unused_args.remove('wait_until_processing')
            _message.wait_until_processing = kwargs['wait_until_processing']

        if 'dont_wait_for_device_ready' in kwargs:
            unused_args.remove('dont_wait_for_device_ready')
            _message.dont_wait_for_device_ready = kwargs['dont_wait_for_device_ready']

        if 'generate_report' in kwargs:
            unused_args.remove('generate_report')
            _message.generate_report = kwargs['generate_report']

        if 'send_sequencing_read_metrics' in kwargs:
            unused_args.remove('send_sequencing_read_metrics')
            _message.send_sequencing_read_metrics = kwargs['send_sequencing_read_metrics']

        if 'send_basecalling_metrics' in kwargs:
            unused_args.remove('send_basecalling_metrics')
            _message.send_basecalling_metrics = kwargs['send_basecalling_metrics']

        if 'purpose' in kwargs:
            unused_args.remove('purpose')
            _message.purpose = kwargs['purpose']

        if 'analysis' in kwargs:
            unused_args.remove('analysis')
            _message.analysis = kwargs['analysis']

        if 'file_output' in kwargs:
            unused_args.remove('file_output')
            _message.file_output = kwargs['file_output']

        if 'generate_final_summary' in kwargs:
            unused_args.remove('generate_final_summary')
            _message.generate_final_summary = kwargs['generate_final_summary']

        if len(unused_args) > 0:
            raise ArgumentError("start got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.start(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.start. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

    def stop(self, _message=None, _timeout=None, **kwargs):
        """
        Stops data acquisition.

        Can specify a stop mode that handles what is done with the data when data acquisition is stopped. Refer to the enum
        description for documentation on what each mode does.

        Be aware that this command will return as soon as Minknow enters the FINISHING state and not the READY state.
        So if starting a new experiment then you will have to wait for the READY state seperately

        :param data_action_on_stop:
        :param wait_until_ready:
            Defaults to false
            If false will return as soon as minknow enters the FINISHING state.
            If true then returns as soon as minknow enters the READY state.
        :param keep_power_on:
            Keep the ASIC power on for GridIONs and MinIONs.

            Unless this option is set to true, the ASIC power will be disabled as soon as MinKNOW has
            stopped pulling data from it. This is because removing (or plugging in) a flow cell while the
            power is on can damage it. Disabling the power will also disable the heating element; this is
            likely to cause the device to cool down (particularly for MinIONs).

            You should normally only use this option if you are expecting to start acquisition again
            in a short amount of time.

            This option has no effect on PromethIONs.

            Since 1.15.2
        :rtype: StopResponse
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.stop(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.stop. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = StopRequest()

        if 'data_action_on_stop' in kwargs:
            unused_args.remove('data_action_on_stop')
            _message.data_action_on_stop = kwargs['data_action_on_stop']

        if 'wait_until_ready' in kwargs:
            unused_args.remove('wait_until_ready')
            _message.wait_until_ready = kwargs['wait_until_ready']

        if 'keep_power_on' in kwargs:
            unused_args.remove('keep_power_on')
            _message.keep_power_on = kwargs['keep_power_on']

        if len(unused_args) > 0:
            raise ArgumentError("stop got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.stop(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.stop. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

    def watch_for_status_change(self, _iterator):
        return self._stub.watch_for_status_change(_iterator)

    def watch_current_acquisition_run(self, _message=None, _timeout=None, **kwargs):
        """
        Returns current acquisition run info and streams any changes to the current acquisition

        This call can be made even if acquisition is not running. In this case, the next streamed
        response will be the start of a new acquisition and you will receive updates for that acquisition
        until it finishes.

        If an acquisition finishes this stream will still continue to run and you will be notified when a new acquisition starts.

        Note if you begin this stream before any acquisition is started in minknow the state is `ACQUISITION_COMPLETED`.

        Since 1.13

        :rtype: AcquisitionRunInfo
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.watch_current_acquisition_run(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.watch_current_acquisition_run. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = WatchCurrentAcquisitionRunRequest()

        if len(unused_args) > 0:
            raise ArgumentError("watch_current_acquisition_run got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.watch_current_acquisition_run(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.watch_current_acquisition_run. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

    def current_status(self, _message=None, _timeout=None, **kwargs):
        """
        Check the current status of MinKNOW.

        :rtype: CurrentStatusResponse
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.current_status(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.current_status. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = CurrentStatusRequest()

        if len(unused_args) > 0:
            raise ArgumentError("current_status got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.current_status(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.current_status. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

    def get_progress(self, _message=None, _timeout=None, **kwargs):
        """
        Information on how much data has been acquired, processed and written.

        :rtype: GetProgressResponse
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.get_progress(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.get_progress. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = GetProgressRequest()

        if len(unused_args) > 0:
            raise ArgumentError("get_progress got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.get_progress(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.get_progress. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

    def get_acquisition_info(self, _message=None, _timeout=None, **kwargs):
        """
        Gets information about an acquisition run, run within this instance on MinKNOW.

        If no run ID is provided, information about the most recently started acquisition run is
        provided.

        Since 1.11

        :param run_id:
            The acquisition period to get information about.
        :rtype: AcquisitionRunInfo
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.get_acquisition_info(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.get_acquisition_info. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = GetAcquisitionRunInfoRequest()

        if 'run_id' in kwargs:
            unused_args.remove('run_id')
            _message.run_id = kwargs['run_id']

        if len(unused_args) > 0:
            raise ArgumentError("get_acquisition_info got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.get_acquisition_info(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.get_acquisition_info. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

    def list_acquisition_runs(self, _message=None, _timeout=None, **kwargs):
        """
        Gets information about all previous acquisitions.

        Since 1.11

        :rtype: ListAcquisitionRunsResponse
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.list_acquisition_runs(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.list_acquisition_runs. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = ListAcquisitionRunsRequest()

        if len(unused_args) > 0:
            raise ArgumentError("list_acquisition_runs got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.list_acquisition_runs(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.list_acquisition_runs. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

    def get_current_acquisition_run(self, _message=None, _timeout=None, **kwargs):
        """
        Returns the name and run id of the currently running acquisition.

        Will fail with FAILED_PRECONDITION if there is no acquisition running

        Since 1.11

        :rtype: AcquisitionRunInfo
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.get_current_acquisition_run(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.get_current_acquisition_run. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = GetCurrentAcquisitionRunRequest()

        if len(unused_args) > 0:
            raise ArgumentError("get_current_acquisition_run got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.get_current_acquisition_run(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.get_current_acquisition_run. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

    def set_signal_reader(self, _message=None, _timeout=None, **kwargs):
        """
        Specify the signal reader to use

        Since 3.6

        :param reader: (required)
            The type of signal reader to use
        :param hdf_source:
            The following settings are optional, and only used when setting the reader to hdf5
        :param hdf_mode:
        :param sample_rate_scale_factor:
        :rtype: SetSignalReaderResponse
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.set_signal_reader(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.set_signal_reader. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = SetSignalReaderRequest()

        if 'reader' in kwargs:
            unused_args.remove('reader')
            _message.reader = kwargs['reader']
        else:
            raise ArgumentError("set_signal_reader requires a 'reader' argument")

        if 'hdf_source' in kwargs:
            unused_args.remove('hdf_source')
            _message.hdf_source = kwargs['hdf_source']

        if 'hdf_mode' in kwargs:
            unused_args.remove('hdf_mode')
            _message.hdf_mode = kwargs['hdf_mode']

        if 'sample_rate_scale_factor' in kwargs:
            unused_args.remove('sample_rate_scale_factor')
            _message.sample_rate_scale_factor = kwargs['sample_rate_scale_factor']

        if len(unused_args) > 0:
            raise ArgumentError("set_signal_reader got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.set_signal_reader(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.acquisition.AcquisitionService.set_signal_reader. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error


