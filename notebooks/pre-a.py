#!/usr/bin/env python3

import argparse, csv, sys
sys.path.insert(0, '..')

from common import *
from tqdm import tqdm

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('csv_path', type=str)
parser.add_argument('dense_path', type=str)
parser.add_argument('sparse_path', type=str)
args = vars(parser.parse_args())

#These features are dense enough (they appear in the dataset more than 4 million times), so we include them in GBDT
# target_cat_feats = ['C9-a73ee510', 'C22-', 'C17-e5ba7672', 'C26-', 'C23-32c7478e', 'C6-7e0ccccf', 'C14-b28479f6', 'C19-21ddcdc9', 'C14-07d13a8f', 'C10-3b08e48b', 'C6-fbad5c96', 'C23-3a171ecb', 'C20-b1252a9d', 'C20-5840adea', 'C6-fe6b92e5', 'C20-a458ea53', 'C14-1adce6ef', 'C25-001f3601', 'C22-ad3062eb', 'C17-07c540c4', 'C6-', 'C23-423fab69', 'C17-d4bb7bd8', 'C2-38a947a1', 'C25-e8b83407', 'C9-7cc72ec2']

target_cat_feats = ['ps_car_01_cat-6', 'ps_car_03_cat-0', 'ps_car_08_cat-0',
       'ps_car_02_cat-0', 'ps_car_06_cat-0', 'ps_car_03_cat-1',
       'ps_car_06_cat-1', 'ps_ind_02_cat-2', 'ps_car_06_cat-11',
       'ps_reg_01_plus_ps_car_02_cat-23', 'ps_car_05_cat-0',
       'ps_reg_01_plus_ps_car_04_cat-90', 'ps_car_05_cat-1',
       'ps_car_01_cat-7', 'ps_car_09_cat-0', 'ps_car_01_cat-11',
       'ps_ind_04_cat-1', 'ps_car_05_cat-', 'ps_ind_04_cat-0',
       'ps_car_09_cat-2', 'ps_car_03_cat-', 'ps_ind_02_cat-1',
       'ps_car_02_cat-1', 'ps_car_08_cat-1', 'ps_car_04_cat-0',
       'ps_ind_05_cat-0', 'ps_car_07_cat-1']

f_nums = ['ps_car_13',
 'ps_reg_03',
 'ps_ind_03',
 'ps_ind_15',
 'ps_reg_02',
 'ps_car_14',
 'ps_car_12',
 'ps_ind_17_bin',
 'ps_reg_01',
 'ps_car_15',
 'ps_ind_01',
 'ps_ind_16_bin',
 'ps_ind_07_bin',
 'ps_ind_06_bin',
 'ps_car_11',
 'ps_calc_09',
 'ps_calc_05',
 'ps_ind_08_bin',
 'ps_ind_09_bin',
 'ps_ind_18_bin',
 'ps_ind_12_bin',
 'ps_ind_14']

f_cats = ['ps_ind_05_cat',
 'ps_car_01_cat',
 'ps_car_07_cat',
 'ps_car_03_cat',
 'ps_car_06_cat',
 'ps_car_04_cat',
 'ps_car_09_cat',
 'ps_car_02_cat',
 'ps_ind_02_cat',
 'ps_car_05_cat',
 'ps_car_08_cat',
 'ps_ind_04_cat',
 'ps_reg_01_plus_ps_car_02_cat',
 'ps_reg_01_plus_ps_car_04_cat']

with open(args['dense_path'], 'w') as f_d, open(args['sparse_path'], 'w') as f_s:
    for row in tqdm(csv.DictReader(open(args['csv_path']))):
        y = '0'
        label='target'
        if label in row:
             y = row[label]
             del row[label]
            
        feats = []
        for j in f_nums:
            val = row[j]
            if val == '':
                val = -10 
            feats.append('{0}'.format(val))
        #f_d.write(row['Label'] + ' ' + ' '.join(feats) + '\n')
        f_d.write(y + ' ' + ' '.join(feats) + '\n')
        
        cat_feats = set()
        for j in f_cats:
            field = j
            key = field + '-' + row[field]
            cat_feats.add(key)

        feats = []
        for j, feat in enumerate(target_cat_feats, start=1):
            if feat in cat_feats:
                feats.append(str(j))
        # f_s.write(row['Label'] + ' ' + ' '.join(feats) + '\n')
        f_s.write(y + ' ' + ' '.join(feats) + '\n')
