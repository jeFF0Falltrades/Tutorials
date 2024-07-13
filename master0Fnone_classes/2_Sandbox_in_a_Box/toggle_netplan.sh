#!/usr/bin/env bash
#
# Author: jeFF0Falltrades
#
# toggle_netplan.sh automates the process of swapping the netplan configuration
# of our "Sandbox in a Box" Remnux machine so that you can swap between the
# configuration used to run upgrades/updates, and the configuration used to
# route the machine for use in the internal (virtual) network.
#
# REMEMBER: Run this as sudo, and remember to switch your VM network as well
#
# MIT License
#
# Copyright (c) 2024 Jeff Archer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
if [ "$EUID" -ne 0 ]; then
  echo "This script must be run as root."
  exit 1
fi

NETPLAN_CONFIG="/etc/netplan/01-netcfg.yaml"

enable_internet=$(cat <<'EOF'
# This file describes the network interfaces available on your system
# For more information, see netplan(5).
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s17:
        dhcp4: yes
        nameservers:
            addresses: [8.8.8.8]
EOF
)

disable_internet=$(cat <<'EOF'
# This file describes the network interfaces available on your system
# For more information, see netplan(5).
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s17:
        dhcp4: no
        addresses: [10.10.10.3/29]
        gateway4: 10.10.10.3
EOF
)

if grep -q "dhcp4: yes" "/etc/netplan/01-netcfg.yaml"; then
    echo "$disable_internet" > "$NETPLAN_CONFIG"
    echo "Swapped to internal network configuration"
else
    echo "$enable_internet" > "$NETPLAN_CONFIG"
    echo "Swapped to NAT configuration"
fi

netplan apply
