#!/usr/bin/env python

"""
@package coi
@file parsers/parser_base.py
@author Tim Giguere
@brief Base parser class that all parsers should inherit from
"""

class Parser(object):
    def __init__(self, file_path=''):
        raise NotImplementedError('__init__ must be implemented in child class')

    def get_col_names(self):
        raise NotImplementedError('get_col_names must be implemented in child class')

    def get_var_shape(self, var_name=''):
        raise NotImplementedError('get_var_shape must be implemented in child class')

    def get_data(self, var_name='', _slice=None):
        raise NotImplementedError('get_data must be implemented in child class')