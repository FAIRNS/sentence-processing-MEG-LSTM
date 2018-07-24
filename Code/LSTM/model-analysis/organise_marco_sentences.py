import argparse
from annotated_data import Data

parser = argparse.ArgumentParser()

parser.add_argument('data', help='Input data to create dictionaries for')
parser.add_argument('out', help='File to write data object to')

args = parser.parse_args()

def compute_length(in_data):
    l = len(in_data.split('|')[0].split())
    return l

corpus_dict = Data()

corpus_dict.add_corpus(args.data, length=compute_length)
filtered = corpus_dict.filter(elements=xrange(1,5), n=2, set_as_attr=True)
# corpus_dict.add_activation_data()

corpus_dict.write_data(args.out)



