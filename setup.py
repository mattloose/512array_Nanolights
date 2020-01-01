from setuptools import setup, find_packages
from os import path

PKG_NAME = "minLights"

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md")) as fh, open(path.join(here, "requirements.txt")) as req:
    long_description = fh.read()
    install_requires = [pkg.strip() for pkg in req]

exec(open("{}/version.py".format(PKG_NAME)).read())

setup(
    name=PKG_NAME,
    version=__version__,
    author="Matt Loose",
    author_email="matt.loose@nottingham.ac.uk",
    description="Python3 implementation of minLights",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nanoporetech",
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    entry_points={
        "console_scripts": [
            "minLights={}.minLights:main".format(PKG_NAME),
            #"ru3_alex={}.alex:main".format(PKG_NAME),
            #"ru3_generators={}.alex_refactor:main".format(PKG_NAME),
            #"ru3_raw_signal_log={}.get_raw_len:main".format(PKG_NAME),
            #"ru3_iteralign={}.iteralign:main".format(PKG_NAME),
            #"ru3_iteralign_centrifuge={}.iteralign_centrifuge:main".format(PKG_NAME),
            #"ru3_unblock_all={}.unblock_all:main".format(PKG_NAME),
        ],
    },
    install_requires=install_requires
)
