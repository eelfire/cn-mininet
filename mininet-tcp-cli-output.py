import argparse
from time import sleep

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink

class CustomTopology(Topo):
    def build(self, link_loss=0):
        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)

        self.addLink(s1, s2, loss=link_loss)


def start_iperf_server(host):
    host.cmd('iperf -s &')

def run_iperf_client(client, server, congestion, config, link_loss):
    iperf_cmd = f'sudo iperf -c {server.IP()} --linux-congestion {congestion} -e -i 0.5 -t 10'
    result = client.cmd(iperf_cmd)
    return result

# def tcp_server(host):
#     start_iperf_server(host)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mininet and iPerf Analysis Program")
    parser.add_argument("--config", choices=["b", "c", "d"], required=True, help="Specify 'b', 'c', or 'd'")
    parser.add_argument("--congestion", default="cubic", help="Congestion control scheme (default: cubic)")
    parser.add_argument("--link-loss", type=float, default=0, help="Link loss percentage (default: 0)")

    args = parser.parse_args()

    # Create Mininet topology
    topology = CustomTopology(link_loss=args.link_loss)
    net = Mininet(topo=topology, host=CPULimitedHost, link=TCLink)
    net.start()

    # h1_pcap = net['h1'].popen('tcpdump -i any -w h1.pcap')

    # CLI(net)
    result = None
    start_iperf_server(net.get('h4'))
    sleep(2)

    # Run experiments
    if args.config == "b":
        result = run_iperf_client(net.get('h1'), net.get('h4'), args.congestion, args.config, args.link_loss)

    elif args.config == "c":
        result = run_iperf_client(net.get('h1'), net.get('h4'), args.congestion, args.config, args.link_loss) + '\n' + run_iperf_client(net.get('h2'), net.get('h4'), args.congestion, args.config, args.link_loss) + '\n' + run_iperf_client(net.get('h3'), net.get('h4'), args.congestion, args.config, args.link_loss)

    elif args.config == "d":
        # Configure link loss on s1-s2
        net.link('s1-eth3', 's2-eth2', loss=args.link_loss)
        result = run_iperf_client(net.get('h1'), net.get('h4'), args.congestion, args.config, args.link_loss)

    print(f"Throughput for configuration {args.config} with {args.congestion}:\n{result}")
    
    sleep(1)
    # h1_pcap.terminate()

    # stop iperf server
    net['h4'].cmd('killall iperf')

    # Stop Mininet
    net.stop()
