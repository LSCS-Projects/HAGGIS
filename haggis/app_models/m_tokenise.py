# m_tokenise.py - Python class (Model) for string tokenisation properties and 
# methods.
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
import string
import re
from collections import OrderedDict

class Tokenise(object):
    """<Tokenise> class for tokenising street field.
    """
    # Constructor: Initialises the properties of <Tokenise> instance.
    # ---------------------------------------------------------------------------------
    def __init__(self):
        self.is_tokenised = False
        self.tokens = []
        self.first_token = ''
        self.aliases = []
    
    # <tokenise_address> method - Tokenises the string data stored at the <record_id> 
    #                             row of <table_name> table.
    #                             Returns a list of <tokens> for a given address
    # ---------------------------------------------------------------------------------   
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
            <use_alias>: Use of Alias names [Boolean]
        """

        _cur = sqlite_db.rCur()
        _cur.execute('SELECT Id, Name, Num, Street, Locality, Town \
                      FROM %s WHERE Id = %i' % (table_name, record_id)) 
        _tokens = []    
        for _row in _cur.fetchall():
            if (_row[1] is not None) and (_row[1] != '') and (bool_name == True):
                _tokens += _row[1].split()

            if (_row[2] is not None) and (_row[2] != '') and (bool_num == True):
                _tokens += _row[2].split()

            if (_row[3] is not None) and (_row[3] != '') and (bool_street == True):
                _tokens += _row[3].split()
            
            if (_row[4] is not None) and (_row[4] != '') and (bool_locality == True):
                _tokens += _row[4].split()

            if (_row[5] is not None) and (_row[5] != '') and (bool_town == True):
                _tokens += _row[5].split()
       
        self.tokens = _tokens
        
        # Remove the duplicate tokens
        self.tokens = list(OrderedDict.fromkeys(self.tokens))

        if len(self.tokens) >= 1:
            self.is_tokenised = True

        return  self.tokens

    # <tokenise_mem_address> method - Tokenises the string data stored at the <record_id> 
    #                                 row of <table_name> memory table.
    #                                 Returns a list of <tokens> for a given address
    # ---------------------------------------------------------------------------------   
    def tokenise_mem_address(self, 
                             mem_db,
                             table_name,
                             record_id,
                             bool_name,
                             bool_street,
                             use_alias):

        """ <mem_db>: Memory database 
            <table_name>: Table name 
            <record_id>: Row identification number
            <bool_name>: Tokenize Name column [Boolean]
            <bool_street>: Tokenize Street column [Boolean]
            <use_alias>: Use of Alias names [Boolean]
        """

        _cur = mem_db.cursor() 

        _rows = _cur.execute('SELECT docid, Name, Street \
                                FROM %s WHERE docid = %i' % (table_name, record_id)).fetchall() 
        _tokens = []  
        if _rows:  
            for _row in _rows:
                if (_row[1] is not None) and (_row[1] != '') and (bool_name == True):
                    _tokens += _row[1].split()

                if (_row[2] is not None) and (_row[2] != '') and (bool_street == True):
                    _tokens += _row[2].split()
       
        self.tokens = _tokens
        
        # Remove the duplicate tokens
        self.tokens = list(OrderedDict.fromkeys(self.tokens))

        if len(self.tokens) >= 1:
            self.is_tokenised = True
        else:
            self.is_tokenised = False

        return  self.tokens
    
    # <tokenise_street> method - Tokenises the street string. Removes tokens with digits
    #                            if <remove_digit_tokens> is True. 
    #                            Returns a list of <tokens> for a given address removing
    #                            tokens that they are containing a digit.
    # ---------------------------------------------------------------------------------   
    def tokenise_street(self, 
                        row,
                        remove_digit_tokens):

        """ <row>: The street string for tokenisation 
            <remove_digit_tokens>: Removing tokens containing a digit [Boolean]
        """

        _digits = re.compile('\d')
        
        _tokens = []    
        _tokens += row.split()       
        self.tokens = _tokens
        
        if bool(_digits.search(_tokens[0])):
            self.first_token = _tokens[0]

       
        # Remove tokens consisting of digits only
        if remove_digit_tokens:
            for _token in self.tokens:
                self.tokens[:] = [_token for _token in self.tokens 
                                  if not bool(_digits.search(_token))]

        if len(self.tokens) >= 1:
            self.is_tokenised = True

        return  self.tokens

    # <tokenise_all> method - Tokenises the string data stored at the <table_name> table.
    #                         Returns a list of <tokens> for a given table.
    # ---------------------------------------------------------------------------------
    def tokenise_all (self,
                      sqlite_db,
                      table_name,
                      bool_name,
                      bool_num,
                      bool_street,
                      bool_locality,
                      bool_town,
                      use_alias):

        """ <sqlite_db>: SQLite database 
            <table_name>: Table name 
            <bool_name>: Tokenize Name column [Boolean]
            <bool_num>: Tokenize Num column [Boolean]
            <bool_street>: Tokenize Street column [Boolean]
            <bool_locality>: Tokenize Locality column [Boolean]
            <bool_town>: Tokenize Town column [Boolean]
            <use_alias>: Use of Alias names [Boolean]
        """

        _cur = sqlite_db.rCur()
        _cur.execute('SELECT Id, Name, Num, Street, Locality, Town \
                      FROM %s' % (table_name)) 
        _tokens = [] 
        _digits = re.compile('\d')   
        for _row in _cur.fetchall():
            if (_row[1] is not None) and (_row[1] != '') and (bool_name == True):
                for token in _row[1].split():
                    _tokens.append(token)

            if (_row[2] is not None) and (_row[2] != '') and (bool_num == True):
               for token in _row[2].split():
                    _tokens.append(token)

            if (_row[3] is not None) and (_row[3] != '') and (bool_street == True):
                for token in _row[3].split():
                    _tokens.append(token)
            
            if (_row[4] is not None) and (_row[4] != '') and (bool_locality == True):
                for token in _row[4].split():
                    _tokens.append(token)

            if (_row[5] is not None) and (_row[5] != '') and (bool_town == True):
                _tokens += word_tokenize(_row[5])
       
        self.tokens = _tokens

        #if use_alias:
        #    for _token in _tokens:
        #        _cur.execute("SELECT Alias, Name, Freq FROM Atb \
        #                      WHERE Alias = '%s'" % _token)
        #        _alias_res = _cur.fetchall()
        #        if _alias_res is not None:
        #            for _alias in _alias_res:
        #                self.aliases += [[_alias[0], _alias[1]]]
        
        ## Remove tokens consisting of digits only
        #for _token in self.tokens:
        #    if any(c.isdigit() for c in _token):
        #        self.tokens.remove(_token)

        if len(self.tokens) >= 1:
            self.is_tokenised = True

        return  self.tokens


   