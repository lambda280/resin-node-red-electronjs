#!/bin/bash

FAILED=0

echo "Testing bluetooth on RPI3. Make sure you have a bluetooth device enabled and visible."

echo "Attaching hci0..."
# if ! /usr/bin/hciattach /dev/ttyAMA0 bcm43xx 921600 noflow -; then
#    echo "First try failed. Let's try another time."
#    /usr/bin/hciattach /dev/ttyAMA0 bcm43xx 921600 noflow -
# fi
until /usr/bin/hciattach /dev/ttyAMA0 bcm43xx 921600 noflow -
do
    echo "Initializing bluetooth failed."
    sleep 5
done

echo "Bring hci0 up..."
hciconfig hci0 up

echo "Scan for devices..."
if [ `hcitool scan | wc -l` -le 1 ]; then
    FAILED=1
else
    FAILED=0
fi

echo "Bluetooth bringup finished."

# Test result
if [ $FAILED -eq 1 ]; then
    echo "TEST FAILED"
else
    echo "TEST PASSED"
fi
