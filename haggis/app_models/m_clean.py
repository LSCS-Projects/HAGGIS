# m_clean.py - Python class (Model) for cleaning properties and methods.
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
import time
import operator
from app_models import m_tokenise

class Clean(object):
    """<Clean> class for normalising(lowercase, strip, punctuation rem) data.
    """
    # Constructor: Initialises the properties of <Clean> instance.
    # ---------------------------------------------------------------------------------
    def __init__(self):
        self.is_clean = False
        self.no_number = False
        self.no_duplicates = False
    
    # <clean_field> method - Cleans the string data stored at the <field_name> field.
    #                        Converts string to lowercase, strips whitespaces and 
    #                        removes punctuation. 
    # ---------------------------------------------------------------------------------   
    def clean_field(self, 
                    sqlite_db,
                    table_name,
                    field_name, 
                    lowercase, 
                    strip_white, 
                    rm_punctuation):

        print('Clean field ...')
        
        _start_timer = time.time() # Timer

        _cur = sqlite_db.rCur()

        _cur.execute('SELECT Id, %s FROM %s' % (field_name, table_name)) 
            
        for _row in _cur.fetchall():
            _fld_val = _row[1]
            _hist_val = _fld_val
            if _fld_val != '':
                if lowercase:
                    _fld_val = _fld_val.lower()
                if strip_white:
                    _fld_val = _fld_val.strip()
                if rm_punctuation:
                    for p in string.punctuation:
                        if p !='?':
                            _fld_val = _fld_val.replace(p, '')
                if _fld_val != _hist_val:
                    _cur.execute("UPDATE %s SET %s = '%s' WHERE Id = %i" 
                                  % (table_name, 
                                     field_name,
                                     _fld_val,
                                     _row[0]))  
        self.is_clean = True

        print ('Time: ' + str(time.time() - _start_timer))  # Timer

        return self.is_clean
    
    # <remove_address_numbers> method - Removes the numeric substring at the start of  
    #                                   an address string. 
    # --------------------------------------------------------------------------------- 
    def remove_address_numbers(self, 
                              sqlite_db,
                              table_name,
                              field_name):

        print('Remove address numbers ...')
        _start_timer = time.time() # Timer

        _cur = sqlite_db.rCur()

        _cur.execute('SELECT Id, %s FROM %s' % (field_name, table_name)) 
            
        for _row in _cur.fetchall():
            _fld_val = _row[1]
            _hist_val = _fld_val
            if _fld_val != '':
                _tokenise = m_tokenise.Tokenise()
                _tokens = _tokenise.tokenise_street(_fld_val, 
                                                    True)
                
                _fld_val = ''
                
                for _token in _tokens:
                    _fld_val = _fld_val + _token + ' '

                _fld_val = _fld_val[:-1]

                if _fld_val != _hist_val:
                    _cur.execute("UPDATE %s SET %s = '%s' WHERE Id = %i" 
                                  % (table_name, 
                                     field_name,
                                     _fld_val,
                                     _row[0]))  
                    # If the first token has a digit then its value will added 
                    # in the 'Num' field.
                    if _tokenise.first_token != '':
                        _cur.execute("UPDATE %s SET Num = '%s' WHERE Id = %i" 
                                      % (table_name, 
                                         _tokenise.first_token,
                                         _row[0]))

        self.no_number = True

        print ('Time: ' + str(time.time() - _start_timer))  # Timer

        return self.no_number

    # <remove_special_tokens> method - Removes tokens related to a field name and stores  
    #                                  them in a new field. 
    # --------------------------------------------------------------------------------- 
    def remove_special_tokens(self, 
                              sqlite_db,
                              table_name,
                              rm_field_name,
                              cp_field_name,
                              csv_path):

        print('Remove special tokens ...')
        _start_timer = time.time() # Timer

        
        # Read <csv_path> file and store it in a List
        _file = open(csv_path, 'rb')
        _sp_tokens = _file.readlines()
        _file.close()

        # Select Id and <rm_field_name> values from the <rm_table_name> table
        _cur = sqlite_db.rCur()
        _cur.execute('SELECT Id, %s FROM %s' % (rm_field_name, table_name)) 

                    
        for _row in _cur.fetchall():
            _fld_val = _row[1]
            _hist_val = _fld_val
            if _fld_val != '':
                _tokenise = m_tokenise.Tokenise()
                _tokens = _tokenise.tokenise_street(_fld_val, 
                                                    True)
                
                _sel_tokens = [x for x in _sp_tokens if _tokens[-1:][0] in x]
                
                if len(_sel_tokens) == 1:
                    _len_sp = len(_sel_tokens[0].split())

                    if _len_sp < len(_tokens):
                        _str_sp = _sel_tokens[0].rstrip('\r\n')
                        _str_tk = ' '.join(_tokens[-_len_sp:])

                        if _str_sp == _str_tk:

                            # Clean string using _len_sp count
                            _clean_str = ' '.join(_tokens[:-_len_sp])

                            # Move value to new column
                            _cur.execute("UPDATE %s SET %s = '%s' WHERE Id = %i" 
                                          % (table_name, 
                                             cp_field_name,
                                             _str_sp,
                                             _row[0]))

                            # Update value to old column
                            _cur.execute("UPDATE %s SET %s = '%s' WHERE Id = %i" 
                                          % (table_name, 
                                             rm_field_name,
                                             _clean_str,
                                             _row[0]))


                if len(_sel_tokens) > 1:
                    for _sel_t in _sel_tokens:
                        _len_sp = len(_sel_t.split())

                        if _len_sp < len(_tokens):
                            _str_sp = _sel_t.rstrip('\r\n')
                            _str_tk = ' '.join(_tokens[-_len_sp:])

                            if _str_sp == _str_tk:

                                # Clean string using _len_sp count
                                _clean_str = ' '.join(_tokens[:-_len_sp])

                                # Move value to new column
                                _cur.execute("UPDATE %s SET %s = '%s' WHERE Id = %i" 
                                              % (table_name, 
                                                 cp_field_name,
                                                 _str_sp,
                                                 _row[0]))

                                # Update value to old column
                                _cur.execute("UPDATE %s SET %s = '%s' WHERE Id = %i" 
                                              % (table_name, 
                                                 rm_field_name,
                                                 _clean_str,
                                                 _row[0]))


        print ('Time: ' + str(time.time() - _start_timer))  # Timer


    # <remove_street_duplicates> method - Removes the street duplicates in a given   
    #                                     <field_name> field in the <sqlite_db> 
    #                                     database.
    # --------------------------------------------------------------------------------- 
    def remove_street_duplicates(self, 
                                 sqlite_db,
                                 table_name,
                                 group_by_fields):

        print('Remove duplicates ...')
        _start_timer = time.time() # Timer

        _cur = sqlite_db.rCur()
        args = ''
        for item in group_by_fields:
            args = args + item + ","
        args = args[:-1]
        _cur.execute('SELECT Id, %s, COUNT(*) AS Freq FROM %s GROUP BY %s' % (args,
                                                                              table_name,
                                                                              args))
        uniqueAddresses = _cur.fetchall()
        args = ''
        for item in uniqueAddresses:
            args = args + str(item[0]) + ","
        args = args[:-1]

        _cur.execute('DELETE FROM %s WHERE Id NOT IN (%s)' % (table_name,
                                                              args))
        sqlite_db.conn.commit()
        
        print ('Time: ' + str(time.time() - _start_timer))  # Timer

        # Clean empty spaces after DELETE 
        _cur.execute('VACUUM')

        # Add CntEvents column to the table
        _cur.execute('ALTER TABLE %s ADD COLUMN CntEvents INTEGER' % (table_name,))

        # Populate the CntEvents column using event frequencies 
        for item in uniqueAddresses:
            _cur.execute("UPDATE %s SET CntEvents = %i WHERE Id = %i" % (table_name, 
                                                                         item[len(item)-1],
                                                                         item[0]))  
        sqlite_db.conn.commit()


    # <replace_aliases> method - Replaces the alias substrings with full names 
    # --------------------------------------------------------------------------------- 
    def replace_aliases(self, 
                        sqlite_db,
                        table_name,
                        field_name,
                        accept_substring):

        _cur = sqlite_db.rCur()

        _cur.execute('SELECT Id, %s FROM %s' % (field_name, table_name)) 
            
        for _row in _cur.fetchall():
            _fld_val = _row[1]
            _hist_val = _fld_val
            if _fld_val != '':
                _tokenise = m_tokenise.Tokenise()
                _tokens = _tokenise.tokenise_street(_row[1],
                                                    False)

                if accept_substring:
                    _safe_indices = self.check_tokens(sqlite_db, _tokens)
                else:
                    _safe_indices = []
                
                _build_string = ''
                _h_flag = False
                for idx, _token in enumerate(_tokens):

                    if (idx not in _safe_indices) and \
                       ((idx != 0) and (len(_token) >= 2)):

                        _atb_sel = _cur.execute("SELECT Name, Freq FROM Atb WHERE Alias = '%s'"
                                                % (_token)).fetchall()
                        
                        if len(_atb_sel) != 0:
                            _atb_sel = sorted(_atb_sel, key=operator.itemgetter(1),reverse=True)
                            _build_string = _build_string + _atb_sel[0][0] + ' '
                            _h_flag = True
                        else:
                            _build_string = _build_string + _token + ' '
                    else:
                        _build_string = _build_string + _token + ' '

                _build_string = _build_string[:-1]

                # Use flag to avoid to update an address without changes
                if  _h_flag:
                    _cur.execute("UPDATE %s SET %s = '%s' WHERE Id = %i" 
                                % (table_name, 
                                    field_name,
                                    _build_string,
                                    _row[0]))  
                    sqlite_db.conn.commit()
        self.no_number = True

        return self.no_number

    # <check_tokens> method - Search for matching between <STtb> substrings and
    #                         the given tokens. Returns the index of token that
    #                         needs to remain unchanged. 
    # --------------------------------------------------------------------------------- 

    def check_tokens(self, 
                     sqlite_db,
                     _tokens):

        _unchanged_tokens = []
        
        _addr_str = ''
        # Build the address string from tokens       
        for _token in _tokens:
            _addr_str = _addr_str + _token + ' '

        _addr_str = _addr_str[:-1]

        _cur = sqlite_db.rCur()
        _cur.execute('SELECT Name FROM STtb')

        for _name in _cur.fetchall():
            
            if _name[0] in _addr_str:
                _sttb_tokens = _name[0].split()
                result = []
                for i, x in enumerate(_tokens):
                    if (x == _sttb_tokens[0]) and (i != len(_tokens) - 1):
                        result.append(i)
                
                for _index in result:
                    cnt = 0
                    _tokens_match = 1
                    for _stoken in _sttb_tokens[1:]: 
                        cnt += 1 
                        if _stoken == _tokens[_index + cnt]:
                            _tokens_match += 1
                    if _tokens_match == len(_sttb_tokens):
                        for i in range(cnt + 1):
                            _unchanged_tokens.append(_index + i)

        return _unchanged_tokens

    # <clone_table> method - Clones an existing table. 
    # --------------------------------------------------------------------------------- 

    def clone_table(self, 
                    sqlite_db,
                    db_table,
                    new_table):

        _cur = sqlite_db.rCur()
        _cur.execute("DROP TABLE if exists %s" % (new_table,))
        _cur.execute("CREATE TABLE %s AS SELECT * FROM %s" % (new_table, db_table))
        sqlite_db.conn.commit()



