# v_load.py - Python class (View) for presenting data loading results.
#
# Copyright (C) 2014-5 Digitising Scotland Project
#
# Author: Konstantinos Daras <konstantinos.daras@gmail.com>
# Source code: https://github.com/LSCS-Projects/HAGGIS
# Web site: http://lscs-projects.github.io/HAGGIS/
# =====================================================================================
#
#  This Source Code is subject to the terms of the BSD license. For license
#  information, see LICENSE.TXT 
#
# =====================================================================================

class v_load(object):
    """<v_load> class for presenting messages and information of the application 
       configuration.
    """

    # <load_yaml_file> method - presents a load message.
    # --------------------------------------------------------------------------------
    def load_yaml_file(self, app_config):
        print('Loading configuration file "%s" ...' % app_config)

    # <load_csv_file> method - presents a load message.
    # --------------------------------------------------------------------------------
    def load_csv_file(self, csv_file, auto_fields):
        print('Loading csv file "%s" (auto read fields: "%s") ...' % (csv_file, 
                                                                      auto_fields))




