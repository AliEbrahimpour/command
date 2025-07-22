#!/bin/bash

DEST="$1"
if [ -z "$DEST" ]; then
    echo "Usage: $0 <destination>"
    exit 1
fi

# MTU = payload + 28 bytes (20 IP + 8 ICMP headers)
LOW=1200
HIGH=1500
MAX=0

while [ $LOW -le $HIGH ]; do
    MID=$(( (LOW + HIGH) / 2 ))
    echo -n "Testing payload size $MID... "
    if ping -c 1 -M do -s "$MID" "$DEST" > /dev/null 2>&1; then
        echo "Success"
        MAX=$MID
        LOW=$((MID + 1))
    else
        echo "Fail"
        HIGH=$((MID - 1))
    fi
done

MTU=$((MAX + 28))
echo "✅ Maximum MTU without fragmentation to $DEST is: $MTU bytes (payload: $MAX)"



# exec ./mtu-check.sh 8.8.8.8
