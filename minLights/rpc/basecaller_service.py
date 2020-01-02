### THIS FILE IS AUTOGENERATED. DO NOT EDIT THIS FILE DIRECTLY ###
from .basecaller_pb2_grpc import *
from . import basecaller_pb2
from minLights.rpc.basecaller_pb2 import *
from minLights.rpc._support import MessageWrapper, ArgumentError
import time
import logging

__all__ = [
    "Basecaller",
    "ListConfigsByKitRequest",
    "ListConfigsByKitResponse",
    "StartRequest",
    "StartResponse",
    "CancelRequest",
    "CancelResponse",
    "RunInfo",
    "GetInfoRequest",
    "GetInfoResponse",
    "WatchRequest",
    "WatchResponse",
    "State",
    "STATE_RUNNING",
    "STATE_SUCCESS",
    "STATE_ERROR",
    "STATE_CANCELLED",
    "SelectionPreset",
    "PRESET_ALL_RUNNING",
    "PRESET_MOST_RECENTLY_STARTED",
    "PRESET_ALL",
]

class Basecaller(object):
    def __init__(self, channel):
        self._stub = BasecallerStub(channel)
        self._pb = basecaller_pb2

    def list_configs_by_kit(self, _message=None, _timeout=None, **kwargs):
        """
        List the available basecalling configurations sorted by flow cell and kit.

        Since 3.5

        :rtype: ListConfigsByKitResponse
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.list_configs_by_kit(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.basecaller.Basecaller.list_configs_by_kit. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = ListConfigsByKitRequest()

        if len(unused_args) > 0:
            raise ArgumentError("list_configs_by_kit got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.list_configs_by_kit(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.basecaller.Basecaller.list_configs_by_kit. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

    def start(self, _message=None, _timeout=None, **kwargs):
        """
        Start basecalling reads files.

        Since 3.5

        :param input_reads_directories:
            Input directories to search for reads to be basecalled.

            Currently, only one directory can be specified, but this definition allows for multiple in
            the future without breaking compatibility.
        :param output_reads_directory:
            Output directory where called reads will be placed.

            Reads will be sorted into subdirectories based on the sequencing run they came from.
        :param configuration:
            The name of the basecalling configuration to use.
        :param fast5_out:
            Enable output of .fast5 files containing original raw reads, event data/trace table from
            basecall and basecall result sequence.

            This causes .fast5 files to be output in addition to FASTQ files.
        :param compress_fastq:
            Enable gzip compression of output FASTQ files.
        :param disable_events:
            Prevent events / trace tables being written to .fast5 files.

            If event tables are not required for downstream processing (eg: for 1d^2) then it is more
            efficient (and produces smaller files) to disable them.

            This has no effect if ``fast5_out`` is not enabled.
        :param recursive:
            Recursively find fast5 files to basecall in the `input_reads_directories`.

            If False, only the fast5 files directly in one of the `input_reads_directories` will be
            basecalled. If True, subdirectories of those directories will also be searched recursively.
        :param barcoding_kits:
            The names of the barcoding kits to use (or an empty list if no barcoding should be performed.)

            Since: 3.6
        :param trim_barcodes:
            Control if barcodes should be trimmed from output sequences (only has an effect if barcoding_kits is specified).

            Since: 3.6
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
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.basecaller.Basecaller.start. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = StartRequest()

        if 'input_reads_directories' in kwargs:
            unused_args.remove('input_reads_directories')
            _message.input_reads_directories.extend(kwargs['input_reads_directories'])

        if 'output_reads_directory' in kwargs:
            unused_args.remove('output_reads_directory')
            _message.output_reads_directory = kwargs['output_reads_directory']

        if 'configuration' in kwargs:
            unused_args.remove('configuration')
            _message.configuration = kwargs['configuration']

        if 'fast5_out' in kwargs:
            unused_args.remove('fast5_out')
            _message.fast5_out = kwargs['fast5_out']

        if 'compress_fastq' in kwargs:
            unused_args.remove('compress_fastq')
            _message.compress_fastq = kwargs['compress_fastq']

        if 'disable_events' in kwargs:
            unused_args.remove('disable_events')
            _message.disable_events = kwargs['disable_events']

        if 'recursive' in kwargs:
            unused_args.remove('recursive')
            _message.recursive = kwargs['recursive']

        if 'barcoding_kits' in kwargs:
            unused_args.remove('barcoding_kits')
            _message.barcoding_kits.extend(kwargs['barcoding_kits'])

        if 'trim_barcodes' in kwargs:
            unused_args.remove('trim_barcodes')
            _message.trim_barcodes = kwargs['trim_barcodes']

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
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.basecaller.Basecaller.start. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

    def cancel(self, _message=None, _timeout=None, **kwargs):
        """
        Stop a basecalling that was started by start_basecalling_reads().

        Since 3.5

        :param id:
            An identifier as returned from a call to start() or list().
        :rtype: CancelResponse
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.cancel(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.basecaller.Basecaller.cancel. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = CancelRequest()

        if 'id' in kwargs:
            unused_args.remove('id')
            _message.id = kwargs['id']

        if len(unused_args) > 0:
            raise ArgumentError("cancel got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.cancel(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.basecaller.Basecaller.cancel. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

    def get_info(self, _message=None, _timeout=None, **kwargs):
        """
        Gets information about one or more basecalling operations.

        Since 3.5

        :param preset:
            A pre-determined selection of runs.
        :param id:
            An identifier, as returned by start().
        :param list:
            A list of identifiers, as returned by start().
        :rtype: GetInfoResponse
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.get_info(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.basecaller.Basecaller.get_info. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        # check oneof group 'selection'
        oneof_fields = set([
            'preset',
            'id',
            'list',
        ])
        if len(unused_args & oneof_fields) > 1:
            raise ArgumentError("get_info given multiple conflicting arguments: '{}'".format("', '".join(unused_args & oneof_fields)))
        _message = GetInfoRequest()

        if 'preset' in kwargs:
            unused_args.remove('preset')
            _message.preset = kwargs['preset']

        if 'id' in kwargs:
            unused_args.remove('id')
            _message.id = kwargs['id']

        if 'list' in kwargs:
            unused_args.remove('list')
            _message.list.CopyFrom(kwargs['list'])

        if len(unused_args) > 0:
            raise ArgumentError("get_info got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.get_info(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.basecaller.Basecaller.get_info. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

    def watch(self, _message=None, _timeout=None, **kwargs):
        """
        Monitors basecalls, returning messages when basecalls are started, stopped or receive
        progress updates.

        The current state of all currently-running basecalls will be returned in the initial set of
        messages. Optionally, the state of all already-finished runs can be included. Note that this
        initial state may be split among several responses.

        Note that progress updates may be rate limited to avoid affecting performance.

        Since 3.5

        :param send_finished_runs:
            By default, no information will be sent about runs that were already finished when this call
            was made. Setting this to true will cause the state of already-finished runs to be returned.
        :rtype: WatchResponse
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.watch(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.basecaller.Basecaller.watch. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = WatchRequest()

        if 'send_finished_runs' in kwargs:
            unused_args.remove('send_finished_runs')
            _message.send_finished_runs = kwargs['send_finished_runs']

        if len(unused_args) > 0:
            raise ArgumentError("watch got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.watch(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.basecaller.Basecaller.watch. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

