# Routing and Congestion Control using Mininet

## Introduction
CS 433 Computer Networks (2023-24): ***Assignment 2***

Team Members:
- Naman Dharmani:	21110136
- Tirth Patel:		21110225

## Part I
File: `custom_network.py`
```bash
# Usage:
sudo python3 custom_network.py [0|1] # 0 for short path (h1 -> ra -> rc -> h6), 1 for long path (h1 -> ra -> rb -> rc -> h6)
```


## Part II
File: `mininet-tcp.py`
```bash
# Usage:
# sudo python3 mininet-tcp.py [-h] --config {b,c,d} [--congestion CONGESTION] [--link-loss LINK_LOSS]

# Example usage:
sudo python3 mininet-tcp.py --config b --link-loss 3 --congestion vegas
```

---
**_NOTE:_**
```
mininet version: 2.3.0
python 3
openvswitch-testcontroller as default controller of mininet
iperf version 2.0.13 (21 Jan 2019) pthreads
```
---