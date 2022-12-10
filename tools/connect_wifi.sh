#!/bin/bash

sudo nmcli device wifi connect $1 password $2 ifname wlan0