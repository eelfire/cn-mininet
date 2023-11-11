from os import link
import matplotlib.pyplot as plt
import csv
import sys

def parse_csv(filename):
    with open(filename, 'r') as f:
        csv_data = f.read()
    parsed_data = []
    csv_reader = csv.reader(csv_data.strip().splitlines()[:-1])

    for row in csv_reader:
        # print(row)
        time = str(row[-3])
        end_time = time.split('-')[1]
        transfer_size = int(row[-2])
        bandwidth = int(row[-1])

        parsed_data.append({
            'time': time,
            'end_time': end_time,
            'transfer_size': transfer_size,
            'bandwidth': bandwidth
        })

    # for data in parsed_data:
    #     print(data)
    
    return parsed_data


# Plot the bandwidth vs. time graph
def plot_csv(config, host, link_loss):
    # times = [data_point['start_time'] for data_point in data]
    csv_files = [f'csv/{host}-{config}-{link_loss}-{congestion}.csv' for congestion in ['vegas', 'reno', 'cubic', 'bbr']]
    plt.figure(figsize=(8,5))

    for csv_file in csv_files:
        data = parse_csv(csv_file)
        times = [data_point['end_time'] for data_point in data]
        bandwidths = [data_point['bandwidth']/1e6 for data_point in data]
        label = csv_file.split('.')[0].split('-')[3]

        plt.plot(times, bandwidths, marker='o', label=label)

    plt.title('Bandwidth vs. Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Bandwidth (Mbits/sec)')
    plt.grid(True, linestyle='--')
    plt.legend()
    # plt.show()
    plt.savefig(f'pdf/{host}-{config}-{link_loss}.pdf')


if len(sys.argv) < 4:
    print('Usage: python3 plot.py <config>{b,c,d} <host>{h1,h2,h3} <link_loss>{0,1,3}')
    exit(1)

config = sys.argv[1]
host = sys.argv[2]
link_loss = int(sys.argv[3])
plot_csv(config, host, link_loss)