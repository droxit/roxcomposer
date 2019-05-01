#! /usr/bin/env python3
#
# cmdparser.py
#
# usage: tokenize(line) will return a list of recognized tokens.
# Integers (decimal and hexadecimal) and floats are cast to their native type.
#
# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU General Public License as published by |
# | the Free Software Foundation, either version 3 of the License, or    |
# | (at your option) any later version.                                  |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU General Public License           |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|
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
