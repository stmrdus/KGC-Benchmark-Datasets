import pandas as pd
import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser("Python scirpt for OpenKE dataset initialization.")
parser.add_argument("--folder", default="FB15K-237",
                    help="Name of dataset folder.")
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

lef = {}
rig = {}
rellef = {}
relrig = {}

triple = open(args.folder+"train2id.txt", "r")
valid = open(args.folder+"valid2id.txt", "r")
test = open(args.folder+"test2id.txt", "r")

tot = (int)(triple.readline())
for i in range(tot):
    content = triple.readline()
    h, t, r = content.strip().split()
    if not (h, r) in lef:
        lef[(h, r)] = []
    if not (r, t) in rig:
        rig[(r, t)] = []
    lef[(h, r)].append(t)
    rig[(r, t)].append(h)
    if not r in rellef:
        rellef[r] = {}
    if not r in relrig:
        relrig[r] = {}
    rellef[r][h] = 1
    relrig[r][t] = 1

tot = (int)(valid.readline())
for i in range(tot):
    content = valid.readline()
    h, t, r = content.strip().split()
    if not (h, r) in lef:
        lef[(h, r)] = []
    if not (r, t) in rig:
        rig[(r, t)] = []
    lef[(h, r)].append(t)
    rig[(r, t)].append(h)
    if not r in rellef:
        rellef[r] = {}
    if not r in relrig:
        relrig[r] = {}
    rellef[r][h] = 1
    relrig[r][t] = 1

tot = (int)(test.readline())
for i in range(tot):
    content = test.readline()
    h, t, r = content.strip().split()
    if not (h, r) in lef:
        lef[(h, r)] = []
    if not (r, t) in rig:
        rig[(r, t)] = []
    lef[(h, r)].append(t)
    rig[(r, t)].append(h)
    if not r in rellef:
        rellef[r] = {}
    if not r in relrig:
        relrig[r] = {}
    rellef[r][h] = 1
    relrig[r][t] = 1

test.close()
valid.close()
triple.close()

f = open(args.folder+"type_constrain.txt", "w")
f.write("%d\n" % (len(rellef)))
for i in rellef:
    f.write("%s\t%d" % (i, len(rellef[i])))
    for j in rellef[i]:
        f.write("\t%s" % (j))
    f.write("\n")
    f.write("%s\t%d" % (i, len(relrig[i])))
    for j in relrig[i]:
        f.write("\t%s" % (j))
    f.write("\n")
f.close()

rellef = {}
totlef = {}
relrig = {}
totrig = {}
# lef: (h, r)
# rig: (r, t)
for i in lef:
    if not i[1] in rellef:
        rellef[i[1]] = 0
        totlef[i[1]] = 0
    rellef[i[1]] += len(lef[i])
    totlef[i[1]] += 1.0

for i in rig:
    if not i[0] in relrig:
        relrig[i[0]] = 0
        totrig[i[0]] = 0
    relrig[i[0]] += len(rig[i])
    totrig[i[0]] += 1.0

s11 = 0
s1n = 0
sn1 = 0
snn = 0
f = open(args.folder+"test2id.txt", "r")
tot = (int)(f.readline())
for i in range(tot):
    content = f.readline()
    h, t, r = content.strip().split()
    rign = rellef[r] / totlef[r]
    lefn = relrig[r] / totrig[r]
    if (rign < 1.5 and lefn < 1.5):
        s11 += 1
    if (rign >= 1.5 and lefn < 1.5):
        s1n += 1
    if (rign < 1.5 and lefn >= 1.5):
        sn1 += 1
    if (rign >= 1.5 and lefn >= 1.5):
        snn += 1
f.close()


f = open(args.folder+"test2id.txt", "r")
f11 = open(args.folder+"1-1.txt", "w")
f1n = open(args.folder+"1-n.txt", "w")
fn1 = open(args.folder+"n-1.txt", "w")
fnn = open(args.folder+"n-n.txt", "w")
fall = open(args.folder+"test2id_all.txt", "w")
tot = (int)(f.readline())
fall.write("%d\n" % (tot))
f11.write("%d\n" % (s11))
f1n.write("%d\n" % (s1n))
fn1.write("%d\n" % (sn1))
fnn.write("%d\n" % (snn))
for i in range(tot):
    content = f.readline()
    h, t, r = content.strip().split()
    rign = rellef[r] / totlef[r]
    lefn = relrig[r] / totrig[r]
    if (rign < 1.5 and lefn < 1.5):
        f11.write(content)
        fall.write("0"+"\t"+content)
    if (rign >= 1.5 and lefn < 1.5):
        f1n.write(content)
        fall.write("1"+"\t"+content)
    if (rign < 1.5 and lefn >= 1.5):
        fn1.write(content)
        fall.write("2"+"\t"+content)
    if (rign >= 1.5 and lefn >= 1.5):
        fnn.write(content)
        fall.write("3"+"\t"+content)
fall.close()
f.close()
f11.close()
f1n.close()
fn1.close()
fnn.close()
