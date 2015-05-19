#!/bin/bash

CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export MALINGER_HOME=$CURDIR/..

export CURUSER=`whoami |awk '{print $1}'`
export LOGS=/home/$CURUSER/webdata/logs/malinger
export CONF=$MALINGER_HOME/conf
export LIB=$MALINGER_HOME/lib
export SRC=$MALINGER_HOME/src
export SERVER=$SRC/server

# export python path
export PYTHONPATH=$LIB:$LIB/cloghandler:$SRC
export PYTHON=/usr/bin/python
export DATE=`date +"%Y-%m-%d"`
