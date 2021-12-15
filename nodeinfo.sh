#!/bin/bash

nodename=$(hostname -s)
wmac=$(ifconfig wlp2s0 | grep ether | awk '{print $2}')
batip=$(ifconfig bat0 | grep "inet " | awk '{print $2}')
batmac=$(ifconfig bat0 | grep "ether" | awk '{print $2}')

echo -n "{'name'"':'"'"$nodename"'","'wmac'"':'"'"$wmac"'","'bmac'"':'"'"$batmac"'","'ip'"':'"'"$batip"'""}" > nodeinfo
cat nodeinfo

while true; do
cat nodeinfo | alfred -s 64
sleep 1000;
done

