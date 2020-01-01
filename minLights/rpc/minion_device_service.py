### THIS FILE IS AUTOGENERATED. DO NOT EDIT THIS FILE DIRECTLY ###
from .minion_device_pb2_grpc import *
from . import minion_device_pb2
from minLights.rpc.minion_device_pb2 import *
from minLights.rpc._support import MessageWrapper, ArgumentError
import time
import logging

__all__ = [
    "MinionDeviceService",
    "TemperatureRange",
    "SamplingFrequencyParameters",
    "MinionDeviceSettings",
    "ChangeSettingsRequest",
    "ChangeSettingsResponse",
    "GetSettingsRequest",
    "GetSettingsResponse",
]

class MinionDeviceService(object):
    def __init__(self, channel):
        self._stub = MinionDeviceServiceStub(channel)
        self._pb = minion_device_pb2

    def change_settings(self, _message=None, _timeout=None, **kwargs):
        """
        Change the settings for the active device.

        If you omit a parameter, that setting will not be changed.

        This call is atomic: either all the settings will be applied, or none of them (if there is an
        error).

        :param bias_voltage:
            The voltage potential to be applied across the wells (in millivolts).

            This voltage drives the process of forcing molecules through the nanopores.

            The range of possible values is -1275 to 1275 inclusive, in 5mv steps.

            When setting this value, if the provided value is not a multiple of 5, an error will be
            returned.
        :param sampling_frequency:
            The number of measurements to take each second.

            This value is derived from the sampling_frequency_params values, and so not all values are
            possible.

            When changing the sampling frequency, either this value can be provided, or the values in
            sampling_frequency_params can be provided (attempting to provide both will cause the RPC to
            fail with an error). If this value is provided, the nearest admissible value will be used
            (eg: if 3000Hz is requested, 3012Hz will be applied).

            This value cannot be changed during acquisition, and changing it will invalidate the current
            calibration.

            Note that setting the sampling frequency to over 20000Hz (20KHz) will force the
            sinc_decimation value to 32.
        :param channel_config:
            The per-channel configuration.

            Each channel can be set to one of 16 states, which specifies the set of electrical
            connections to make. This includes which, if any, of the four wells linked to the channel to
            use.

            Note that channel names start at 1. If you pass 0 as a key in this map, it will result in
            an error.

            When changing the device settings, any omitted channels (or channels set to
            CHANNEL_CONFIG_KEEP) will use the default value set in
            ChangeSettingsRequest.channel_config_default.
        :param enable_temperature_control:
            Whether to enable temperature control.

            If true, the device will attempt to keep its temperature within the bounds given by
            ``temperature_lower_bound`` and ``temperature_upper_bound``. If false, it will not do any
            temperature control.

            Default is enabled.

            It is recommended that this is enabled. If temperature control is disabled, the device may
            overheat. In this case, it will turn itself off, and must be unplugged and allowed to cool
            before using again.
        :param temperature_target:
            The target temperature range for the device.

            If enable_temperature_control is set to true, the device will attempt to keep its temperature
            between the min and max values provided here.

            Default is defined in application config.

            Note that if soft temperature control is enabled, only the ``max`` temperature is used.
        :param int_capacitor:
            Integration capacitor value.

            This affects the sensitivity of the measurement: lower capacitor values give more
            sensitive measurements (but also more noise). Changing this will invalidate the current
            calibration.

            Default is 250.0
        :param test_current:
            The level of current used in the TEST_CURRENT channel configuration.

            This can be set in the range 0pA to 350pA in 50pA intervals, default is 100.0
        :param unblock_voltage:
            The unblock voltage potential (in millivolts).

            When a channel is set to one of the UNBLOCK configurations, the specified well will have this
            voltage applied across it, rather than bias_voltage.

            The range of possible values is -372 to 0 inclusive, in 12mv steps,  default is 0.

            When setting this value, if the provided value is not a multiple of 12, an error will be
            returned.
        :param overcurrent_limit:
            Whether to enable detection of excessive current.

            The ADC output of a channel that trips the overcurrent depends on what track and hold gain
            has been set to.

            Default is enabled.
        :param samples_to_reset:
            The the number of integrator resets per sample.

            The range of possible values is 0 to 255, default is 1
        :param th_gain:
            Track/Hold gain.

            Default is 5.0
        :param sinc_delay:
            Delay from 2:1 mux switch to sinc filter enable in ADC clocks.

            The range of possible values is 0 to 15, default is 4.0
        :param th_sample_time:
            Track/Hold sample time in microseconds (us).

            The range of possible values is 0.5us to 7.5us in steps of 0.5us, default is 0.5.
        :param int_reset_time:
            Integrator reset time in microseconds (us).

            This value forms a part of the integration time specified in the sampling frequency
            parameters.

            The range of possible values is 1us to 16us in steps of 0.5us, default is 3.5.
        :param sinc_decimation:
            Decimation.

            If the integration time is set to less than 50us (or, equivalently, the sampling frequency is
            set to greater than 20KHz), this value will be forced to 32.

            Default is 64.0.
        :param low_pass_filter:
            Low pass filter that should be applied.

            Default is 40kHz
        :param non_overlap_clock:
            Amount of non-overlap for non-overlapping clocks.

            Default is NOC_1_HS_CLOCK.
        :param bias_current:
            Bias current.

            This can be set in the range 0 to 15 in intervals of 5, default is 5.
        :param compensation_capacitor:
            Compensation capacitor value.

            This can be set in the range 0 to 49 in intervals of 7, default is 14.
        :param sampling_frequency_params:
            Sampling frequency parameters.

            The sampling_frequency value is calculated from these settings.

            When changing the sampling frequency, either the values here can be provided, or a
            sampling_frequency can be provided (attempting to provide both will cause the RPC to fail
            with an error).

            WARNING: This should not be used in a change_settings call without consulting the hardware
            documentation for permissible combinations of values. MinKNOW will only do minimal checking
            of the values given here; if you use invalid combinations of settings, the device will be
            unable to acquire data, and may even be permanently damaged.

            This value cannot be changed during acquisition.
        :param enable_asic_power:
            Enable ASIC analogue supply voltage.

            This must be enabled to heat and acquire data from the ASIC. It can be disabled to save
            power, but doing so will allow the ASIC to cool down, and it will take time to heat it up
            again.

            Default is true.
        :param fan_speed:
            The speed of the fan when temperature control is off.

            If ``enable_temperature_control`` is false, this setting will be ignored, as the temperature
            control routines on the device will control the speed of the fan.

            Note that this setting does not apply to GridIONs.

            Default is FANSPEED_MAX.
        :param allow_full_fan_stop:
            Whether to allow the fan to completely stop.

            Allowing the fan to stop causes issues on some old MinION models.

            Note that this setting does not apply to GridIONs.

            Default is false.
        :param enable_soft_temperature_control:
            Enable soft temperature control.

            "Soft" temperature control is a more intelligent temperature control algorithm. It works on a
            single target temperature, and dynamically adjusts the fan speed to reach that temperature
            quickly, and then mainains the target temperature with high precision.

            If this is disabled, "hard" temperature control is used instead. This is a naive algorithm
            that simply turns the fan up when dropping below the minimum temperature and turns it down
            when going above the maximum temperature.

            If ``enable_temperature_control`` is false, this setting is ignored.

            It is recommended that this is enabled.

            Default is true.
        :param enable_bias_voltage_lookup:
            Use the bias voltage lookup table to set the bias voltage.

            If this is enabled, the bias voltage will be updated every millisecond with each entry in the
            bias voltage lookup table (see ``bias_voltage_lookup_table``) in turn, cycling through when
            the end of the table is reached.

            This has the effect of producing a bias voltage waveform.

            When enabling this, it is required to either provide the lookup table entries at the same
            time, or to have already provided them in a previous call.

            Default is false.
        :param bias_voltage_lookup_table:
            The bias voltage lookup table.

            If no entries are provided, the existing lookup table (if any) is preserved.

            See ``enable_bias_voltage_lookup``.

            Up to 75 values can be provided. The values have the same constraints as ``bias_voltage``.
        :param channel_config_default:
            The default channel configuration.

            This provides the default configuration to apply to any channels not listed in
            settings.channel_config.
        :rtype: ChangeSettingsResponse
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.change_settings(_message, timeout=_timeout), unwraps=[])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.minion_device.MinionDeviceService.change_settings. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = ChangeSettingsRequest()

        if 'bias_voltage' in kwargs:
            unused_args.remove('bias_voltage')
            _message.settings.bias_voltage.value = kwargs['bias_voltage']

        if 'sampling_frequency' in kwargs:
            unused_args.remove('sampling_frequency')
            _message.settings.sampling_frequency.value = kwargs['sampling_frequency']

        if 'channel_config' in kwargs:
            unused_args.remove('channel_config')
            _message.settings.channel_config.update(kwargs['channel_config'])

        if 'enable_temperature_control' in kwargs:
            unused_args.remove('enable_temperature_control')
            _message.settings.enable_temperature_control.value = kwargs['enable_temperature_control']

        if 'temperature_target' in kwargs:
            unused_args.remove('temperature_target')
            _message.settings.temperature_target.CopyFrom(kwargs['temperature_target'])

        if 'int_capacitor' in kwargs:
            unused_args.remove('int_capacitor')
            _message.settings.int_capacitor = kwargs['int_capacitor']

        if 'test_current' in kwargs:
            unused_args.remove('test_current')
            _message.settings.test_current.value = kwargs['test_current']

        if 'unblock_voltage' in kwargs:
            unused_args.remove('unblock_voltage')
            _message.settings.unblock_voltage.value = kwargs['unblock_voltage']

        if 'overcurrent_limit' in kwargs:
            unused_args.remove('overcurrent_limit')
            _message.settings.overcurrent_limit.value = kwargs['overcurrent_limit']

        if 'samples_to_reset' in kwargs:
            unused_args.remove('samples_to_reset')
            _message.settings.samples_to_reset.value = kwargs['samples_to_reset']

        if 'th_gain' in kwargs:
            unused_args.remove('th_gain')
            _message.settings.th_gain = kwargs['th_gain']

        if 'sinc_delay' in kwargs:
            unused_args.remove('sinc_delay')
            _message.settings.sinc_delay.value = kwargs['sinc_delay']

        if 'th_sample_time' in kwargs:
            unused_args.remove('th_sample_time')
            _message.settings.th_sample_time.value = kwargs['th_sample_time']

        if 'int_reset_time' in kwargs:
            unused_args.remove('int_reset_time')
            _message.settings.int_reset_time.value = kwargs['int_reset_time']

        if 'sinc_decimation' in kwargs:
            unused_args.remove('sinc_decimation')
            _message.settings.sinc_decimation = kwargs['sinc_decimation']

        if 'low_pass_filter' in kwargs:
            unused_args.remove('low_pass_filter')
            _message.settings.low_pass_filter = kwargs['low_pass_filter']

        if 'non_overlap_clock' in kwargs:
            unused_args.remove('non_overlap_clock')
            _message.settings.non_overlap_clock = kwargs['non_overlap_clock']

        if 'bias_current' in kwargs:
            unused_args.remove('bias_current')
            _message.settings.bias_current.value = kwargs['bias_current']

        if 'compensation_capacitor' in kwargs:
            unused_args.remove('compensation_capacitor')
            _message.settings.compensation_capacitor.value = kwargs['compensation_capacitor']

        if 'sampling_frequency_params' in kwargs:
            unused_args.remove('sampling_frequency_params')
            _message.settings.sampling_frequency_params.CopyFrom(kwargs['sampling_frequency_params'])

        if 'enable_asic_power' in kwargs:
            unused_args.remove('enable_asic_power')
            _message.settings.enable_asic_power.value = kwargs['enable_asic_power']

        if 'fan_speed' in kwargs:
            unused_args.remove('fan_speed')
            _message.settings.fan_speed = kwargs['fan_speed']

        if 'allow_full_fan_stop' in kwargs:
            unused_args.remove('allow_full_fan_stop')
            _message.settings.allow_full_fan_stop.value = kwargs['allow_full_fan_stop']

        if 'enable_soft_temperature_control' in kwargs:
            unused_args.remove('enable_soft_temperature_control')
            _message.settings.enable_soft_temperature_control.value = kwargs['enable_soft_temperature_control']

        if 'enable_bias_voltage_lookup' in kwargs:
            unused_args.remove('enable_bias_voltage_lookup')
            _message.settings.enable_bias_voltage_lookup.value = kwargs['enable_bias_voltage_lookup']

        if 'bias_voltage_lookup_table' in kwargs:
            unused_args.remove('bias_voltage_lookup_table')
            _message.settings.bias_voltage_lookup_table.extend(kwargs['bias_voltage_lookup_table'])

        if 'channel_config_default' in kwargs:
            unused_args.remove('channel_config_default')
            _message.channel_config_default = kwargs['channel_config_default']

        if len(unused_args) > 0:
            raise ArgumentError("change_settings got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.change_settings(_message, timeout=_timeout), unwraps=[])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.minion_device.MinionDeviceService.change_settings. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error

    def get_settings(self, _message=None, _timeout=None, **kwargs):
        """
        Get the current settings for the active device.

        :rtype: GetSettingsResponse
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            retry_count = 20
            error = None
            for i in range(retry_count):
                try:
                    result = MessageWrapper(self._stub.get_settings(_message, timeout=_timeout), unwraps=["settings"])
                    return result
                except grpc.RpcError as e:
                    # Retrying unidentified grpc errors to keep clients from crashing
                    if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                    (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                        logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.minion_device.MinionDeviceService.get_settings. Attempt {}.'.format(e.code(), e.details(), i))
                    else:
                        raise
                    error = e
                time.sleep(1)
            raise error

        unused_args = set(kwargs.keys())

        _message = GetSettingsRequest()

        if len(unused_args) > 0:
            raise ArgumentError("get_settings got unexpected keyword arguments '{}'".format("', '".join(unused_args)))
        retry_count = 20
        error = None
        for i in range(retry_count):
            try:
                result = MessageWrapper(self._stub.get_settings(_message, timeout=_timeout), unwraps=["settings"])
                return result
            except grpc.RpcError as e:
                # Retrying unidentified grpc errors to keep clients from crashing
                if (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details()) or\
                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()):
                    logging.info('Bypassed ({}: {}) error for grpc: ont.rpc.minion_device.MinionDeviceService.get_settings. Attempt {}.'.format(e.code(), e.details(), i))
                else:
                    raise
                error = e
            time.sleep(1)
        raise error


