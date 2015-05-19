#!/bin/bash
#author dragonriver

bin=`dirname "$0"`
bin=`cd "$bin"; pwd`

. "$bin"/env.sh

start_log=~/webdata/logs/malinger_offline/malinger_runtime.log

start(){
    echo "start servicing..."
    nohup $PYTHON $CURDIR/../src/server/malinger.py >> $start_log 2>&1 &
}

stop(){
    echo "stopping service..."
    for pid in `ps aux | grep -v "grep" | grep "malinger.py" | grep $bin | awk '{print $2}'`
    do
        if kill -0 $pid > /dev/null 2>&1; then
            kill $pid
        fi
    done
}

restart() {
    stop
    start
}

case "$1" in
    start|stop|restart)
        $1
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart}"
        exit 2
esac