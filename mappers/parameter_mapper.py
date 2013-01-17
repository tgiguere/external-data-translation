#!/usr/bin/env python

"""
@package coi
@file coverage-creator/parameter_mapper.py
@author James Case
@brief The core classes comprising the ParameterMapper
"""

import os
import csv

# TODO: Make specific error classes
class ParameterMapperError(Exception):
    pass

class ParameterMapper(object):
    """
    The PersistenceLayer class manages the disk-level storage (and retrieval) of the Coverage Model using HDF5 files.
    """

    def __init__(self, pmap_file, parameter_dictionary, **kwargs):
        """
        Constructor for ParameterMapper

        @param root
        @param kwargs
        @return None
        """
        # TODO: What does the structure of this file look like?
        if os.path.exists(pmap_file):
            self.pmap_file = pmap_file
        else:
            raise ValueError('Parameter mapping file {0} not found'.format(pmap_file))

        # TODO: Verify is instance of ParameterDictionary
        self.parameter_dictionary = parameter_dictionary

        # TODO: Get the parameter_types, axis_types and variability from the CoverageModel
        self.parameter_types = [
            'ReferenceType',
            'BooleanType',
            'CategoryType',
            'CountType',
            'QuantityType',
            'TextType',
            'TimeType',
            'CategoryRangeType',
            'CountRangeType',
            'QuantityRangeType',
            'TimeRangeType',
            'FunctionType',
            'ConstantType',
            'RecordType',
            'VectorType',
            'ArrayType'
        ]

        self.axis_types = [
            'TIME',
            'LON',
            'LAT',
            'HEIGHT',
            'GEO_X',
            'GEO_Y',
            'GEO_Z'
        ]

        self.variability = [
            'BOTH',
            'NONE',
            'TEMPORAL',
            'SPATIAL'
        ]

        # TODO: Stand up parameter mapping dictionary
        self.pmap_dict = {}

        # TODO Stand up the ParameterContext mapping dict
        self.param_context_listing = []

    def _parse_pmap(self):
        """
        Parses the parameter mapping file supplied by the user and creates a dictionary object
        """

        header = [
            'ID',
            'SRC_VARIABLE_NAME',
            'DEST_PARAMETER_NAME',
            'DEST_TYPE',
            'DEST_AXIS',
            'DEST_FILL_VALUE',
            'DEST_VARIABILITY',
            'DEST_UOM'
        ]

        # TODO: Read in the pmap file
        with open(self.pmap_file, 'rb') as pmap_file:
            pmap_reader = csv.reader(pmap_file, delimiter=',', quotechar='|')
            # TODO: Construct the dict
            # Skip the header
            pmap_reader.next()
            for row in pmap_reader:
                self.pmap_dict[row[1]] = dict([(header[2], row[2]), (header[3], row[3]), (header[4], row[4]), (header[5], row[5]), (header[6], row[6])])
#                self.pmap_dict[header[0]] = row[0]
#                self.pmap_dict[header[1]] = row[1]
#                self.pmap_dict[header[2]] = row[2]
#                self.pmap_dict[header[3]] = row[3]
#                self.pmap_dict[header[4]] = row[4]
#                self.pmap_dict[header[5]] = row[5]
#                self.pmap_dict[header[6]] = row[6]

    def _load_pdict(self):
        self.param_context_listing = []
        # TODO: Loads the ParameterDictionary into a local construct for mapping evaluation
        # TODO: Manually appending test parameter names at the moment
        # Example: cov.list_parameters() creates a list or ParameterDictionary.keys() does the same
        # TODO: Use this when ready: self.param_context_listing = self.parameter_dictionary.keys()
        self.param_context_listing.append('temp')
        self.param_context_listing.append('salinity')
        self.param_context_listing.append('junk')

    def get_mapping(self):
        """
        Uses the parsed pmap file and pdict to form the mapping between the external dataset and the ParameterDictionary
        @return mapping dictionary
        """
        self._parse_pmap()
        self._load_pdict()

        # TODO: Associate keys from the pmap dict to the pdict parameter context
        pmap = dict([(x,self.pmap_dict[x]['DEST_PARAMETER_NAME']) for i,x in enumerate(self.pmap_dict)])
        return pmap
