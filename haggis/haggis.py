# haggis.py - Python main file.
#
# Copyright (C) 2014-5 Digitising Scotland Project
#
# Author: Konstantinos Daras <konstantinos.daras@gmail.com>
# Source code: https://github.com/LSCS-Projects/HAGGIS
# Web site: http://lscs-projects.github.io/HAGGIS/
# =================================================================================
#
#  This Source Code is subject to the terms of the GPL 3.0 license. For license
#  information, see http://www.gnu.org/licenses/gpl.html 
#
# =================================================================================

# ---------------------------------------------------------------------------------
# Import necessary modules

import sys
import getopt
import os
import yaml
import time
import subprocess
import app_controllers.c_load as CLoad
import app_controllers.c_clean as CClean
import app_controllers.c_tokenise as CTokenise
import app_controllers.c_match as CMatch
import app_controllers.c_spatial as CSpatial
import db.dbTools as DB


# <main> function - returns the <inputfile> configuration file
# ---------------------------------------------------------------------------------
def main(argv):
   cfgfile = ''
   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
   except getopt.GetoptError:
      print 'haggis.py -i <configfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'haggis.py -i <configfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   return inputfile

# <create_db> function - creates a new database using the given SQL schema 
# ---------------------------------------------------------------------------------
def create_db (cfg_data):
    if cfg_data.cfg_db_schema is not None:

        # Create SQLite database.
        newdb = DB.dbSQLiteManager(cfg_data.cfg_db_path)
        newdb.apply_schema_db(cfg_data.cfg_db_path,
                                cfg_data.cfg_db_schema)
        newdb.apply_indexes_db(cfg_data.cfg_db_path,
                                cfg_data.cfg_db_indexes)

        # Add records to Atb
        if (cfg_data.cfg_atb_alias is None or
            cfg_data.cfg_atb_name is None or
            cfg_data.cfg_atb_freq == 0):

            app_load.load_csv_sqlite(newdb,
                                    cfg_data.cfg_alias_csv,
                                    'Atb',
                                    [],
                                    cfg_data.cfg_rest_key,
                                    cfg_data.cfg_delimiter,
                                    cfg_data.cfg_quote_char,
                                    True)
        else:
            field_list = [('Alias',cfg_data.cfg_atb_alias),
                            ('Name',cfg_data.cfg_atb_name),
                            ('Freq',cfg_data.cfg_atb_freq)]
            app_load.load_csv_sqlite(newdb,
                                    cfg_data.cfg_alias_csv,
                                    'Atb',
                                    field_list,
                                    cfg_data.cfg_rest_key,
                                    cfg_data.cfg_delimiter,
                                    cfg_data.cfg_quote_char,
                                    False)
        # Add records to STtb
        if cfg_data.cfg_sttb_name is None:

            app_load.load_csv_sqlite(newdb,
                                    cfg_data.cfg_accept_csv,
                                    'STtb',
                                    [],
                                    cfg_data.cfg_rest_key,
                                    cfg_data.cfg_delimiter,
                                    cfg_data.cfg_quote_char,
                                    True)
        else:
            field_list = [('Name',cfg_data.cfg_sttb_name)]
            app_load.load_csv_sqlite(newdb,
                                    cfg_data.cfg_accept_csv,
                                    'STtb',
                                    field_list,
                                    cfg_data.cfg_rest_key,
                                    cfg_data.cfg_delimiter,
                                    cfg_data.cfg_quote_char,
                                    False)

        # Add records to Htb
        if cfg_data.cfg_htb_hid == '':

            app_load.load_csv_sqlite(newdb,
                                    cfg_data.cfg_hist_csv,
                                    'Htb',
                                    [],
                                    cfg_data.cfg_rest_key,
                                    cfg_data.cfg_delimiter,
                                    cfg_data.cfg_quote_char,
                                    True)
        else:
            field_list = [('Hid', cfg_data.cfg_htb_hid)]
            if cfg_data.cfg_htb_name is not None:
                field_list.append(('Name', cfg_data.cfg_htb_name))
            if cfg_data.cfg_htb_num is not None:
                field_list.append(('Num', cfg_htb_num))
            if cfg_data.cfg_htb_street is not None:
                field_list.append(('Street', cfg_data.cfg_htb_street))
            if cfg_data.cfg_htb_hpcode is not None:
                field_list.append(('HPCode', cfg_data.cfg_htb_hpcode))
            if cfg_data.cfg_htb_locality is not None:
                field_list.append(('Locality', cfg_data.cfg_htb_locality))
            if cfg_data.cfg_htb_town is not None:
                field_list.append(('Town', cfg_data.cfg_htb_town))
            if cfg_data.cfg_htb_hyear is not None:
                field_list.append(('HYear', cfg_data.cfg_htb_hyear))
            if cfg_data.cfg_htb_distcode is not None:
                field_list.append(('DistCode', cfg_data.cfg_htb_distcode))

            app_load.load_csv_sqlite(newdb,
                                        cfg_data.cfg_hist_csv,
                                        'Htb',
                                        field_list,
                                        cfg_data.cfg_rest_key,
                                        cfg_data.cfg_delimiter,
                                        cfg_data.cfg_quote_char,
                                        False)
        # Add records to Ctb
        if cfg_data.cfg_ctb_cid == '':

            app_load.load_csv_sqlite(newdb,
                                    cfg_data.cfg_cont_csv,
                                    'Ctb',
                                    [],
                                    cfg_data.cfg_rest_key,
                                    cfg_data.cfg_delimiter,
                                    cfg_data.cfg_quote_char,
                                    True)
        else:
            field_list = [('Cid', cfg_data.cfg_ctb_cid)]
            if cfg_data.cfg_ctb_name is not None:
                field_list.append(('Name', cfg_data.cfg_ctb_name))
            if cfg_data.cfg_ctb_num is not None:
                field_list.append(('Num', cfg_ctb_num))
            if cfg_data.cfg_ctb_street is not None:
                field_list.append(('Street', cfg_data.cfg_ctb_street))
            if cfg_data.cfg_ctb_cpcode is not None:
                field_list.append(('CPCode', cfg_data.cfg_ctb_cpcode))
            if cfg_data.cfg_ctb_locality is not None:
                field_list.append(('Locality', cfg_data.cfg_ctb_locality))
            if cfg_data.cfg_ctb_town is not None:
                field_list.append(('Town', cfg_data.cfg_ctb_town))
            if cfg_data.cfg_ctb_greasting is not None:
                field_list.append(('GREasting', cfg_data.cfg_ctb_greasting))
            if cfg_data.cfg_ctb_grnorthing is not None:
                field_list.append(('GRNorthing', cfg_data.cfg_ctb_grnorthing))
            if cfg_data.cfg_ctb_distcode is not None:
                field_list.append(('DistCode', cfg_data.cfg_ctb_distcode))

            app_load.load_csv_sqlite(newdb,
                                        cfg_data.cfg_cont_csv,
                                        'Ctb',
                                        field_list,
                                        cfg_data.cfg_rest_key,
                                        cfg_data.cfg_delimiter,
                                        cfg_data.cfg_quote_char,
                                        False)
        # Close SQLite database
        newdb.close_db()

