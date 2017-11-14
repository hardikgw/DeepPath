#!/usr/bin/env python

from KB import KB
from BFS import BFS
import sys


def main():

    file = "full_data.txt"
    entity1 = "/m/017dcd"
    entity2 = "/m/0184jc"
    num_paths = 5

    kb = KB()
    with open(file, 'r') as f:
        for line in f.readlines():
            ent1, rel, ent2 = extract(line.rstrip())
            rel_inv = rel + '_inv'
            kb.addRelation(ent1, rel, ent2)
            kb.addRelation(ent2, rel_inv, ent1)
    print('Finishing building')
    num_intermediates = int(num_paths)
    intermediates = pickRandomIntermediatesFrom(kb, entity1, entity2, num_intermediates)
    res_entity_lists = []
    res_path_lists = []
    for i in range(num_intermediates):
        suc1, entity_list1, path_list1 = BFS(kb, entity1, intermediates[i])
        if not suc1:
            continue
        suc2, entity_list2, path_list2 = BFS(kb, intermediates[i], entity2)
        res_entity_lists.append(entity_list1 + entity_list2[1:])
        res_path_lists.append(path_list1 + path_list2)
    prettyPrint(res_entity_lists, res_path_lists)


def extract(line):
    return line.split('\t')


def pickRandomIntermediatesFrom(kb, entity1, entity2, num_intermediates):
    try:
        return kb.pickRandomIntermediatesBetween(entity1, entity2, num_intermediates)
    except ValueError as err:
        print(err.args)


def prettyPrint(entity_lists, path_lists):
    if len(entity_lists) == 0:
        print('Cannot find any path')
    for i in range(len(entity_lists)):
        print("Entities List:", entity_lists[i])
        print("Paths List:", path_lists[i])
        print('------------------')


if __name__ == "__main__":
    main()
