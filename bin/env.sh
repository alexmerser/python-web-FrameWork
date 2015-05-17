#!/bin/bash
# encoding: utf-8

# ${BASH_SOURCE[0]} get the bash file name
CURDIR="$( cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"

export PROJECT_HOME=$CURDIR
export CURUSER=`whoami | awk '{print $1}'`
export LOGS=/home/$CURUSER/webdata/logs/project-name
export CONF=$PROJECT_HOME/conf
export LIB=$PROJECT_HOME/lib
export SRC=$PROJECT_HOME/src

#export python path
export PYTHONPATH=$LIB:$LIB/cloghandler:$SRC
export PYTHON=/usr/bin/python
export DATE=`date + "%Y-%m-%d"`
