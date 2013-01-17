#!/usr/bin/env python

"""
@package coi
@file coverage_creator/coverage_creator.py
@author Tim Giguere
@brief Class used to create a coverage from an input data source
"""

#import numpy as np
#from coverage_model.parameter import ParameterDictionary, ParameterContext
#from coverage_model.parameter_types import QuantityType
#from coverage_model.basic_types import VariabilityEnum
#from coverage_creator.coverage_creator import coverage_creator
#pdict = ParameterDictionary()
#t_ctxt = ParameterContext('time', param_type=QuantityType(value_encoding=np.dtype('int64')), variability=VariabilityEnum.TEMPORAL)
#t_ctxt.uom = 'seconds since 01-01-1979'
#pdict.add_context(t_ctxt, is_temporal=True)
#temp_ctxt = ParameterContext('temp', param_type=QuantityType(value_encoding=np.dtype('float32')))
#temp_ctxt.uom = 'K'
#pdict.add_context(temp_ctxt)
#sal_ctxt = ParameterContext('salinity', param_type=QuantityType(value_encoding=np.dtype('float32')))
#sal_ctxt.uom = 'ppm'
#pdict.add_context(sal_ctxt)
#cov = coverage_creator('parsers.parser_csv', 'CSVParser', 'test_data/test.csv')
#cov.create_coverage('test_data/ncell.pmap', pdict)

import os
import uuid

from coverage_model.coverage import SimplexCoverage, CRS, GridDomain, GridShape
from coverage_model.basic_types import AxisTypeEnum, MutabilityEnum
from mappers.parameter_mapper import ParameterMapper

class coverage_creator():
    def __init__(self, mod_name='', class_name='', file_path=''):

        module = __import__(mod_name, fromlist=[class_name])
        classobj = getattr(module, class_name)

        self._parser = classobj(file_path)
        self._coverage = None

    def create_coverage(self, mapping_file, param_dict):

        if param_dict:
            self._param_mapper = ParameterMapper(pmap_file=mapping_file, parameter_dictionary=param_dict)

            # Construct temporal Coordinate Reference System objects
            tcrs = CRS([AxisTypeEnum.TIME])

            # Construct temporal and spatial Domain objects
            tdom = GridDomain(GridShape('temporal', [0]), tcrs, MutabilityEnum.EXTENSIBLE) # 1d (timeline)

            self._coverage = SimplexCoverage('test_data',
                                             self.create_guid(),
                                             os.path.splitext(os.path.basename('test_data/test.csv'))[0],
                                             parameter_dictionary=param_dict,
                                             temporal_domain=tdom)

            shp = self._parser.get_var_shape('time')
            self._coverage.insert_timesteps(shp[0])

            mapping = self._param_mapper.get_mapping()

            for var in self._parser.get_col_names():
                #parameter mapping goes here
                print var
                print mapping[var]
                vals = self._parser.get_values(var_name=var)
                print vals
                self._coverage.set_parameter_values(mapping[var],
                                                    value=vals)
                print self._coverage.get_parameter_values(mapping[var])

    def create_guid(self):
        """
        @retval Return global unique id string
        """
        # guids seem to be more readable if they are UPPERCASE
        return str(uuid.uuid4()).upper()