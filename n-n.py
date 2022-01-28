import pandas as pd
import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser("Relation types script")
parser.add_argument("--folder", default="WN18RR", help="Name of dataset folder.")
args = parser.parse_args()
print(args)

train_data = pd.read_table(args.folder + "/train.txt" ,header=None, sep='\t')
valid_data = pd.read_table(args.folder + "/valid.txt" ,header=None, sep='\t')
test_data = pd.read_table(args.folder + "/test.txt" ,header=None, sep='\t')

complete_data = pd.concat([train_data, valid_data, test_data], axis = 0)

tph_count = complete_data.groupby([0, 1]).count()
tphr_count_sum = tph_count.groupby([1]).sum()
tphr_count_count = tph_count.groupby([1]).count()
tphr = tphr_count_sum / tphr_count_count
tphr = tphr[2]

hpt_count = complete_data.groupby([2, 1]).count()
hptr_count_sum = hpt_count.groupby([1]).sum()
hptr_count_count = hpt_count.groupby([1]).count()
hptr = hptr_count_sum / hptr_count_count
hptr = hptr[0]

test_data1_1, test_data1_n, test_datan_1, test_datan_n = None, None, None, None

def add_rel_category(rel_category, new_data):
    if rel_category is not None:
        return rel_category.append(new_data)
    else:
        return pd.DataFrame(data=np.array([new_data.to_numpy()]))

for index, row in test_data.iterrows():
    rel = row[1]
    hptr_temp = hptr.loc[rel]
    tphr_temp = tphr.loc[rel]
    if hptr_temp < 1.5 and tphr_temp < 1.5:
        test_data1_1 = add_rel_category(test_data1_1, row)
    elif hptr_temp < 1.5 and tphr_temp >= 1.5:
        test_data1_n = add_rel_category(test_data1_n, row)
    elif hptr_temp >= 1.5 and tphr_temp < 1.5:
        test_datan_1 = add_rel_category(test_datan_1, row)
    elif hptr_temp >= 1.5 and tphr_temp >= 1.5:
        test_datan_n = add_rel_category(test_datan_n, row)


test_data1_1.to_csv((args.folder + "/test/1-1.txt"), sep='\t', header=None, index=None)
test_data1_n.to_csv((args.folder + "/test/1-n.txt"), sep='\t', header=None, index=None)
test_datan_1.to_csv((args.folder + "/test/n-1.txt"), sep='\t', header=None, index=None)
test_datan_n.to_csv((args.folder + "/test/n-n.txt"), sep='\t', header=None, index=None)

test_data_grouped = test_data.groupby(1)

for k, gr in test_data_grouped:
    gr.to_csv((args.folder + "/test/{}.txt".format(k)), sep='\t', encoding='utf-8', index=False, header=False, mode='a')