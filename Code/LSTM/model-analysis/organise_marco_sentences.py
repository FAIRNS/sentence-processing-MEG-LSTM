import argparse
from functions import annotated_data

parser = argparse.ArgumentParser()

parser.add_argument('data', help='Input data to create dictionaries for')
parser.add_argument('out', help='File to write data object to')

args = parser.parse_args()

corpus_dict = annotated_data.Data()

corpus_dict.add_corpus(args.data)
filtered = corpus_dict.filter(elements=range(1,5), n=2, set_as_attr=True)
# corpus_dict.add_activation_data()

corpus_dict.write_data(args.out)



