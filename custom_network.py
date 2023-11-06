#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.link import TCLink
from linuxrouter import LinuxRouter
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class CustomTopology( Topo ):
    def build(self, **_opts):
        # add routers
        ra = self.addNode('ra', cls=LinuxRouter, ip='10.0.1.1/24')
        rb = self.addNode('rb', cls=LinuxRouter, ip='10.0.2.1/24')
        rc = self.addNode('rc', cls=LinuxRouter, ip='10.0.3.1/24')

        # add switches
        sa = self.addSwitch('s1')
        sb = self.addSwitch('s2')
        sc = self.addSwitch('s3')

        # add hosts
        h1 = self.addHost('h1', ip='10.0.1.10/24', defaultRoute='via 10.0.1.1')
        h2 = self.addHost('h2', ip='10.0.1.20/24', defaultRoute='via 10.0.1.1')
        h3 = self.addHost('h3', ip='10.0.2.10/24', defaultRoute='via 10.0.2.1')
        h4 = self.addHost('h4', ip='10.0.2.20/24', defaultRoute='via 10.0.2.1')
        h5 = self.addHost('h5', ip='10.0.3.10/24', defaultRoute='via 10.0.3.1')
        h6 = self.addHost('h6', ip='10.0.3.20/24', defaultRoute='via 10.0.3.1')

        # add links 
        self.addLink(h1, sa, intfName1='h-eth1')
        self.addLink(h2, sa, intfName1='h-eth2')
        self.addLink(h3, sb, intfName1='h-eth1')
        self.addLink(h4, sb, intfName1='h-eth2')
        self.addLink(h5, sc, intfName1='h-eth1')
        self.addLink(h6, sc, intfName1='h-eth2')

        self.addLink(sa, ra, intfName1='sa-etha', intfName2='ra-etha')
        self.addLink(sb, rb, intfName1='sb-ethb', intfName2='rb-ethb')
        self.addLink(sc, rc, intfName1='sc-ethc', intfName2='rc-ethc')

        self.addLink(ra, rb, intfName1='ra-ethb', intfName2='rb-etha')
        self.addLink(rb, rc, intfName1='rb-ethc', intfName2='rc-ethb')
        self.addLink(rc, ra, intfName1='rc-etha', intfName2='ra-ethc')

def run():
    topo = CustomTopology()
    net = Mininet(topo=topo, waitConnected=True)
    net.start()
    info('*** Routing Table on Router:\n')
    info(net['ra'].cmd('route'))
    info(net['rb'].cmd('route'))
    info(net['rc'].cmd('route'))
    CLI(net)
    
    net.stop()
    
if __name__ == '__main__':
    setLogLevel('info')
    run()
