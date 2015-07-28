# c_load.py - Python class (Controller) for controling the tasks of the 
# <m_load> and <v_load>.
#
# Copyright (C) 2014-5 Digitising Scotland Project
#
# Author: Konstantinos Daras <konstantinos.daras@gmail.com>
# Source code: https://github.com/LSCS-Projects/HAGGIS
# Web site: http://lscs-projects.github.io/HAGGIS/
# =====================================================================================
#
#  This Source Code is subject to the terms of the GPL 3.0 license. For license
#  information, see http://www.gnu.org/licenses/gpl.html 
#
# =====================================================================================

# -------------------------------------------------------------------------------------
# Import necessary modules
from app_models import m_load
from app_views import v_load

# Load the <yaml> configuration file and set the properties
# ------------------------------------------------------------------------------------
class c_load(object):
    """<c_load> class for controling the <m_load> model and the <v_load> view.
    """
    # Constructor: Creates the <m_load> model and <v_load> view properties 
    # --------------------------------------------------------------------------------
    def __init__(self):
        self.app_config = m_load.AppConfig()
        self.csv_data = m_load.CsvData()
        self.view = v_load.v_load()
    # --------------------------------------------------------------------------------

    # <load_yaml_file> method - calls the <load_yaml_file> method of <m_load> model 
    # and presents appropriate message using the <load_yaml_file> method of 
    # <v_load> view.
    # --------------------------------------------------------------------------------
    def load_yaml_file(self, yaml_path):
        self.app_config.load_yaml_file(yaml_path)
        self.view.load_yaml_file(self.app_config.cfg_yaml_file)
        cfg_data = self.app_config
        return cfg_data
    # --------------------------------------------------------------------------------

    # <load_csv_file> method - calls the <load_csv_file> method of <m_load> model 
    # and presents appropriate message using the <load_csv_file> method of 
    # <v_load> view.
    # --------------------------------------------------------------------------------
    def load_csv_sqlite(self, 
                        sqlite_db, 
                        csv_filename, 
                        table_name, 
                        field_names, 
                        rest_key, 
                        delimiter, 
                        quote_char, 
                        auto_fields):
        
        self.csv_data.csv_filename = csv_filename
        self.csv_data.field_names = field_names
        self.csv_data.rest_key = rest_key
        self.csv_data.delimiter = delimiter
        self.csv_data.quote_char = quote_char

        if auto_fields is False:
            self.view.load_csv_file(self.csv_data.csv_filename, False )
            self.csv_data.load_csv(sqlite_db, table_name, False)
        else:
            self.view.load_csv_file(self.csv_data.csv_filename, True)
            self.csv_data.load_csv(sqlite_db, table_name, True)
    # --------------------------------------------------------------------------------
