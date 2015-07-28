# c_match.py - Python class (Controller) for controling the tasks of the 
# <m_match> and <v_match>.
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
from app_models import m_match

class CMatch(object):
    """<CMatch> class for matching address fields.
    """
    # Constructor: Initialises the properties of <CMatch> instance.
    # ---------------------------------------------------------------------------------
    def __init__(self):
        self.model = m_match.Match()
    
    # <matching_addressess> method - Tokenises the string data stored at the <record_id> 
    #                             row of <table_name> table.
    #                             Returns a list of <tokens> for a given address
    # ---------------------------------------------------------------------------------   
    def matching_addressess(self, 
                            sqlite_db,
                            distance_type,
                            string_set_type,
                            matching_threshold,
                            use_alias,
                            use_freq_tables,
                            freq_tables,
                            freq_ctb_limit,
                            freq_htb_limit,
                            filter_locality,
                            filter_town):
        """ <sqlite_db>:  SQLite database
            <distance_type>: Type of string distance algorithm 
                             0 = Levenshtein edit-distance,
                             1 = FREE SLOT
                             2 = FREE SLOT
            <string_set_type>: Type of set ratio
                               3 = FREE SLOT 
                               4 = Similarity ratio
            <matching_threshold>: String matching threshold 
                                  Recommended value is 0.9 for Levenshtein distance. 
                                  Value ranges from 1 for exact match to 0 for no match.
            <use_alias>: Use of Alias names [Boolean]
            <use_freq_tables>: Use of Frequency tables [Boolean]
            <freq_ctb_limit>: Limit of token frequency for the Ctb table
            <freq_htb_limit>: Limit of token frequency for the Htb table
            <filter_locality>: Block with Locality field [Boolean]
            <filter_town>: Block with Town field [Boolean]
        """

        self.model.matching_tokens(sqlite_db,
                                   distance_type,
                                   string_set_type,
                                   matching_threshold,
                                   use_alias,
                                   use_freq_tables,
                                   freq_tables,
                                   freq_ctb_limit,
                                   freq_htb_limit,
                                   filter_locality,
                                   filter_town)

    def sec_matching (self, 
                      sqlite_db,
                      ctb_easting,
                      ctb_northing,
                      dist_code,
                      distance_type,
                      string_set_type,
                      matching_threshold,
                      rd_bb_method):
        """ <sqlite_db>:  SQLite database
            <ctb_easting>: Name of the Easting coordinate field in Ctb table
            <ctb_northing>: Name of the Northing coordinate field in Ctb table
            <dist_code>: Name of the Registration District code field in Htb table
            <distance_type>: Type of string distance algorithm 
                             0 = Levenshtein edit-distance,
                             1 = FREE SLOT
                             2 = FREE SLOT
            <string_set_type>: Type of set ratio
                               3 = FREE SLOT 
                               4 = Similarity ratio
            <matching_threshold>: String matching threshold 
                                  Recommended value is 0.9 for Levenshtein distance. 
                                  Value ranges from 1 for exact match to 0 for no match.
            <rd_bb_method>: The method for defining the bounding box of pseudo-RD
                            0: Use the bounding boxes of thiessen polygons with 
                               assigned RD codes. 
                            1: Use the bounding boxes of RD thiessen polygons
                               created by using the centroids of thiessen polygons  
                               with assigned RD codes.
        """

        self.model.sec_matching(sqlite_db,
                                ctb_easting,
                                ctb_northing,
                                dist_code,
                                distance_type,
                                string_set_type,
                                matching_threshold,
                                rd_bb_method)

    def build_freq_table(self, 
                        sqlite_db,
                        freq_tables,
                        freq_ctb_limit,
                        freq_htb_limit,
                        use_alias):
        """ <sqlite_db>: SQLite database
            <freq_tables>: Use of Frequency tables [Boolean]
            <freq_ctb_limit>: Limit of token frequency for the Ctb table
            <freq_htb_limit>: Limit of token frequency for the Htb table
            <use_alias>: Use of Alias names [Boolean]
        """

        self.model.build_freq_tables(sqlite_db,
                                   freq_tables,
                                   freq_ctb_limit,
                                   freq_htb_limit,
                                   use_alias)

 