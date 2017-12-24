
# coding: utf-8

# In[2]:

import argparse, csv, sys, collections
import os
sys.path.append('..')

from common import *
from tqdm import tqdm


# In[ ]:


if len(sys.argv) == 1:
    sys.argv.append('-h')


# In[ ]:

# parser = argparse.ArgumentParser()
# parser.add_argument('csv_path', type=str)
# args = vars(parser.parse_args())


# In[ ]:

counts = collections.defaultdict(lambda : [0, 0, 0])

def count_values_in_row(csv_path):
    for i, row in tqdm(enumerate(csv.DictReader(open(csv_path)), start=2)):
#         print(row)
        label = row['target']
        for j in f_cats:
            field = j
            value = row[field]
            if label == '0':
                counts[field+','+value][0] += 1
            else:
                counts[field+','+value][1] += 1
            counts[field+','+value][2] += 1
        if i % 1000000 == 0:
            sys.stderr.write('{0}m\n'.format(int(i/1000000)))


# In[ ]:

def print_results(dest_csv):
    fp = open(dest_csv, 'w')
    fp.write('Field,Value,Neg,Pos,Total,Ratio\n')
    for key, (neg, pos, total) in sorted(counts.items(), key=lambda x: x[1][2]):
        if total < 10:
            continue
        ratio = round(float(pos)/total, 5)
        counts_str = key+','+str(neg)+','+str(pos)+','+str(total)+','+str(ratio) + '\n'
        fp.write(counts_str)
    fp.close()


# In[ ]:

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_csv_path', required=True, type=str, help='Train CSV File Path')
    parser.add_argument('--dest_csv_path', required=True, type=str, help='Dest CSV File Path')
    
    args = parser.parse_args()

    print(args)

    count_values_in_row(args.src_csv_path)
    delete_file_if_exists(args.dest_csv_path)
    print_results(args.dest_csv_path)

