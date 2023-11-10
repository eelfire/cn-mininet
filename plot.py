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
def plot_csv(config):
    # times = [data_point['start_time'] for data_point in data]
    csv_files = [f'csv/{config}-{int(link_loss)}-{congestion}.csv' for link_loss in [0] for congestion in ['vegas', 'reno', 'cubic', 'bbr']]
    plt.figure(figsize=(8,5))

    for csv_file in csv_files:
        data = parse_csv(csv_file)
        times = [data_point['end_time'] for data_point in data]
        bandwidths = [data_point['bandwidth']/1e9 for data_point in data]
        label = csv_file.split('.')[0].split('-')[2]

        plt.plot(times, bandwidths, marker='o', label=label)

    plt.title('Bandwidth vs. Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Bandwidth (Gbits/sec)')
    plt.grid(True, linestyle='--')
    plt.legend()
    # plt.show()
    plt.savefig(f'pdf/b.pdf')


plot_csv(sys.argv[1])