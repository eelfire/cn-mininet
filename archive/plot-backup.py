import sys
import re
from matplotlib import lines
import matplotlib.pyplot as plt

# Sample iperf data
# iperf_data = """
# [  3] 0.0000-0.5000 sec  3.31 GBytes  56.9 Gbits/sec  27140/0          0     4284K/49 us  145195676.73
# [  3] 0.5000-1.0000 sec  3.60 GBytes  61.8 Gbits/sec  29462/0          0     4284K/18 us  429071473.78
# [  3] 1.0000-1.5000 sec  4.11 GBytes  70.7 Gbits/sec  33696/0          0     4924K/20 us  441660211.20
# [  3] 1.5000-2.0000 sec  4.01 GBytes  68.9 Gbits/sec  32864/0          0     4924K/14 us  615364315.43
# [  3] 2.0000-2.5000 sec  3.89 GBytes  66.8 Gbits/sec  31837/0          0     4924K/18 us  463659918.22
# [  3] 2.5000-3.0000 sec  3.87 GBytes  66.5 Gbits/sec  31706/0          0     4924K/21 us  395787507.81
# [  3] 3.0000-3.5000 sec  4.10 GBytes  70.4 Gbits/sec  33576/0          0     4924K/42 us  209565403.43
# [  3] 3.5000-4.0000 sec  3.52 GBytes  60.5 Gbits/sec  28868/0          0     4924K/18 us  420420721.78
# [  3] 4.0000-4.5000 sec  3.77 GBytes  64.8 Gbits/sec  30904/0          0     4924K/19 us  426384114.53
# [  3] 4.5000-5.0000 sec  3.75 GBytes  64.5 Gbits/sec  30739/0          0     5435K/50 us  161160888.32
# [  3] 5.0000-5.5000 sec  3.84 GBytes  66.0 Gbits/sec  31467/0          0     5435K/27 us  305514268.44
# [  3] 5.5000-6.0000 sec  4.02 GBytes  69.1 Gbits/sec  32972/0          0     5435K/17 us  508435998.12
# [  3] 6.0000-6.5000 sec  3.57 GBytes  61.4 Gbits/sec  29270/0          0     5435K/49 us  156590915.92
# [  3] 6.5000-7.0000 sec  3.62 GBytes  62.2 Gbits/sec  29662/0          0     5435K/19 us  409248175.16
# [  3] 7.0000-7.5000 sec  4.06 GBytes  69.7 Gbits/sec  33235/0          0     8313K/21 us  414874087.62
# [  3] 7.5000-8.0000 sec  3.99 GBytes  68.6 Gbits/sec  32725/0          0     8313K/15 us  571910826.67
# [  3] 8.0000-8.5000 sec  3.85 GBytes  66.1 Gbits/sec  31534/0          0     8313K/20 us  413322444.80
# [  3] 8.5000-9.0000 sec  3.89 GBytes  66.9 Gbits/sec  31890/0          0     8313K/18 us  464431786.67
# [  3] 9.0000-9.5000 sec  4.65 GBytes  80.0 Gbits/sec  38132/0          0     8313K/24 us  416503125.33
# [  3] 9.5000-10.0000 sec  4.27 GBytes  73.4 Gbits/sec  35019/0          0     8313K/19 us  483158986.11
# """

# get file name from argument
if len(sys.argv) != 2:
    print("Usage: python plot.py <filename>")
    exit()
filename = sys.argv[1]

# get data from file without last line
with open(filename, 'r') as f:
    all_lines = f.read()

selected_lines = all_lines[7:-1]
iperf_data = ''.join(selected_lines)

def parse_iperf_data(data):
    time_bandwidth = []
    pattern = re.compile(r'\[ *\d+ *\] (\d+\.\d+)-(\d+\.\d+) sec +(\d+\.\d+) GBytes +(\d+\.\d+) Gbits/sec *')
    
    for line in data.split('\n'):
        match = pattern.search(line)
        print(line)
        if match:
            start_time, end_time, data_transfer, bandwidth = map(float, match.groups()[0:4])
            # time_bandwidth.append((start_time, bandwidth))
            time_bandwidth.append((end_time, bandwidth))
    
    return time_bandwidth

def plot_bandwidth_vs_time(data):
    times, bandwidths = zip(*data)
    # plt.plot(times, bandwidths, marker='o', linestyle='-', color='b')s
    plt.plot(times, bandwidths, marker='o')
    plt.title('Bandwidth vs. Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Bandwidth (Gbits/sec)')
    plt.grid(True)
    # plt.show()
    # plot to pdf
    plt.savefig('plot.pdf')

# Parse and plot iperf data
print(iperf_data)
iperf_parsed_data = parse_iperf_data(iperf_data)
print(iperf_parsed_data)
plot_bandwidth_vs_time(iperf_parsed_data)