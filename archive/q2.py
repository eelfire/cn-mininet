from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import argparse

class CustomTopology( Topo ):
    def build(self, loss=0):
        sa = self.addSwitch('s1')
        sb = self.addSwitch('s2')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        self.addLink(h1, sa)
        self.addLink(h2, sa)
        self.addLink(h3, sb)
        self.addLink(h4, sb)

        self.addLink(sa, sb, loss=loss)


def run( loss=0 ):
    topo = CustomTopology( loss=loss )
    net = Mininet(topo=topo, waitConnected=True, host=CPULimitedHost, link=TCLink)
    net.start()

    CLI(net)

    net.stop()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mininet Custom Topology')
    parser.add_argument('--link-loss', type=int, default=0, help='Specify link loss percentage')

    args = parser.parse_args()

    setLogLevel('info')
    run(loss=args.link_loss)
    