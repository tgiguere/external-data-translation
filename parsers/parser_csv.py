#!/usr/bin/env python

"""
@package coi
@file parsers/parser_csv.py
@author Tim Giguere
@brief Example CSV parser class
"""

from parsers.parser_base import Parser
import csv
import numpy as np

class CSVParser(Parser):

    def __init__(self, file_path=''):
        self.file_path = file_path
        with open(self.file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            self.col_names = csvreader.next()

    def get_col_names(self):
        return self.col_names

    def get_var_shape(self, var_name=''):
        vals = self.read_var(var_name)
        return vals.shape

    def get_values(self, var_name='', _slice=None):
        vals = self.read_var(var_name)
        if _slice:
            return vals[_slice]
        else:
            return vals

    def read_var(self, var_name=''):
        col_index = self.col_names.index(var_name)    # Will raise ValueError is name is not in list
        return np.genfromtxt(self.file_path, delimiter=',', skip_header=1, usecols=col_index)




