import os, re, random, datetime


def read_dictionary(filename):
    dict_to_return = {}
    with open(filename, 'rt', encoding='utf-8') as file:
        lines = [line.strip() for line in file.read().split('\n')]
        if '</>' in lines:
            mark_indexes = []
            for i, line in enumerate(lines):
                if line.strip() == '</>':
                    mark_indexes.append(i)
            if mark_indexes[0] < 2:
                mark_indexes.pop(0)
            start = 0
            for index in mark_indexes:
                dict_to_return[lines[start]] = '\n'.join(lines[start + 1:index])
                start = index + 1
        elif False not in ('\t' in line for line in lines):
            for line in lines:
                word, expl = line.split('\t')
                dict_to_return[word] = expl
    return dict_to_return


def read_wordset(filename):
    with open(filename, 'rt', encoding='utf-8') as file:
        lines = [line.strip() for line in file.read().split('\n')]
    return lines


