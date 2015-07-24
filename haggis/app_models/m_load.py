# m_load.py - Python classes (Models) for data loading properties and methods.
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

# -------------------------------------------------------------------------------------
# Import necessary modules
import sys
import os
import yaml
import csv
import string
import time
import tqdm

class AppConfig(object):
    """<AppConfig> class for loading application settings.
    """
    # Constructor: Creates the load properties for a given <yaml> configuration 
    # file.
    # ---------------------------------------------------------------------------------
    def __init__(self):
        self.cfg_yaml_file = ''
        ## SQLite database settings
        self.cfg_db_path = ''
        self.cfg_db_schema = ''
        self.cfg_db_indexes = ''
        self.cfg_use_freq_tables = True
        self.cfg_db_freq_tables = True
        self.cfg_db_freq_ctb_limit = 10000
        self.cfg_db_freq_htb_limit = 10000
        # System settings
        #------------------------------------------------------------------------------
        self.cfg_gui = False
        self.cfg_coordinate_system = 0
        self.cfg_srid_code = 27700

        # Paths of CSV files
        #------------------------------------------------------------------------------
        self.cfg_hist_csv = ''
        self.cfg_cont_csv = ''
        self.cfg_accept_csv = ''
        self.cfg_alias_csv = ''
        self.cfg_localities_csv = ''
        self.cfg_towns_csv = ''

        # Field Mapping between 'Ctb' table and contemporary addresses' CSV file
        #------------------------------------------------------------------------------
        self.cfg_ctb_cid = ''
        self.cfg_ctb_name = ''
        self.cfg_ctb_num = ''
        self.cfg_ctb_street = ''
        self.cfg_ctb_cpcode = ''
        self.cfg_ctb_locality = ''
        self.cfg_ctb_town = ''
        self.cfg_ctb_greasting = ''
        self.cfg_ctb_grnorthing = ''
        self.cfg_ctb_distcode = ''

        # Field Mapping between 'Htb' table and historical addresses' CSV file
        #------------------------------------------------------------------------------
        self.cfg_htb_hid = ''
        self.cfg_htb_name = ''
        self.cfg_htb_num = ''
        self.cfg_htb_street = ''
        self.cfg_htb_hpcode = ''
        self.cfg_htb_locality = ''
        self.cfg_htb_town = ''
        self.cfg_htb_hyear = ''
        self.cfg_htb_distcode = ''

        # Field Mapping between 'Atb' table and 'alias_csv' CSV file
        #------------------------------------------------------------------------------
        self.cfg_atb_alias = '' 
        self.cfg_atb_name = ''
        self.cfg_atb_freq = 1

        # Field Mapping between 'STtb' table and 'accept_csv' CSV file
        #------------------------------------------------------------------------------ 
        self.cfg_atb_name = ''

        # Cleaning process settings
        #------------------------------------------------------------------------------
        self.cfg_lcase = True
        self.cfg_strip = True
        self.cfg_punct = False
        self.cfg_rm_address_num = True
        self.cfg_rm_locality = False
        self.cfg_rm_town = False
        self.cfg_rm_ctb_street_duplicates = True
        self.cfg_ctb_group_by_fields = ['Street', 'DistCode']
        self.cfg_rm_htb_street_duplicates = True
        self.cfg_htb_group_by_fields = ['Street', 'DistCode']
        self.cfg_accept_substring = True

        # Tokenisation process settings
        #------------------------------------------------------------------------------
        self.cfg_delimiter = ','
        self.cfg_quote_char = '"'
        self.cfg_rest_key = 'undefined-fieldnames'
        self.cfg_alias = True

        # String distance algorithms
        #------------------------------------------------------------------------------
        self.cfg_init_matching = True
        self.cfg_db_backup = True
        self.cfg_str_distance = 0
        self.cfg_str_set = 2
        self.cfg_matching_threshold = 0.8
        self.cfg_matching_order = 'EXT'
        self.cfg_filter_locality = False
        self.cfg_filter_town = False

        # Spatial process settings
        #------------------------------------------------------------------------------
        self.cfg_sp_run = True
        self.cfg_sp_radius = 500.0
        self.cfg_sp_matching_threshold = 80
        self.cfg_sp_density_threshold = 1
        self.cfg_sp_cent_fill = False

        # Second round matching process settings
        #------------------------------------------------------------------------------
        self.cfg_sec_matching = True
        self.cfg_sec_db_backup = True
        self.cfg_sec_str_distance = 0
        self.cfg_sec_str_set = 2
        self.cfg_sec_matching_threshold = 0.5
        self.cfg_sec_matching_order = 'EXT'
        self.cfg_sec_sp_rd_bb_method = 0

        # Second round Spatial process settings
        #------------------------------------------------------------------------------
        self.cfg_sec_sp_run = True
        self.cfg_sec_sp_radius = 500.0
        self.cfg_sec_sp_matching_threshold = 80
        self.cfg_sec_sp_density_threshold = 1
        self.cfg_sec_sp_cent_fill = False

        # Lists of Field require cleaning
        #------------------------------------------------------------------------------
        self.atb_fields = []
        self.ctb_fields = []
        self.htb_fields = []
        self.sttb_fields = []
    # ---------------------------------------------------------------------------------

    # Load the <yaml> configuration file and set the properties
    # ---------------------------------------------------------------------------------
    def load_yaml_file(self, yaml_path):
        if os.path.exists(yaml_path):
            f = open(yaml_path)
            cfg_data = yaml.safe_load(f)
            f.close()
            
            # SQLite database settings
            self.cfg_yaml_file = yaml_path
            self.cfg_db_path = cfg_data['db_path']
            self.cfg_db_schema = cfg_data['db_schema']
            self.cfg_db_indexes = cfg_data['db_indexes']
            self.cfg_use_freq_tables = cfg_data['use_freq_tables']
            self.cfg_db_freq_tables = cfg_data['db_freq_tables']
            self.cfg_db_freq_ctb_limit = cfg_data['db_freq_ctb_limit']
            self.cfg_db_freq_htb_limit = cfg_data['db_freq_htb_limit']
            

            # System settings
            if cfg_data['gui'] is not None:
                self.cfg_gui = cfg_data['gui']
            if cfg_data['coordinate_system'] is not None:
                self.cfg_coordinate_system = cfg_data['coordinate_system']
            if cfg_data['srid_code'] is not None:
                self.cfg_srid_code = cfg_data['srid_code']
            

            # Paths of CSV files
            self.cfg_hist_csv = cfg_data['hist_csv']
            self.cfg_cont_csv = cfg_data['cont_csv']
            self.cfg_alias_csv = cfg_data['alias_csv']
            self.cfg_accept_csv = cfg_data['accept_csv']
            self.cfg_localities_csv = cfg_data['localities_csv']
            self.cfg_towns_csv = cfg_data['towns_csv']

            # Field Mapping between 'Ctb' table and 'cont_csv' CSV file
            #help_str = ''
            if cfg_data['ctb_cid'] is not None:
                if cfg_data['ctb_cid'].endswith('*'):
                    help_lst = cfg_data['ctb_cid'].split("*")
                    self.cfg_ctb_cid = help_lst[0]
                else:
                    self.cfg_ctb_cid = cfg_data['ctb_cid']
            else:
                self.cfg_ctb_cid = cfg_data['ctb_cid']
            
            if cfg_data['ctb_name'] is not None:
                if cfg_data['ctb_name'].endswith('*'):
                    help_lst = cfg_data['ctb_name'].split("*")
                    self.cfg_ctb_name = help_lst[0]
                    self.ctb_fields.append('Name')
                else:
                    self.cfg_ctb_name = cfg_data['ctb_name']
            else:
                self.cfg_ctb_name = cfg_data['ctb_name']

            if cfg_data['ctb_num'] is not None:
                if  cfg_data['ctb_num'].endswith('*'):
                    help_lst = cfg_data['ctb_num'].split("*")
                    self.cfg_ctb_num = help_lst[0]
                else:
                    self.cfg_ctb_num = cfg_data['ctb_num']
            else:
                self.cfg_ctb_num = cfg_data['ctb_num']
            
            if cfg_data['ctb_street'] is not None:
                if cfg_data['ctb_street'].endswith('*'):
                    help_lst = cfg_data['ctb_street'].split("*")
                    self.cfg_ctb_street = help_lst[0]
                    self.ctb_fields.append('Street')
                else:
                    self.cfg_ctb_street = cfg_data['ctb_street']
            else:
                self.cfg_ctb_street = cfg_data['ctb_street']
            
            if cfg_data['ctb_cpcode'] is not None:
                if cfg_data['ctb_cpcode'].endswith('*'):
                    help_lst = cfg_data['ctb_cpcode'].split("*")
                    self.cfg_ctb_cpcode = help_lst[0]
                    self.ctb_fields.append('CPCode')
                else:
                    self.cfg_ctb_cpcode = cfg_data['ctb_cpcode']
            else:
                self.cfg_ctb_cpcode = cfg_data['ctb_cpcode']
            
            if cfg_data['ctb_locality'] is not None:
                if cfg_data['ctb_locality'].endswith('*'):
                    help_lst = cfg_data['ctb_locality'].split("*")
                    self.cfg_ctb_locality = help_lst[0]
                    self.ctb_fields.append('Locality')
                else:
                    self.cfg_ctb_locality = cfg_data['ctb_locality']
            else:
                self.cfg_ctb_locality = cfg_data['ctb_locality']
            
            if cfg_data['ctb_town'] is not None:
                if cfg_data['ctb_town'].endswith('*'):
                    help_lst = cfg_data['ctb_town'].split("*")
                    self.cfg_ctb_town = help_lst[0]
                    self.ctb_fields.append('Town')
                else:
                    self.cfg_ctb_town = cfg_data['ctb_town']
            else:
                self.cfg_ctb_town = cfg_data['ctb_town']
            
            if cfg_data['ctb_greasting'] is not None:
                if cfg_data['ctb_greasting'].endswith('*'):
                    help_lst = cfg_data['ctb_greasting'].split("*")
                    self.cfg_ctb_greasting = help_lst[0]
                else:
                    self.cfg_ctb_greasting = cfg_data['ctb_greasting']
            else:
                self.cfg_ctb_greasting = cfg_data['ctb_greasting']
            
            if cfg_data['ctb_grnorthing'] is not None:
                if cfg_data['ctb_grnorthing'].endswith('*'):
                    help_lst = cfg_data['ctb_grnorthing'].split("*")
                    self.cfg_ctb_grnorthing = help_lst[0]
                else:
                    self.cfg_ctb_grnorthing = cfg_data['ctb_grnorthing']
            else:
                self.cfg_ctb_grnorthing = cfg_data['ctb_grnorthing']

            if cfg_data['ctb_distcode'] is not None:
                if cfg_data['ctb_distcode'].endswith('*'):
                    help_lst = cfg_data['ctb_distcode'].split("*")
                    self.cfg_ctb_distcode = help_lst[0]
                    self.ctb_fields.append('DistCode')
                else:
                    self.cfg_ctb_distcode = cfg_data['ctb_distcode']
            else:
                self.cfg_ctb_distcode = cfg_data['ctb_distcode']

            # Field Mapping between 'Htb' table and 'hist_csv' CSV file
            if cfg_data['htb_hid'] is not None:
                if cfg_data['htb_hid'].endswith('*'):
                    help_lst = cfg_data['htb_hid'].split("*")
                    self.cfg_htb_hid = help_lst[0]
                else:
                    self.cfg_htb_hid = cfg_data['htb_hid']
            else:
                self.cfg_htb_hid = cfg_data['htb_hid']

            if cfg_data['htb_name'] is not None:
                if cfg_data['htb_name'].endswith('*'):
                    help_lst = cfg_data['htb_name'].split("*")
                    self.cfg_htb_name = help_lst[0]
                    self.htb_fields.append('Name')
                else:
                    self.cfg_htb_name = cfg_data['htb_name']
            else:
                self.cfg_htb_name = cfg_data['htb_name']
            
            if cfg_data['htb_num'] is not None:
                if cfg_data['htb_num'].endswith('*'):
                    help_lst = cfg_data['htb_num'].split("*")
                    self.cfg_htb_num = help_lst[0]
                    self.htb_fields.append('Num')
                else:
                    self.cfg_htb_num = cfg_data['htb_num']
            else:
                self.cfg_htb_num = cfg_data['htb_num']

            if cfg_data['htb_street'] is not None:
                if cfg_data['htb_street'].endswith('*'):
                    help_lst = cfg_data['htb_street'].split("*")
                    self.cfg_htb_street = help_lst[0]
                    self.htb_fields.append('Street')
                else:
                    self.cfg_htb_street = cfg_data['htb_street']
            else:
                self.cfg_htb_street = cfg_data['htb_street']

            if cfg_data['htb_hpcode'] is not None:
                if cfg_data['htb_hpcode'].endswith('*'):
                    help_lst = cfg_data['htb_hpcode'].split("*")
                    self.cfg_htb_hpcode = help_lst[0]
                    self.htb_fields.append('HPCode')
                else:
                    self.cfg_htb_hpcode = cfg_data['htb_hpcode']
            else:
                self.cfg_htb_hpcode = cfg_data['htb_hpcode']

            if cfg_data['htb_locality'] is not None:
                if cfg_data['htb_locality'].endswith('*'):
                    help_lst = cfg_data['htb_locality'].split("*")
                    self.cfg_htb_locality = help_lst[0]
                    self.htb_fields.append('Locality')
                else:
                    self.cfg_htb_locality = cfg_data['htb_locality']
            else:
                self.cfg_htb_locality = cfg_data['htb_locality']

            if cfg_data['htb_town'] is not None:
                if cfg_data['htb_town'].endswith('*'):
                    help_lst = cfg_data['htb_town'].split("*")
                    self.cfg_htb_town = help_lst[0]
                    self.htb_fields.append('Town')
                else:
                    self.cfg_htb_town = cfg_data['htb_town']
            else:
                self.cfg_htb_town = cfg_data['htb_town']
            
            if cfg_data['htb_hyear'] is not None:
                if cfg_data['htb_hyear'].endswith('*'):
                    help_lst = cfg_data['htb_hyear'].split("*")
                    self.cfg_htb_hyear = help_lst[0]
                    self.htb_fields.append('HYear')
                else:
                    self.cfg_htb_hyear = cfg_data['htb_hyear']
            else:
                self.cfg_htb_hyear = cfg_data['htb_hyear']
                 

            if cfg_data['htb_distcode'] is not None:
                if cfg_data['htb_distcode'].endswith('*'):
                    help_lst = cfg_data['htb_distcode'].split("*")
                    self.cfg_htb_distcode = help_lst[0]
                    self.htb_fields.append('DistCode')
                else:
                    self.cfg_htb_distcode = cfg_data['htb_distcode']
            else:
                self.cfg_htb_distcode = cfg_data['htb_distcode']

            # Field Mapping between 'Atb' table and 'alias_csv' CSV file
            if cfg_data['atb_alias'] is not None:
                if cfg_data['atb_alias'].endswith('*'):
                    help_lst = cfg_data['atb_alias'].split("*")
                    self.cfg_atb_alias = help_lst[0]
                    self.atb_fields.append('Alias')
                else:
                    self.cfg_atb_alias = cfg_data['atb_alias']
            else:
                self.cfg_atb_alias = cfg_data['atb_alias']

            if cfg_data['atb_name'] is not None:
                if cfg_data['atb_name'].endswith('*'):
                    help_lst = cfg_data['atb_name'].split("*")
                    self.cfg_atb_name = help_lst[0]
                    self.atb_fields.append('Name')
                else:
                    self.cfg_atb_name = cfg_data['atb_name']
            else:
                self.cfg_atb_name = cfg_data['atb_name']
            
            if cfg_data['atb_freq'] is not None:
                if cfg_data['atb_freq'].endswith('*'):
                    help_lst = cfg_data['atb_freq'].split("*")
                    self.cfg_atb_freq = help_lst[0]
                else:
                    self.cfg_atb_freq = cfg_data['atb_freq']
            else:
                self.cfg_atb_freq = cfg_data['atb_freq']

            # Field Mapping between 'STtb' table and 'accept_csv' CSV file
            if cfg_data['sttb_name'] is not None:
                if cfg_data['sttb_name'].endswith('*'):
                    help_lst = cfg_data['sttb_name'].split("*")
                    self.cfg_sttb_name = help_lst[0]
                    self.sttb_fields.append('Name')
                else:
                    self.cfg_sttb_name = cfg_data['sttb_name']
            else:
                self.cfg_sttb_name = cfg_data['sttb_name']

            # Cleaning process settings
            if cfg_data['lcase'] is not None:
                self.cfg_lcase = cfg_data['lcase']
            if cfg_data['strip'] is not None:
                self.cfg_strip = cfg_data['strip']
            if cfg_data['punct'] is not None:
                self.cfg_punct = cfg_data['punct']

            if cfg_data['rm_address_num'] is not None:
                self.cfg_rm_address_num = cfg_data['rm_address_num']
            if cfg_data['rm_locality'] is not None:
                self.cfg_rm_locality = cfg_data['rm_locality']
            if cfg_data['rm_town'] is not None:
                self.cfg_rm_town = cfg_data['rm_town']
            if cfg_data['rm_ctb_street_duplicates'] is not None:
                self.cfg_rm_ctb_street_duplicates = cfg_data['rm_ctb_street_duplicates']
            if cfg_data['ctb_group_by_fields'] is not None:
                self.cfg_ctb_group_by_fields = cfg_data['ctb_group_by_fields']    
            if cfg_data['rm_htb_street_duplicates'] is not None:
                self.cfg_rm_htb_street_duplicates = cfg_data['rm_htb_street_duplicates']
            if cfg_data['htb_group_by_fields'] is not None:
                self.cfg_htb_group_by_fields = cfg_data['htb_group_by_fields']

            if cfg_data['accept_substring'] is not None:
                self.cfg_accept_substring = cfg_data['accept_substring']
            
            # Tokenisation process settings
            if cfg_data['delimiter'] is not None:
                self.cfg_delimiter = cfg_data['delimiter']
            if cfg_data['quotechar'] is not None:
                self.cfg_quote_char = cfg_data['quotechar']
            if cfg_data['restkey'] is not None:
                self.cfg_rest_key = cfg_data['restkey']
            if cfg_data['alias'] is not None:
                self.cfg_alias = cfg_data['alias']

            # String distance settings
            if cfg_data['init_matching'] is not None:
                self.cfg_init_matching = cfg_data['init_matching']
            if cfg_data['db_backup'] is not None:
                self.cfg_db_backup = cfg_data['db_backup']
            if cfg_data['str_distance'] is not None:
                self.cfg_str_distance = cfg_data['str_distance']
            if cfg_data['str_set'] is not None:
                self.cfg_str_set = cfg_data['str_set']
            if cfg_data['matching_threshold'] is not None:
                self.cfg_matching_threshold = cfg_data['matching_threshold']
            if cfg_data['matching_order'] is not None:
                self.cfg_matching_order = cfg_data['matching_order']
            if cfg_data['filter_locality'] is not None:
                self.cfg_filter_locality = cfg_data['filter_locality']
            if cfg_data['filter_town'] is not None:
                self.cfg_filter_town = cfg_data['filter_town']

            # Spatial process settings
            if cfg_data['sp_run'] is not None:
                self.cfg_sp_run = cfg_data['sp_run']
            if cfg_data['sp_radius'] is not None:
                self.cfg_sp_radius = cfg_data['sp_radius']
            if cfg_data['sp_matching_threshold'] is not None:
                self.cfg_sp_matching_threshold = cfg_data['sp_matching_threshold']
            if cfg_data['sp_density_threshold'] is not None:
                self.cfg_sp_density_threshold = cfg_data['sp_density_threshold']
            if cfg_data['sp_cent_fill'] is not None:
                self.cfg_sp_cent_fill = cfg_data['sp_cent_fill']

            # Second round String distance settings
            if cfg_data['sec_matching'] is not None:
                self.cfg_sec_matching = cfg_data['sec_matching']
            if cfg_data['sec_db_backup'] is not None:
                self.cfg_sec_db_backup = cfg_data['sec_db_backup']
            if cfg_data['sec_str_distance'] is not None:
                self.cfg_sec_str_distance = cfg_data['sec_str_distance']
            if cfg_data['sec_str_set'] is not None:
                self.cfg_sec_str_set = cfg_data['sec_str_set']
            if cfg_data['sec_matching_threshold'] is not None:
                self.cfg_sec_matching_threshold = cfg_data['sec_matching_threshold']
            if cfg_data['sec_matching_order'] is not None:
                self.cfg_sec_matching_order = cfg_data['sec_matching_order']
            if cfg_data['sec_sp_rd_bb_method'] is not None:
                self.cfg_sec_sp_rd_bb_method = cfg_data['sec_sp_rd_bb_method']

            # Second round Spatial process settings
            if cfg_data['sec_sp_run'] is not None:
                self.cfg_sec_sp_run = cfg_data['sec_sp_run']
            if cfg_data['sec_sp_radius'] is not None:
                self.cfg_sec_sp_radius = cfg_data['sec_sp_radius']
            if cfg_data['sec_sp_matching_threshold'] is not None:
                self.cfg_sec_sp_matching_threshold = cfg_data['sec_sp_matching_threshold']
            if cfg_data['sec_sp_density_threshold'] is not None:
                self.cfg_sec_sp_density_threshold = cfg_data['sec_sp_density_threshold']
            if cfg_data['sec_sp_cent_fill'] is not None:
                self.cfg_sec_sp_cent_fill = cfg_data['sec_sp_cent_fill']
        else:
            print ('Please create a new configuration file!')
            print 'sys.argv[0] =', sys.argv[0]
            pathname = os.path.dirname(sys.argv[0]) 
            print 'path =', pathname
            print 'full path =', os.path.abspath(pathname)
    # ---------------------------------------------------------------------------------

