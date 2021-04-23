#!/bin/sh

APP_NAME=mologov
JAR_NAME=$APP_NAME
PID=$APP_NAME\.pid

usage() {
    echo "Usage: sh monit.sh [start|startBySW|stop|restart|status]"
    echo "	start "
    echo "	stop "
    echo "	restart "
    echo "	status "
    exit 1
}

# check existence
is_exist(){
  pid=`ps -ef|grep $JAR_NAME|grep -v grep|awk '{print $2}' `
  # none 1，exists 0
  if [ -z "${pid}" ]; then
   return 1
  else
    return 0
  fi
}

start(){
  is_exist
  if [ $? -eq "0" ]; then 
    echo ">>> ${APP_NAME} is already running PID=${pid} <<<" 
  else 
    nohup ./mologov -f init.yml > $APP_NAME\.log 2>&1 &
    echo $! > $PID
    echo ">>> start $APP_NAME successed PID=$!          <<<"
   fi
  }


stop(){
  #is_exist
  pidf=$(cat $PID)
  #echo "$pidf"  
  echo ">>> ${APP_NAME} PID = $pidf begin kill $pidf    <<<"
  kill $pidf
  rm -rf $PID
  sleep 2
  is_exist
  if [ $? -eq "0" ]; then 
    echo ">>> $APP_NAME 2 PID = $pid begin kill -9 $pid  <<<"
    kill -9  $pid
    sleep 2
    echo ">>> $APP_NAME process stopped                  <<<"
  else
    echo ">>> $APP_NAME is not running                   <<<"
  fi  
}

status(){
  is_exist
  if [ $? -eq "0" ]; then
    echo ">>> ${APP_NAME} is running PID is ${pid} <<<"
  else
    echo ">>> $APP_NAME is not running             <<<"
  fi
}

restart(){
  stop
  start
}

case "$1" in
  "start")
    start
    ;;
  "stop")
    stop
    ;;
  "status")
    status
    ;;
  "restart")
    restart
    ;;
  *)
    usage
    ;;
esac
exit 0
