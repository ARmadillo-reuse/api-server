PID=`cat smtp/pid`
kill $PID
./manage.py startclient &
echo $! > smtp/pid
true
