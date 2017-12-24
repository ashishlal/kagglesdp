#!/usr/bin/env python3

import argparse, csv, sys

sys.path.insert(0, '..')

from common import *
from tqdm import tqdm

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--nr_bins', type=int, default=int(1e+6))
parser.add_argument('-t', '--threshold', type=int, default=int(10))
parser.add_argument('csv_path', type=str)
parser.add_argument('gbdt_path', type=str)
parser.add_argument('out_path', type=str)
args = vars(parser.parse_args())

def gen_hashed_fm_feats(feats, nr_bins):
    feats = ['{0}:{1}:1'.format(field-1, hashstr(feat, nr_bins)) for (field, feat) in feats]
    return feats

frequent_feats = read_freqent_feats(args['threshold'])

with open(args['out_path'], 'w') as f:
    print('writing ffm..\n')
    for row, line_gbdt in tqdm(zip(csv.DictReader(open(args['csv_path'])), open(args['gbdt_path']))):
        y = '0'
        label='target'
        if label in row:
             y = row[label]
             del row[label]

        feats = []

        for feat in gen_feats2(row):
            print(feat)
            field = feat.split('-')[0]
            print(field)
            t, field = field[0], int(field[1:])
            if t == 'C' and feat not in frequent_feats:
                feat = feat.split('-')[0]+'less'
            if t == 'C':
                field += 13
            feats.append((field, feat))

        for i, feat in enumerate(line_gbdt.strip().split()[1:], start=1):
            field = i + 39
            feats.append((field, str(i)+":"+feat))

        feats = gen_hashed_fm_feats(feats, args['nr_bins'])
        # f.write(row['Label'] + ' ' + ' '.join(feats) + '\n')
        f.write(y + ' ' + ' '.join(feats) + '\n')