class CsvData(object):
    """<csvData> class for loading csv data.
    """
    # Constructor: Initialises the properties of <csvData> instance.
    # ---------------------------------------------------------------------------------
    def __init__(self):
        self.csv_filename = ''
        self.field_names = []
        self.rest_key = ''
        self.delimiter = ''
        self.quote_char = ''
    
    # <load_csv> method - loads the csv data to the SQLite database 
    # ---------------------------------------------------------------------------------   
    def load_csv(self, sqlite_db, table_name, auto_fields):
        if auto_fields is False:
            _csv_fp = open(self.csv_filename, 'rb')
            _csv_fld = []
            # Read csv field names
            for _fld in self.field_names:
                _csv_fld.append(_fld[1])
            # Read the csv file
            _csv_reader = csv.DictReader(_csv_fp, 
                                        delimiter=self.delimiter, 
                                        quotechar=self.quote_char)
            _cur = sqlite_db.rCur()
        
            _current_row = 0
          
            for _row in tqdm.tqdm(_csv_reader,'Progress', _csv_reader.line_num, True):
                _current_row += 1    
                if _current_row == 1: # Skip heading row 
                    continue
                _str_fld = ''
                _str_vals = ''
                if table_name == 'Ctb':
                    if (_row['GridRefEasting'] != '') and (_row['GridRefNorthing'] != ''):
                    # Build the 'fields' and 'values' strings for the sql command
                        for _fld in self.field_names:
                            _str_fld += _fld[0] + ','
                            # TODO: Hardcode field values - bad code below
                            if (_row[_fld[1]].isdigit() and (_fld[1] == 'Freq' or 
                                _fld[1] == 'Cid' or _fld[1] == 'Hid' or 
                                _fld[1] == 'GREasting' or _fld[1] == 'GRNorthing',
                                _fld[1] == 'GridRefEasting' or _fld[1] == 'GridRefGRNorthing')):

                                _str_vals += _row[_fld[1]].replace("'","") + ','
                            else:
                                _str_vals += '\'' + _row[_fld[1]].replace("'","") + '\','
                        _str_fld = _str_fld[:-1]
                        _str_vals = _str_vals[:-1]

                        _str_exec = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name,
                                                                        _str_fld,
                                                                        _str_vals)
                        _cur.execute(_str_exec)
                        
                else:
                    
                    # Build the 'fields' and 'values' strings for the sql command
                    for _fld in self.field_names:
                        _str_fld += _fld[0] + ','

                        # TODO: Hardcode field values - bad code below
                        if (_row[_fld[1]].isdigit() and (_fld[1] == 'Freq' or 
                            _fld[1] == 'Cid' or _fld[1] == 'Hid' or 
                            _fld[1] == 'GREasting' or _fld[1] == 'GRNorthing')):

                            _str_vals += _row[_fld[1]].replace("'","") + ','
                        else:
                            _str_vals += '\'' + _row[_fld[1]].replace("'","") + '\','

                    _str_fld = _str_fld[:-1]
                    _str_vals = _str_vals[:-1]
                    
                    _str_exec = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name,
                                                                    _str_fld,
                                                                    _str_vals)
                    _cur.execute(_str_exec)
                    
        else:
            _csv_fp = open(self.csv_filename, 'rb')
            _csv_reader = csv.DictReader(_csv_fp, 
                                         fieldnames=self.field_names,
                                         restkey=self.rest_key,
                                         delimiter=self.delimiter, 
                                         quotechar=self.quote_char)
            _cur = sqlite_db.rCur()
            _tb_fld_names = list(map(lambda x: x[0], _cur.description))
            _current_row = 0

            for _row in _csv_reader:
                _current_row += 1    
                if _current_row == 1: # Automatically identifies the fieldnames of csv
                    _csv_reader.fieldnames = _row[self.rest_key]
                    continue
                _str_fld = ''
                _str_vals = ''
                for _tb_fld in _tb_fld_names:
                    if _tb_fld != 'Id':
                        _str_fld += _tb_fld + ','
                for _fld in _csv_reader.fieldnames:                  
                    if (_row[_fld].isdigit()) and (_fld.rfind('id')!= -1):
                        _str_vals += _row[_fld] + ','
                    else:
                        _str_vals += '\'' + _row[_fld] + '\','
                _str_fld = _str_fld[:-1]
                _str_vals = _str_vals[:-1]
                _str_exec = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name,
                                                                _str_fld,
                                                                _str_vals)
                _cur.execute(_str_exec)
        sqlite_db.conn.commit()
# -------------------------------------------------------------------------------------