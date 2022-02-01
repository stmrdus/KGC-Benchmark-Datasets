import pandas as pd
import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser("Relation types script")
parser.add_argument("--folder", default="FB15K-237", help="Name of dataset folder.")
args = parser.parse_args()
print(args)

def getID(folder='FB122/'):
    lstEnts = {}
    lstRels = {}
    with open(folder + 'train.txt') as f, open(folder + 'train_marked.txt', 'w') as f2:
        count = 0
        for line in f:
            line = line.strip().split()
            line = [i.strip() for i in line]
            # print(line[0], line[1], line[2])
            if line[0] not in lstEnts:
                lstEnts[line[0]] = len(lstEnts)
            if line[1] not in lstRels:
                lstRels[line[1]] = len(lstRels)
            if line[2] not in lstEnts:
                lstEnts[line[2]] = len(lstEnts)
            count += 1
            f2.write(str(line[0]) + '\t' + str(line[1]) +
                     '\t' + str(line[2]) + '\n')
        print("Size of train_marked set set ", count)

    with open(folder + 'valid.txt') as f, open(folder + 'valid_marked.txt', 'w') as f2:
        count = 0
        for line in f:
            line = line.strip().split()
            line = [i.strip() for i in line]
            # print(line[0], line[1], line[2])
            if line[0] not in lstEnts:
                lstEnts[line[0]] = len(lstEnts)
            if line[1] not in lstRels:
                lstRels[line[1]] = len(lstRels)
            if line[2] not in lstEnts:
                lstEnts[line[2]] = len(lstEnts)
            count += 1
            f2.write(str(line[0]) + '\t' + str(line[1]) +
                     '\t' + str(line[2]) + '\n')
        print("Size of VALID_marked set set ", count)

    with open(folder + 'test.txt') as f, open(folder + 'test_marked.txt', 'w') as f2:
        count = 0
        for line in f:
            line = line.strip().split()
            line = [i.strip() for i in line]
            # print(line[0], line[1], line[2])
            if line[0] not in lstEnts:
                lstEnts[line[0]] = len(lstEnts)
            if line[1] not in lstRels:
                lstRels[line[1]] = len(lstRels)
            if line[2] not in lstEnts:
                lstEnts[line[2]] = len(lstEnts)
            count += 1
            f2.write(str(line[0]) + '\t' + str(line[1]) +
                     '\t' + str(line[2]) + '\n')
        print("Size of test_marked set set ", count)

    wri = open(folder + 'entity2id.txt', 'w')
    for entity in lstEnts:
        wri.write(entity + '\t' + str(lstEnts[entity]))
        wri.write('\n')
    wri.close()

    wri = open(folder + 'relation2id.txt', 'w')
    for entity in lstRels:
        wri.write(entity + '\t' + str(lstRels[entity]))
        wri.write('\n')
    wri.close()

print("[LOG] Init entity and relation id.")
getID(folder=args.folder)

print("[LOG] Read entity and relation id.")
entity2id = pd.read_table("FB122/entity2id.txt", header=None, sep='\t')
relation2id = pd.read_table("FB122/relation2id.txt", header=None, sep='\t')

print("[LOG] Read train, test and validation set.")
train = pd.read_table(args.folder+"/train.txt", header=None, sep='\t')
test = pd.read_table(args.folder+"/test.txt", header=None, sep='\t')
valid = pd.read_table(args.folder+"/valid.txt", header=None, sep='\t')

train[[1, 2]] = train[[2, 1]]
test[[1, 2]] = test[[2, 1]]
test[[1, 2]] = test[[2, 1]]

d = dict(zip(relation2id[0].values, relation2id[1].values))
e = dict(zip(entity2id[0].values, entity2id[1].values))

print("[LOG] Mapping train, validation and test data with id.")
def mapping(data):
    data[0] = data[0].map(e)
    data[1] = data[1].map(e)
    data[2] = data[2].map(d)

train.to_csv((args.folder+"/train2id.txt"), header=None, index=None, sep=" ")
valid.to_csv((args.folder+"/valid2id.txt"), header=None, index=None, sep=" ")
test.to_csv((args.folder+"/test2id.txt"), header=None, index=None, sep=" ")