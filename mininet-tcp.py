import argparse
import os
from multiprocessing import Process
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

        self.addLink(h1, s1, bw=100)
        self.addLink(h2, s1, bw=100)
        self.addLink(h3, s2, bw=100)
        self.addLink(h4, s2, bw=100)

        self.addLink(s1, s2, loss=link_loss, bw=100)


def start_iperf_server(host):
    host.cmd('iperf -s > iperf.txt &')


def run_iperf_client(client, server, congestion, config, link_loss):
    iperf_cmd = f'sudo iperf -c {server.IP()} --linux-congestion {congestion} -e -i 0.5 -t 10 -y C> csv/{client}-{config}-{int(link_loss)}-{congestion}.csv'
    client.cmd(iperf_cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Mininet and iPerf Analysis Program")
    parser.add_argument(
        "--config", choices=["b", "c", "d"], required=True, help="Specify 'b', 'c', or 'd'")
    parser.add_argument("--congestion", default="cubic",
                        help="Congestion control scheme (default: cubic)")
    parser.add_argument("--link-loss", type=float, default=0,
                        help="Link loss percentage (default: 0)")

    args = parser.parse_args()

    # Create Mininet topology
    topology = CustomTopology(link_loss=args.link_loss)
    net = Mininet(topo=topology, host=CPULimitedHost, link=TCLink)
    net.start()

    os.system('mkdir -p pcap')
    h1_pcap = net['h1'].popen(
        f'tcpdump -i any -w pcap/h1-{args.config}-{int(args.link_loss)}-{args.congestion}.pcap')
    h2_pcap = net['h2'].popen(
        f'tcpdump -i any -w pcap/h2-{args.config}-{int(args.link_loss)}-{args.congestion}.pcap')
    h3_pcap = net['h3'].popen(
        f'tcpdump -i any -w pcap/h3-{args.config}-{int(args.link_loss)}-{args.congestion}.pcap')
    h4_pcap = net['h4'].popen(
        f'tcpdump -i any -w pcap/h4-{args.config}-{int(args.link_loss)}-{args.congestion}.pcap')

    # CLI(net)
    start_iperf_server(net.get('h4'))
    sleep(2)

    print(f"Analysis for configuration {args.config} with {args.congestion}")

    # Run experiments
    if args.config == "b" or args.config == "d":
        run_iperf_client(net.get('h1'), net.get(
            'h4'), args.congestion, args.config, args.link_loss)

    elif args.config == "c":
        # run iperf_client simultaneously on h1, h2, h3
        h1 = Process(target=run_iperf_client, args=(net.get('h1'), net.get(
            'h4'), args.congestion, args.config, args.link_loss))
        h2 = Process(target=run_iperf_client, args=(net.get('h2'), net.get(
            'h4'), args.congestion, args.config, args.link_loss))
        h3 = Process(target=run_iperf_client, args=(net.get('h3'), net.get(
            'h4'), args.congestion, args.config, args.link_loss))
        h1.start()
        h2.start()
        h3.start()
        h1.join()
        h2.join()
        h3.join()

    sleep(2)
    h1_pcap.terminate()
    h2_pcap.terminate()
    h3_pcap.terminate()
    h4_pcap.terminate()

    # stop iperf server
    net['h4'].cmd('killall iperf')

    # Stop Mininet
    net.stop()
