python /userdata/RetroFlag/SafeShutdown.py &

(
  sleep 5
  echo '1-2' > /sys/bus/usb/drivers/usb/unbind
  sleep 5
  echo '1-2' > /sys/bus/usb/drivers/usb/bind
) &
