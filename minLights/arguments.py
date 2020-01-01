import argparse
import sys


from minLights.utils import nice_join

DEFAULT_ROWS=16
DEFAULT_COLS=32
DEFAULT_CHAIN=1
DEFAULT_SCAN=1
DEFAULT_PARALLEL=1
DEFAULT_PWM_BITS=11
DEFAULT_BRIGHTNESS=100
DEFAULT_GPIO="adafruit-hat"
DEFAULT_PWM_LSB=130
DEFAULT_SLOWDOWN=1

DEFAULT_SERVER_HOST = "127.0.0.1"
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(message)s"
DEFAULT_LOG_LEVEL = "info"
DEFAULT_LOG_PREFIX = ""

LOG_LEVELS = ("debug", "info", "warning", "error", "critical")

LIGHTS_ARGS = (
(
    "--rows-led",
    dict(
        metavar="rows-led",
        type=int,
        help="Display rows. 16 for 16x32, 32 for 32x32. (Default: {})".format(DEFAULT_ROWS),
        default=DEFAULT_ROWS,
    ),
),
(
    "--cols-led",
    dict(
        metavar="cols-led",
        type=int,
        help="Panel columns. Typically 32 or 64. (Default: {})".format(DEFAULT_COLS),
        default=DEFAULT_COLS,
    ),
),
(
    "--led-chain",
    dict(
        metavar="led-chain",
        type=int,
        help="Daisy-chained boards. (Default: {})".format(DEFAULT_CHAIN),
        default=DEFAULT_CHAIN,
    ),
),
(
    "--led-parallel",
    dict(
        metavar="led-parallel",
        type=int,
        help="For Plus-models or RPi2: parallel chains. 1..3. Default: {}".format(DEFAULT_PARALLEL),
        default=DEFAULT_PARALLEL,
    ),
),
(
    "--led-pwm-bits",
    dict(
        metavar="led-pwm-bits",
        type=int,
        help="Bits used for PWM. Something between 1..11. Default: {}".format(DEFAULT_PWM_BITS),
        default=DEFAULT_PWM_BITS,
    ),
),
(
    "--led-brightness",
    dict(
        metavar="led-brightness",
        type=int,
        help="Sets brightness level. Default: {}. Range: 1..100".format(DEFAULT_BRIGHTNESS),
        default=DEFAULT_BRIGHTNESS,
    ),
),
(
        "--led-gpio-mapping",
        dict(
            metavar="led-gpio-mapping",
            type=str,
            help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm, choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'] Default: {}".format(DEFAULT_GPIO) ,
            default=DEFAULT_GPIO,
        ),
    ),
(
    "--led-scan-mode",
    dict(
        metavar="led-scan-mode",
        type=int,
        help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default: {})".format(DEFAULT_SCAN),
        default=DEFAULT_SCAN,
    ),
),
(
    "--led-pwm-lsb-nanoseconds",
    dict(
        metavar="led-pwm-lsb-nanoseconds",
        type=int,
        help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: {}".format(DEFAULT_PWM_LSB),
        default=DEFAULT_PWM_LSB,
    ),
),
(
    "--led-show-refresh",
    dict(
        action="store_true",
        help="Shows the current refresh rate of the LED panel.",
    ),
),
(
    "--led-slowdown-gpio",
    dict(
        metavar="led-slowdown-gpio",
        type=int,
        help="Slow down writing to GPIO. Range: 0..4. Default: {}".format(DEFAULT_SLOWDOWN),
        default=DEFAULT_SLOWDOWN,
    ),
),
)
"""
        
        self.parser.add_argument("--led-no-hardware-pulse", action="store", help
="Don't use hardware pin-pulse generation")
        self.parser.add_argument("--led-rgb-sequence", action="store", help="Swi
tch if your matrix has led colors swapped. Default: RGB", default="RGB", type=st
r)
        self.parser.add_argument("--led-pixel-mapper", action="store", help="App
ly pixel mappers. e.g \"Rotate:90\"", default="", type=str)
        self.parser.add_argument("--led-row-addr-type", action="store", help="0
= default; 1=AB-addressed panels;2=row direct", default=0, type=int, choices=[0,
1,2])
        self.parser.add_argument("--led-multiplexing", action="store", help="Mul
tiplexing type: 0=direct; 1=strip; 2=checker; 3=spiral; 4=ZStripe; 5=ZnMirrorZSt
ripe; 6=coreman; 7=Kaler2Scan; 8=ZStripeUneven (Default: 0)", default=0, type=in
t)"""

BASE_ARGS = (
    (
        "--host",
        dict(
            metavar="HOST",
            help="MinKNOW server host (default: {})".format(DEFAULT_SERVER_HOST),
            default=DEFAULT_SERVER_HOST,
        ),
    ),


    (
        "--log-level",
        dict(
            metavar="LOG-LEVEL",
            action="store",
            default=DEFAULT_LOG_LEVEL,
            choices=LOG_LEVELS,
            help="One of: {}".format(nice_join(LOG_LEVELS)),
        ),
    ),
    (
        "--log-format",
        dict(
            metavar="LOG-FORMAT",
            action="store",
            default=DEFAULT_LOG_FORMAT,
            help="A standard Python logging format string (default: {!r})".format(
                DEFAULT_LOG_FORMAT.replace("%", "%%")
            ),
        ),
    ),
    (
        "--log-file",
        dict(
            metavar="LOG-FILE",
            action="store",
            default=None,
            help="A filename to write logs to, or None to write to the standard stream (default: None)",
        ),
    ),
)


def get_parser(extra_args=None, file=None, default_args=None):
    """Generic argument parser for Read Until scripts

    Parameters
    ----------
    extra_args : Tuple[Tuple[str, dict], ...]
        Extra arguments to append onto the base arguments
    file : str
        Optional. __file__ from the python script, used for program string
    default_args : Tuple[Tuple[str, dict], ...]
        Arguments that form the base requirements for all Read Until scripts

    Returns
    -------
    parser : argparse.ArgumentParser
        The argparse parser, used for raising parser errors manually
    arguments : argparse.ArgumentParser().parse_args()
        The parsed arguments
    """
    if default_args is None:
        args = BASE_ARGS
    else:
        args = default_args

    if extra_args is not None:
        args = args + extra_args

    args = args + LIGHTS_ARGS

    if file is None:
        prog_string = "minLights API: {}".format(sys.argv[0].split("/")[-1])
    else:
        prog_string = "minLights     API: {} ({})".format(sys.argv[0].split("/")[-1], file)

    parser = argparse.ArgumentParser(prog_string)
    for arg in args:
        flags = arg[0]
        if not isinstance(flags, tuple):
            flags = (flags,)
        parser.add_argument(*flags, **arg[1])

    return parser, parser.parse_args()
