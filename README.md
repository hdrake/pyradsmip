PyRADSMIP: comparing python-wrapped radiation codes
==============================
[![Build Status](https://travis-ci.com/hdrake/pyradsmip.svg?branch=master)](https://travis-ci.com/hdrake/pyradsmip)
[![codecov](https://codecov.io/gh/hdrake/pyradsmip/branch/master/graph/badge.svg)](https://codecov.io/gh/hdrake/pyradsmip)
[![License:MIT](https://img.shields.io/badge/License-MIT-lightgray.svg?style=flt-square)](https://opensource.org/licenses/MIT)

# Installation

We recommend using [`anaconda`](https://www.anaconda.com/distribution/) to handle `python` dependencies behind the scenes. With `anaconda` installed, simply create an environment with the necessary `python` modules based on the `environment.yml` file with:

`conda env create -f environment.yml`

The newly created conda environment `pyradsmip` can be activated with:

`source activate pyradsmip`

# Radiation codes supported

## RRTMG

The correlated-k code RRTMG is wrapped in Python via [`climlab`](https://github.com/brian-rose/climlab). `climlab` is included in the conda environment file `environment.yml`.

## PyRADS

The line-by-line module PyRADS needs to be installed manually (see [github page](https://github.com/ddbkoll/PyRADS)) and the path to import it into `pyradsmip` has to be updated in `pyradsmip/__init__.py`.

--------

<p><small>Project based on the <a target="_blank" href="https://github.com/jbusecke/cookiecutter-science-project">cookiecutter science project template</a>.</small></p>