# <__main__> 
# ---------------------------------------------------------------------------------
if __name__ == "__main__":

    # Load config file
    app_load = CLoad.c_load()
    cfg_data = ''
    cfg_file = os.path.abspath(os.path.dirname(sys.argv[0])) + os.sep + 'config.yaml'
   
    if os.path.exists(cfg_file) == False:
        cfg_file = main(sys.argv[1:])
        cfg_data = app_load.load_yaml_file(os.path.abspath
                                           (os.path.dirname(sys.argv[0])) +
                                            os.sep + cfg_file)
    else:
         cfg_data = app_load.load_yaml_file(cfg_file)
    
    # If True runs a window GUI environment - TODO: To be implemented!!!
    if cfg_data.cfg_gui == False and cfg_data != '':
        
        # Reads an existing database or creates a new one using the given schema
        if cfg_data.cfg_db_schema is not None:
            create_db(cfg_data)

        # Open SQLite database
        if cfg_data.cfg_db_path !='':
            opendb = DB.dbSQLiteManager(cfg_data.cfg_db_path)
            opendb.cur

            # Clean process for Ctb table
            if cfg_data.ctb_fields:
                for fld in cfg_data.ctb_fields:
                    app_clean = CClean.CClean()
                    app_clean.clean_field(opendb,
                                          'Ctb', 
                                          fld, 
                                          cfg_data.cfg_lcase, 
                                          cfg_data.cfg_strip, 
                                          cfg_data.cfg_punct)

            # Clean process for Htb table
            if cfg_data.htb_fields:
                for fld in cfg_data.htb_fields:
                    app_clean = CClean.CClean()
                    app_clean.clean_field(opendb,
                                          'Htb', 
                                          fld, 
                                          cfg_data.cfg_lcase, 
                                          cfg_data.cfg_strip, 
                                          cfg_data.cfg_punct)


            # Clean process for Atb table
            if cfg_data.atb_fields:
                for fld in cfg_data.atb_fields:
                    app_clean = CClean.CClean()
                    app_clean.clean_field(opendb,
                                          'Atb', 
                                          fld, 
                                          cfg_data.cfg_lcase, 
                                          cfg_data.cfg_strip, 
                                          cfg_data.cfg_punct)

            # Clean process for STtb table
            if cfg_data.sttb_fields:
                for fld in cfg_data.sttb_fields:
                    app_clean = CClean.CClean()
                    app_clean.clean_field(opendb,
                                          'STtb', 
                                          fld, 
                                          cfg_data.cfg_lcase, 
                                          cfg_data.cfg_strip, 
                                          cfg_data.cfg_punct)

            # Clean address numbers
            if cfg_data.cfg_rm_address_num:
                app_clean = CClean.CClean()
                app_clean.remove_address_numbers(opendb,
                                                 'Ctb', 
                                                 'Street')
                app_clean.remove_address_numbers(opendb,
                                                 'Htb', 
                                                 'Street')

            # Clean Town information
            if cfg_data.cfg_rm_town:
                app_clean = CClean.CClean()
                app_clean.remove_special_tokens(opendb,
                                                'Htb',
                                                'Street',
                                                'Town',
                                                cfg_data.cfg_towns_csv)

            # Clean Locality information
            if cfg_data.cfg_rm_locality:
                app_clean = CClean.CClean()
                app_clean.remove_special_tokens(opendb,
                                                'Htb',
                                                'Street',
                                                'Locality',
                                                cfg_data.cfg_localities_csv)


            # Clone Htb table
            app_clean = CClean.CClean()
            app_clean.clone_table(opendb,
                                  'Htb', 
                                  'HtbFull')

            # Clone Ctb table
            app_clean.clone_table(opendb,
                                  'Ctb', 
                                  'CtbFull')
            
            # Remove Htb street duplicates
            if cfg_data.cfg_rm_htb_street_duplicates: 
                app_clean = CClean.CClean()
                app_clean.remove_street_duplicates(opendb,
                                                   'Htb',
                                                   cfg_data.cfg_htb_group_by_fields)

            # Remove Ctb street duplicates
            if cfg_data.cfg_rm_ctb_street_duplicates:
                app_clean = CClean.CClean()
                app_clean.remove_street_duplicates(opendb,
                                                   'Ctb',
                                                   cfg_data.cfg_ctb_group_by_fields)
            
            # Build Frequency tables
            if cfg_data.cfg_db_freq_tables:
                app_clean = CMatch.CMatch()
                app_clean.build_freq_table(opendb,
                                           cfg_data.cfg_db_freq_tables,
                                           cfg_data.cfg_db_freq_ctb_limit,
                                           cfg_data.cfg_db_freq_htb_limit,
                                           cfg_data.cfg_alias)

            # Replace aliases
            if cfg_data.cfg_alias:

                app_clean = CClean.CClean()
                app_clean.replace_aliases(opendb,
                                          'Htb',
                                          'Street',
                                          cfg_data.cfg_accept_substring)

                app_clean.replace_aliases(opendb,
                                          'HtbFull',
                                          'Street',
                                          cfg_data.cfg_accept_substring)


            opendb.close_db()
            if cfg_data.cfg_init_matching:
                opendb = DB.dbSQLiteManager(cfg_data.cfg_db_path)
            
                _cur = opendb.rCur()

                _start_timer = time.time() # Timer
                _cur.execute('VACUUM')
                print ('VACUUM Time: ' + str(time.time() - _start_timer))  # Timer

                app_match = CMatch.CMatch()

                _start_timer = time.time() # Timer
                app_match.matching_addressess(opendb, 
                                              cfg_data.cfg_str_distance,
                                              cfg_data.cfg_str_set,
                                              cfg_data.cfg_matching_threshold,
                                              cfg_data.cfg_alias,
                                              cfg_data.cfg_use_freq_tables,
                                              cfg_data.cfg_db_freq_tables,
                                              cfg_data.cfg_db_freq_ctb_limit,
                                              cfg_data.cfg_db_freq_htb_limit,
                                              False,
                                              False)
                print ('Matching Process Time: ' + str(time.time() - _start_timer))  # Timer

                # Close SQLite database
                opendb.close_db()

            if cfg_data.cfg_sp_run:
                opendb = DB.dbSQLiteManager(cfg_data.cfg_db_path)

                _cur = opendb.rCur()
                _start_timer = time.time() # Timer
                _cur.execute('VACUUM')
                print ('VACUUM Time: ' + str(time.time() - _start_timer))  # Timer

                if cfg_data.cfg_db_backup:
                    opendb.backup_db(cfg_data.cfg_db_path, '_before_1stMatch')

                opendb.open_db(cfg_data.cfg_db_path)

                # Initialise Spatial-SQLite database (use of Spatialite)
                opendb.init_spatial_db()

                # Update database with spatial tables/columns
                opendb.update_spatial_db(cfg_data.cfg_srid_code)

                # Initialise Thiessen table
                opendb.init_thiessen_tbl(cfg_data.cfg_srid_code)

                # Initialise LUT_Regions table
                opendb.init_regions_tbl()

                app_spatial = CSpatial.CSpatial()
                app_spatial.update_geometry_txt(opendb,
                                                'Ttb',
                                                'Id',
                                                'Ttb',
                                                'Id',
                                                'GREasting',
                                                'GRNorthing',
                                                'Geometry',
                                                'POINT',
                                                cfg_data.cfg_srid_code)

                app_spatial.update_thiessen(opendb,
                                            False,
                                            'Unique_Points',
                                            'Geometry',
                                            'Thiessen',
                                            'Geometry',
                                            cfg_data.cfg_srid_code)

                app_spatial.intersection_point_in_poly(opendb,
                                                       False,
                                                      'Ttb',
                                                      'Geometry',
                                                      'Id',
                                                      'ThiesId',
                                                      'Thiessen',
                                                      'Geometry',
                                                      'ThiesId')

                app_spatial.assign_density_region_codes(opendb,
                                                        'Ttb',
                                                        'Geometry',
                                                        'Id',
                                                        'DistCode',
                                                        'AssignedCode',
                                                        'AssignedDens',
                                                        'ThiesId',
                                                        'Thiessen',
                                                        'ThiesId',
                                                        'RegionId',
                                                        cfg_data.cfg_sp_radius,
                                                        cfg_data.cfg_sp_matching_threshold,
                                                        cfg_data.cfg_sp_density_threshold)
            
            if cfg_data.cfg_sec_matching:
                opendb = DB.dbSQLiteManager(cfg_data.cfg_db_path)

                _cur = opendb.rCur()
                _start_timer = time.time() # Timer
                _cur.execute('VACUUM')
                print ('VACUUM Time: ' + str(time.time() - _start_timer))  # Timer

                if cfg_data.cfg_sec_db_backup:
                    opendb.backup_db(cfg_data.cfg_db_path, '_before_2ndMatch')

                opendb.open_db(cfg_data.cfg_db_path)
             
                app_match = CMatch.CMatch()

                _start_timer = time.time() # Timer
                app_match.sec_matching(opendb,
                                       'GREasting',
                                       'GRNorthing',
                                       'DistCode',
                                       cfg_data.cfg_sec_str_distance,
                                       cfg_data.cfg_sec_str_set,
                                       cfg_data.cfg_sec_matching_threshold,
                                       cfg_data.cfg_sec_sp_rd_bb_method)

                print ('Second Round of Matching Process Time: ' + str(time.time() - _start_timer))  # Timer

                # Spatial Analysis 2nd Round --------------------------------------------------------------
                
                # Initialise Thiessen table
                opendb.init_thiessen_tbl(cfg_data.cfg_srid_code)

                # Initialise LUT_Regions table
                opendb.init_regions_tbl()

                app_spatial = CSpatial.CSpatial()
                app_spatial.update_geometry_txt(opendb,
                                                'Ttb',
                                                'Id',
                                                'Ttb',
                                                'Id',
                                                'GREasting',
                                                'GRNorthing',
                                                'Geometry',
                                                'POINT',
                                                cfg_data.cfg_srid_code)

                app_spatial.update_thiessen(opendb,
                                            False,
                                            'Unique_Points',
                                            'Geometry',
                                            'Thiessen',
                                            'Geometry',
                                            cfg_data.cfg_srid_code)

                app_spatial.intersection_point_in_poly(opendb,
                                                       False,
                                                      'Ttb',
                                                      'Geometry',
                                                      'Id',
                                                      'ThiesId',
                                                      'Thiessen',
                                                      'Geometry',
                                                      'ThiesId')

                app_spatial.assign_density_region_codes(opendb,
                                                        'Ttb',
                                                        'Geometry',
                                                        'Id',
                                                        'DistCode',
                                                        'AssignedCode',
                                                        'AssignedDens',
                                                        'ThiesId',
                                                        'Thiessen',
                                                        'ThiesId',
                                                        'RegionId',
                                                        cfg_data.cfg_sec_sp_radius,
                                                        cfg_data.cfg_sec_sp_matching_threshold,
                                                        cfg_data.cfg_sec_sp_density_threshold)



                # Close SQLite database
                opendb.close_db()

        else:
            print ('ERROR: Missing database path in the <config.yaml> file.')
            print ('Please set up the database path!')


    else:
        subprocess.Popen("python C:\Repos\HAG\hag\start_gui.py", shell=True)