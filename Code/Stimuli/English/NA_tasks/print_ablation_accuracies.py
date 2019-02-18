import sys
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--base_perf', type=float,
                    help='performance of the unablated model')
parser.add_argument('--ratio', type=float, default=0.9,
                    help='ratio of baseline performance under which to consider the ablated unit')
args = parser.parse_args()

if __name__ == "__main__":
    for line in sys.stdin:
        elements = line.split()
        if float(elements[3]) < (args.base_perf * args.ratio):
        	sys.stdout.write("\t" + elements[0] + "\t" + elements[3] + "\n")





