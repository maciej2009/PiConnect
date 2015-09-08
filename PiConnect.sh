sudo cp /home/pi/projects/PiConnect/PiConnect.py /usr/local/sbin/
sudo nano /etc/init.d/PiConnect
sudo chmod 755 /etc/init.d/PiConnect
sudo update-rc.d PiConnect defaults



#! /bin/sh
# /etc/init.d/skrypt
 
### BEGIN INIT INFO
# Provides:          PiConnect
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: PiConnect
# Description:       PiConnect
### END INIT INFO

case "$1" in
  start)
    echo "Starting skrypt"
    # run application you want to start
    python /usr/local/sbin/PiConnect.py &
    ;;
  stop)
    echo "Stopping skrypt"
    # kill application you want to stop
    killall python
    ;;
  *)
    echo "Usage: /etc/init.d/PiConnect{start|stop}"
    exit 1
    ;;
esac
 
exit 0








