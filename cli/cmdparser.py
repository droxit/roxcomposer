#! /usr/bin/env python3
#
# cmdparser.py
#
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#
# usage: tokenize(line) will return a list of recognized tokens.
# Integers (decimal and hexadecimal) and floats are cast to their native type.
#

import re

token_patterns = [
        ('FLOAT', r'\b\d+\.\d*\b'),
        ('HEX_INT', r'\b0x[a-zA-Z0-9]+\b'),
        ('INTEGER', r'\b\d+\b'),
        ('STRING', r'\S+')
]

tok_rex = '|'.join(['(?P<{}>{})'.format(token[0], token[1]) for token in token_patterns])


def tokenize(line):
    return [type_caster(mo.lastgroup, mo.group(mo.lastgroup)) for mo in re.finditer(tok_rex, line)]


def type_caster(group, val):
    if group == 'STRING':
        return val
    if group == 'INTEGER':
        return int(val)
    if group == 'HEX_INT':
        return int(val, base=16)
    if group == 'FLOAT':
        return float(val)

    return val
