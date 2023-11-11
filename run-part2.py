import os

for config in ['b', 'c', 'd']:
    for congestion in ['vegas', 'reno', 'cubic', 'bbr']:
        if config == 'd':
            for link_loss in [1, 3]:
                print(f"Running mininet-tcp.py with config {config} and congestion {congestion} and link_loss {link_loss}")
                mininet_tcp_cmd = f'sudo python3 mininet-tcp.py --config {config} --congestion {congestion} --link-loss {link_loss}'
                os.system(mininet_tcp_cmd)

        else:
            print(f"Running mininet-tcp.py with config {config} and congestion {congestion}")
            mininet_tcp_cmd = f'sudo python3 mininet-tcp.py --config {config} --congestion {congestion} --link-loss 0'
            os.system(mininet_tcp_cmd)
