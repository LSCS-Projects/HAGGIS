# c_clean.py - Python class (Controller) for controlling the tasks of the Model
# and View.
#
# Copyright (C) 2014-5 Digitising Scotland Project
#
# Author: Konstantinos Daras <konstantinos.daras@gmail.com>
# Source code: https://github.com/LSCS-Projects/HAGGIS
# Web site: http://lscs-projects.github.io/HAGGIS/
# =============================================================================
#
#  This Source Code is subject to the terms of the GPL 3.0 license. For license
#  information, see http://www.gnu.org/licenses/gpl.html 
#
# =============================================================================

# -------------------------------------------------------------------------------------
# Import necessary modules
from app_models import m_clean
from app_views import v_clean

# Load the <yaml> configuration file and set the properties
# ------------------------------------------------------------------------------------
class CClean(object):
    """<c_clean> class for controlling the <m_clean> model and the <v_clean> view.
    """
    # Constructor: Creates the <m_clean> model and <v_clean> view properties 
    # --------------------------------------------------------------------------------
    def __init__(self):
        self.model = m_clean.Clean()
        self.view = v_clean.VClean()
    # --------------------------------------------------------------------------------

    # <clean_field> method - calls the <load_yaml_file> method of <m_load> model 
    # and presents appropriate message using the <load_yaml_file> method of 
    # <v_load> view.
    # --------------------------------------------------------------------------------
    def clean_field(self, 
                    sqlite_db, 
                    table_name,
                    field_name, 
                    lowercase, 
                    strip_white, 
                    rm_punctuation):

        self.view.cmd_clean(table_name, field_name)

        is_clean = self.model.clean_field(sqlite_db, 
                                          table_name, 
                                          field_name, 
                                          lowercase, 
                                          strip_white, 
                                          rm_punctuation)

        is_clean = self.model.remove_address_numbers(sqlite_db, 
                                                     table_name, 
                                                     field_name)
        return is_clean


    # <remove_address_numbers> method - calls the <remove_address_numbers> method of 
    # <m_load> model and presents appropriate message using the <remove_address_numbers> 
    # method of <v_load> view.
    # --------------------------------------------------------------------------------
    def remove_address_numbers(self, 
                               sqlite_db, 
                               table_name,
                               field_name):
        
        is_clean = self.model.remove_address_numbers(sqlite_db, 
                                                     table_name, 
                                                     field_name)
        return is_clean

    # <remove_special_tokens> method - Removes tokens related to a field name and stores  
    #                                  them in a new field. 
    # --------------------------------------------------------------------------------- 
    def remove_special_tokens(self, 
                              sqlite_db,
                              table_name,
                              rm_field_name,
                              cp_field_name,
                              csv_path):

        self.model.remove_special_tokens(sqlite_db,
                                         table_name,
                                         rm_field_name,
                                         cp_field_name,
                                         csv_path)

    # <remove_street_duplicates> method - calls the <remove_street_duplicates> method 
    # of <m_load> model and presents appropriate message using the 
    # <remove_street_duplicates> method of <v_load> view.
    # --------------------------------------------------------------------------------
    def remove_street_duplicates(self, 
                                 sqlite_db, 
                                 table_name,
                                 group_by_fields):
        
        is_clean = self.model.remove_street_duplicates(sqlite_db, 
                                                       table_name,
                                                       group_by_fields)
        return is_clean

    # <replace_aliases> method - calls the <replace_aliases> method of <m_load> model 
    # and presents appropriate message using the <replace_aliases> method of 
    # <v_load> view.
    # --------------------------------------------------------------------------------
    def replace_aliases(self,
                        sqlite_db,
                        table_name,
                        field_name,
                        accept_substring):

        self.model.replace_aliases(sqlite_db, 
                                   table_name,
                                   field_name,
                                   accept_substring)

    # <clone_table> method - clones an existing table in database
    # --------------------------------------------------------------------------------
    def clone_table(self,
                    sqlite_db,
                    db_table,
                    new_table):

        self.model.clone_table(sqlite_db,
                               db_table,
                               new_table)

    # --------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------

