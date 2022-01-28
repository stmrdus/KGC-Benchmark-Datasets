import pandas as pd
import numpy as np
import html
from argparse import ArgumentParser

import os
from collections import defaultdict

# https://github.com/merialdo/research.lpca

FILENAME = "relation_properties.csv"
SYMMETRIC = "Symmetric"
ANTISYMMETRIC = "Antisymmetric"
REFLEXIVE = "Reflexive"
IRREFLEXIVE = "Irreflexive"
TRANSITIVE = "Transitive"
PARTIAL_EQUIVALENCE = "Partial Equivalence"
EQUIVALENCE = "Equivalence"
PREORDER = "Preorder"
ORDER = "Order"

ALL_PROPERTIES_NAMES = [REFLEXIVE, IRREFLEXIVE, SYMMETRIC, ANTISYMMETRIC, TRANSITIVE, PREORDER, ORDER, PARTIAL_EQUIVALENCE, EQUIVALENCE]

parser = ArgumentParser("Relation types script")
parser.add_argument("--folder", default="YAGO3-10", help="Name of dataset folder.")
args = parser.parse_args()
print(args)

entities = set()
relationships = set()

train_path = args.folder + "/train.txt"
valid_path = args.folder + "/valid.txt"
test_path = args.folder + "/test.txt"
separator = "\t"
write_separator = ";"

def read_triples(triples_path, separator="\t"):
    triples = []
    with open(triples_path, "r") as triples_file:
        lines = triples_file.readlines()
        for line in lines:
            #line = html.unescape(line)
            head, relationship, tail = line.strip().split(separator)
            triples.append((head, relationship, tail))
            entities.add(head)
            entities.add(tail)
            relationships.add(relationship)
    return triples

print("Reading train triples for %s..." % args.folder)
train_triples = read_triples(train_path, separator)

print("Reading validation triples for %s..." % args.folder)
valid_triples = read_triples(valid_path, separator)

print("Reading test triples for %s..." % args.folder)
test_triples = read_triples(test_path, separator)


def _check_reflexivity(relation, relation_2_train_facts, tolerance=0.5):
    facts_with_that_relation = relation_2_train_facts[relation]
    heads = set()
    for fact in facts_with_that_relation:
        heads.add(fact[0])
    reflexive_count = 0
    overall_count = 0
    for head in heads:
        overall_count +=1
        if (head, relation, head) in facts_with_that_relation:
            reflexive_count+=1
    if reflexive_count == 0:
        return IRREFLEXIVE
    if (float(reflexive_count)/float(overall_count)) >= tolerance:
        return REFLEXIVE
    else:
        return None


def _check_symmetry(relation, relation_2_train_facts, tolerance=0.5):
    facts_with_that_relation = relation_2_train_facts[relation]
    numerator_count = 0
    denominator_count = 0
    for (head, relation, tail) in facts_with_that_relation:
        if head == tail:
            continue
        denominator_count += 1
        if (tail, relation, head) in facts_with_that_relation:
            numerator_count += 1
    if numerator_count == 0:
        return ANTISYMMETRIC
    if (float(numerator_count) / float(denominator_count)) >= tolerance:
        return SYMMETRIC
    else:
        return None

def _check_transitivity(relation, relation_2_train_facts, head_2_train_facts, tolerance=0.5):
    facts_with_that_relation = relation_2_train_facts[relation]
    all_chains_count = 0
    transitive_chains_count = 0
    for step_one_fact in facts_with_that_relation:
        (head1, relation1, tail1) = step_one_fact
        if head1 == tail1:
            continue
        for step_two_fact in head_2_train_facts[tail1]:
            (head2, relation2, tail2) = step_two_fact
            if relation2 != relation:
                continue
            if head2 == tail2 or tail2 == head1:
                continue
            all_chains_count += 1
            if (head1, relation, tail2) in facts_with_that_relation:
                transitive_chains_count += 1
    if transitive_chains_count > 0 and (float(transitive_chains_count) / float(all_chains_count)) >= tolerance:
        return TRANSITIVE
    else:
        return None

relation_2_types = defaultdict(lambda: [])
relation_2_train_facts = defaultdict(lambda: set())
head_2_train_facts = defaultdict(lambda: set())

print("Computing the mappings <relation name -> type> in %s training set..." % args.folder)

for (head, relation, tail) in train_triples:
    relation_2_train_facts[relation].add((head, relation, tail))
    head_2_train_facts[head].add((head, relation, tail))

for relation in relationships:
    relation_2_types[relation] = []

    is_reflexive = _check_reflexivity(relation, relation_2_train_facts)
    is_symmetric = _check_symmetry(relation, relation_2_train_facts)
    is_transitive = _check_transitivity(relation, relation_2_train_facts, head_2_train_facts)

    if is_reflexive is not None:
        relation_2_types[relation].append(is_reflexive)
    if is_symmetric is not None:
        relation_2_types[relation].append(is_symmetric)
    if is_transitive is not None:
        relation_2_types[relation].append(is_transitive)

    if REFLEXIVE in relation_2_types[relation] and TRANSITIVE in relation_2_types[relation]:
            relation_2_types[relation].append(PREORDER)
    if REFLEXIVE in relation_2_types[relation] and ANTISYMMETRIC in relation_2_types[relation] and TRANSITIVE in relation_2_types[relation]:
        relation_2_types[relation].append(ORDER)
    if SYMMETRIC in relation_2_types[relation] and TRANSITIVE in relation_2_types[relation]:
        relation_2_types[relation].append(PARTIAL_EQUIVALENCE)
    if REFLEXIVE in relation_2_types[relation] and SYMMETRIC in relation_2_types[relation] and TRANSITIVE in relation_2_types[relation]:
        relation_2_types[relation].append(EQUIVALENCE)

lines = []
for relation in sorted(relationships):
    lines.append(write_separator.join([relation, ",".join(relation_2_types[relation])]) + "\n")

output_filepath = FILENAME

print("Writing the mappings <entity name -> in, out and overall degree> for %s training set in %s..." % (args.folder, output_filepath))

output_filepath = args.folder + "/" + FILENAME
with open(output_filepath, "w") as output_file:
    output_file.writelines(lines)
        

