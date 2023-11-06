from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.link import TCLink

class CustomTopology(Topo):
    def build(self):
        # Create hosts and routers
        h1 = self.addHost('h1', ip='10.0.1.1/24')
        h2 = self.addHost('h2', ip='10.0.1.2/24')
        h3 = self.addHost('h3', ip='10.0.2.1/24')
        h4 = self.addHost('h4', ip='10.0.2.2/24')
        h5 = self.addHost('h5', ip='10.0.3.1/24')
        h6 = self.addHost('h6', ip='10.0.3.2/24')

        ra = self.addHost('ra')
        rb = self.addHost('rb')
        rc = self.addHost('rc')

        # Create switches with canonical names
        sa = self.addSwitch('s1')
        sb = self.addSwitch('s2')
        sc = self.addSwitch('s3')

        # Connect hosts to routers
        self.addLink(h1, sa)
        self.addLink(h2, sa)
        self.addLink(h3, sb)
        self.addLink(h4, sb)
        self.addLink(h5, sc)
        self.addLink(h6, sc)

        # Connect routers to switches
        self.addLink(sa, ra)
        self.addLink(sb, rb)
        self.addLink(sc, rc)

def create_custom_topology():
    topo = CustomTopology()
    net = Mininet(topo=topo, host=Host, link=TCLink)
    net.start()
    
    # Ensure all hosts are able to send packets to every other host
    net.pingAll()
    
    # You can add additional test commands here
    
    net.stop()

if __name__ == '__main__':
    create_custom_topology()
