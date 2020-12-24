#!/usr/bin/env python
import os

import setuptools

os.environ['PBR_VERSION'] = "0.0.4"
setuptools.setup(setup_requires=["pbr"], pbr=True)
