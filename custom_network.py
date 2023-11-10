#!/usr/bin/env python

"""
    Inspiration from the following sources:
    https://github.com/mininet/mininet/blob/master/examples/linuxrouter.py
    https://stackoverflow.com/questions/46595423/mininet-how-to-create-a-topology-with-two-routers-and-their-respective-hosts
"""

import sys
from time import sleep
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class CustomTopology(Topo):
    def build(self, **_opts):
        # add routers
        ra = self.addNode('ra', cls=LinuxRouter, ip='10.1.0.1/24')
        rb = self.addNode('rb', cls=LinuxRouter, ip='10.2.0.1/24')
        rc = self.addNode('rc', cls=LinuxRouter, ip='10.3.0.1/24')

        # add corresponding switches for each router
        sa = self.addSwitch('s1')
        sb = self.addSwitch('s2')
        sc = self.addSwitch('s3')

        # add hosts & configure their IP
        h1 = self.addHost('h1', ip='10.1.0.10/24', defaultRoute='via 10.1.0.1')
        h2 = self.addHost('h2', ip='10.1.0.20/24', defaultRoute='via 10.1.0.1')
        h3 = self.addHost('h3', ip='10.2.0.10/24', defaultRoute='via 10.2.0.1')
        h4 = self.addHost('h4', ip='10.2.0.20/24', defaultRoute='via 10.2.0.1')
        h5 = self.addHost('h5', ip='10.3.0.10/24', defaultRoute='via 10.3.0.1')
        h6 = self.addHost('h6', ip='10.3.0.20/24', defaultRoute='via 10.3.0.1')

        # add links
        self.addLink(h1, sa)
        self.addLink(h2, sa)
        self.addLink(h3, sb)
        self.addLink(h4, sb)
        self.addLink(h5, sc)
        self.addLink(h6, sc)

        self.addLink(sa, ra, intfName2='ra-ethsa',
                     param2={'ip': '10.1.0.1/24'})
        self.addLink(sb, rb, intfName2='rb-ethsb',
                     param2={'ip': '10.2.0.1/24'})
        self.addLink(sc, rc, intfName2='rc-ethsc',
                     param2={'ip': '10.3.0.1/24'})

        self.addLink(ra, rb, intfName1='ra-ethb', intfName2='rb-etha',
                     params1={'ip': '10.100.12.1/24'}, params2={'ip': '10.100.12.2/24'})
        self.addLink(rb, rc, intfName1='rb-ethc', intfName2='rc-ethb',
                     params1={'ip': '10.100.23.2/24'}, params2={'ip': '10.100.23.3/24'})
        self.addLink(rc, ra, intfName1='rc-etha', intfName2='ra-ethc',
                     params1={'ip': '10.100.31.3/24'}, params2={'ip': '10.100.31.1/24'})


def run(is_long_path=0):
    topo = CustomTopology()
    net = Mininet(topo=topo, waitConnected=True)
    net.start()

    # add routes for reaching networks that aren't directly connected
    info(net['ra'].cmd('ip route add 10.2.0.0/24 via 10.100.12.2 dev ra-ethb'))
    info(net['rb'].cmd('ip route add 10.1.0.0/24 via 10.100.12.1 dev rb-etha'))
    info(net['rb'].cmd('ip route add 10.3.0.0/24 via 10.100.23.3 dev rb-ethc'))
    info(net['rc'].cmd('ip route add 10.2.0.0/24 via 10.100.23.2 dev rc-ethb'))

    if not is_long_path:
        info(net['ra'].cmd('ip route add 10.3.0.0/24 via 10.100.31.3 dev ra-ethc'))
        info(net['rc'].cmd('ip route add 10.1.0.0/24 via 10.100.31.1 dev rc-etha'))
    else:
        info(net['ra'].cmd('ip route add 10.3.0.0/24 via 10.100.12.2 dev ra-ethb'))
        info(net['rc'].cmd('ip route add 10.1.0.0/24 via 10.100.23.2 dev rc-ethb'))

    print('--- Routes on ra: ---')
    info(net['ra'].cmd('ip route show | column -t | tee ra_routes.txt'))
    print('--- Routes on rb: ---')
    info(net['rb'].cmd('ip route show | column -t | tee rb_routes.txt'))
    print('--- Routes on rc: ---')
    info(net['rc'].cmd('ip route show | column -t | tee rc_routes.txt'))

    if not is_long_path:
        print('--- --- ---\n')
        info('--- Starting tcpdump on ra, rb, rc ---\n')
        ra_pcap = net['ra'].popen('tcpdump -i any -w ra_capture.pcap')
        rb_pcap = net['rb'].popen('tcpdump -i any -w rb_capture.pcap')
        rc_pcap = net['rc'].popen('tcpdump -i any -w rc_capture.pcap')
        sleep(1)

        info('--- Running pingAll() ---\n')
        net.pingAll()
        sleep(1)

        ra_pcap.terminate()
        rb_pcap.terminate()
        rc_pcap.terminate()

        print('--- --- ---\n')
        print('*** h1 -> ra -> rc -> h6')
    else:
        print('--- --- ---\n')
        print('*** h1 -> ra -> rb -> rc -> h6')

    # ping h1 -> h6
    print('ping h1 -> h6 for 10 counts')
    info(net['h1'].cmd('ping -c 10 10.3.0.20'))

    # iperf h1 h6
    print('--- --- ---\n')
    print('iperf h1 -> h6 for 10 seconds')
    net['h6'].cmd('iperf -s &')
    sleep(1)
    info(net['h1'].cmd('iperf -c 10.3.0.20 -t 10'))
    net['h6'].cmd('kill %iperf')

    print('--- --- ---\n')

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    # 0 for short path (h1 -> ra -> rc -> h6), 1 for long path (h1 -> ra -> rb -> rc -> h6)
    is_long_path = 0
    if len(sys.argv) > 1:
        is_long_path = int(sys.argv[1])
    run(is_long_path)
