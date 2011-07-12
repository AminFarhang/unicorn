#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Gabriel Brammer on 2011-05-18.

$URL$
$Author$
$Date$

"""
__version__ = "$Rev$"

import prepare
import reduce
import candels
import analysis
import go_3dhst
import galfit
import catalogs

from socket import gethostname as hostname

if hostname().startswith('uni'):
    GRISM_HOME = '/3DHST/Spectra/Work/'
else:
    GRISM_HOME = '/research/HST/GRISM/3DHST/'

