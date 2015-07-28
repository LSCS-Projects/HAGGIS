# c_tokenise.py - Python class (Controller) for controling the tasks of the 
# <m_tokenise> and <v_tokenise>.
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
from app_models import m_tokenise

# Load the <yaml> configuration file and set the properties
# ------------------------------------------------------------------------------------
class CTokenise(object):
    """<CTokenise> class for controling the <m_clean> model and the <v_clean> view.
    """

    # Constructor: Creates the <m_tokenise> model and <v_tokenise> view properties 
    # --------------------------------------------------------------------------------
    def __init__(self):
        self.model = m_tokenise.Tokenise()
    # --------------------------------------------------------------------------------

    # <tokenise_address> method - calls the <tokenise_address> model 
    # --------------------------------------------------------------------------------
    def tokenise_address(self, 
                         sqlite_db, 
                         table_name,
                         record_id,
                         bool_name,
                         bool_num,
                         bool_street,
                         bool_locality,
                         bool_town,
                         use_alias):

        """ <sqlite_db>: SQLite database 
            <table_name>: Table name 
            <record_id>: Row identification number
            <bool_name>: Tokenize Name column [Boolean]
            <bool_num>: Tokenize Num column [Boolean]
            <bool_street>: Tokenize Street column [Boolean]
            <bool_locality>: Tokenize Locality column [Boolean]
            <bool_town>: Tokenize Town column [Boolean]
            <use_alias>: Use Alias names [Boolean]
        """

        _tokens = self.model.tokenise_address(sqlite_db, 
                                             table_name, 
                                             record_id,
                                             bool_name,
                                             bool_num,
                                             bool_street,
                                             bool_locality,
                                             bool_town,
                                             use_alias)
        return _tokens

    # --------------------------------------------------------------------------------
    # <tokenise_address> method - calls the <tokenise_address> model 
    # --------------------------------------------------------------------------------
    def tokenise_mem_address(self, 
                             sqlite_db, 
                             table_name,
                             record_id,
                             bool_name,
                             bool_street,
                             use_alias):

        """ <mem_db>: memory database 
            <table_name>: Table name 
            <record_id>: Row identification number
            <bool_name>: Tokenize Name column [Boolean]
            <bool_street>: Tokenize Street column [Boolean]
            <use_alias>: Use Alias names [Boolean]
        """

        _tokens = self.model.tokenise_mem_address(sqlite_db, 
                                                 table_name, 
                                                 record_id,
                                                 bool_name,
                                                 bool_street,
                                                 use_alias)
        return _tokens
    # --------------------------------------------------------------------------------


