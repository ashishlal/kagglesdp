
# coding: utf-8

# In[ ]:

import hashlib, csv, math, os, pickle, subprocess
import numpy as np
from tqdm import tqdm

# In[ ]:

# HEADER="Id,Label,I1,I2,I3,I4,I5,I6,I7,I8,I9,I10,I11,I12,I13,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,     C14,C15,C16,C17,C18,C19,C20,C21,C22,C23,C24,C25,C26"

HEADER="ps_car_13,ps_reg_03,ps_ind_05_cat,ps_ind_03,ps_ind_15,ps_reg_02,ps_car_14,ps_car_12,ps_car_01_cat,ps_car_07_cat,ps_ind_17_bin,ps_car_03_cat,ps_reg_01,ps_car_15,ps_ind_01,ps_ind_16_bin,ps_ind_07_bin,ps_car_06_cat,ps_car_04_cat,ps_ind_06_bin,ps_car_09_cat,ps_car_02_cat,ps_ind_02_cat,ps_car_11,ps_car_05_cat,ps_calc_09,ps_calc_05,ps_ind_08_bin,ps_car_08_cat,ps_ind_09_bin,ps_ind_04_cat,ps_ind_18_bin,ps_ind_12_bin,ps_ind_14,ps_reg_01_plus_ps_car_02_cat,ps_reg_01_plus_ps_car_04_cat,id,target"

# In[ ]:
train_feats = ['ps_car_13',
 'ps_reg_03',
 'ps_ind_05_cat',
 'ps_ind_03',
 'ps_ind_15',
 'ps_reg_02',
 'ps_car_14',
 'ps_car_12',
 'ps_car_01_cat',
 'ps_car_07_cat',
 'ps_ind_17_bin',
 'ps_car_03_cat',
 'ps_reg_01',
 'ps_car_15',
 'ps_ind_01',
 'ps_ind_16_bin',
 'ps_ind_07_bin',
 'ps_car_06_cat',
 'ps_car_04_cat',
 'ps_ind_06_bin',
 'ps_car_09_cat',
 'ps_car_02_cat',
 'ps_ind_02_cat',
 'ps_car_11',
 'ps_car_05_cat',
 'ps_calc_09',
 'ps_calc_05',
 'ps_ind_08_bin',
 'ps_car_08_cat',
 'ps_ind_09_bin',
 'ps_ind_04_cat',
 'ps_ind_18_bin',
 'ps_ind_12_bin',
 'ps_ind_14',
 'ps_reg_01_plus_ps_car_02_cat',
 'ps_reg_01_plus_ps_car_04_cat']

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

def open_with_first_line_skipped(path, skip=True):
    f = open(path)
    if not skip:
        return f
    next(f)
    return f

def hashstr(str, nr_bins):
    return int(hashlib.md5(str.encode('utf8')).hexdigest(), 16)%(nr_bins-1)+1

def gen_feats2(row):
    feats = []
    for j in train_feats:
        field = j
        value = row[field]
        if value != '':
            value = int(np.ceil(float(value)))
            if value > 2:
                value = int(math.log(float(value))**2)
            else:
                value = 'SP'+str(value)
        key = field + '-' + str(value)
        feats.append(key)
    return feats

def gen_feats(row):
    feats = []
    for j in train_feats:
        field = j
        value = row[field]
        if value != '':
            value = int(value)
            if value > 2:
                value = int(math.log(float(value))**2)
            else:
                value = 'SP'+str(value)
        key = field + '-' + str(value)
        feats.append(key)
    return feats

def read_freqent_feats(threshold=10):
    print('1')
    frequent_feats = set()
    for row in csv.DictReader(open('../cache/fc.trva.t10.txt')):
        if int(row['Total']) < threshold:
            continue
        print(row['Value'])
        
        frequent_feats.add(row['Field']+'-'+ row['Value'])
    return frequent_feats

def split(path, nr_thread, has_header):

    def open_with_header_witten(path, idx, header):
        f = open(path+'.__tmp__.{0}'.format(idx), 'w')
        if not has_header:
            return f 
        f.write(header)
        return f

    def calc_nr_lines_per_thread():
        nr_lines = int(list(subprocess.Popen('wc -l {0}'.format(path), shell=True, 
            stdout=subprocess.PIPE).stdout)[0].split()[0])
        if not has_header:
            nr_lines += 1 
        return math.ceil(float(nr_lines)/nr_thread)

    header = open(path).readline()

    nr_lines_per_thread = calc_nr_lines_per_thread()

    idx = 0
    f = open_with_header_witten(path, idx, header)
    for i, line in tqdm(enumerate(open_with_first_line_skipped(path, has_header), start=1)):
        if i%nr_lines_per_thread == 0:
            f.close()
            idx += 1
            f = open_with_header_witten(path, idx, header)
        f.write(line)
    f.close()

def parallel_convert(cvt_path, arg_paths, nr_thread):

    workers = []
    for i in range(nr_thread):
        cmd = '{0}'.format(os.path.join('.', cvt_path))
        for path in arg_paths:
            cmd += ' {0}'.format(path+'.__tmp__.{0}'.format(i))
        worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        workers.append(worker)
    for worker in workers:
        worker.communicate()

def cat(path, nr_thread):
    
    if os.path.exists(path):
        os.remove(path)
    for i in range(nr_thread):
        cmd = 'cat {svm}.__tmp__.{idx} >> {svm}'.format(svm=path, idx=i)
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()

def delete(path, nr_thread):
    
    for i in range(nr_thread):
        os.remove('{0}.__tmp__.{1}'.format(path, i))
        

def append_to_csv(batch, csv_file):
    props = dict(encoding='utf-8', index=False)
    if not os.path.exists(csv_file):
        batch.to_csv(csv_file, **props)
    else:
        batch.to_csv(csv_file, mode='a', header=False, **props)

def delete_file_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)
        
def chunk_dataframe(df, n):
    for i in range(0, len(df), n):
        yield df.iloc[i:i+n]



