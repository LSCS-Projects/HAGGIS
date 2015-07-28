# m_match.py - Python class (Model) for string matching properties and methods.
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
import sqlite3
import collections
import itertools
import operator
import csv

from Levenshtein import setratio, distance
from app_models import m_tokenise, m_spatial
import cProfile

class Match(object):
    """<Match> class for matching the <Htb> and <Ctb> address tokens
    """
    # Constructor: Initialises the properties of <Match> instance.
    # ---------------------------------------------------------------------------------
    def __init__(self):
        self.ctb_freq_tokens = []
        self.htb_freq_tokens = []

    # PROFILER................................
    def do_cprofile(func):
        def profiled_func(*args, **kwargs):
            profile = cProfile.Profile()
            try:
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                return result
            finally:
                profile.print_stats()
        return profiled_func
    # PROFILER................................

    # <matching_tokens> method - Matching the <Htb> and <Ctb>/<Ttb> address tokens.
    # ---------------------------------------------------------------------------------   
    #@do_cprofile    
    def matching_tokens(self, 
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

        if freq_tables:
            self.build_freq_tables(sqlite_db,
                                   freq_tables,
                                   freq_ctb_limit,
                                   freq_htb_limit,
                                   use_alias)

        _cur = sqlite_db.rCur()
        # Select all RowID from Htb table
        _htb_ids = _cur.execute('SELECT Id, Locality, Town FROM Htb').fetchall()        

        _num_matches = 0

        # Create virtual table for Ctb.
        con = sqlite3.connect(":memory:")
        con.execute("CREATE VIRTUAL TABLE CtbMem USING fts3(Name,Street,Locality,Town)")

        # Copy Ctb records to the new virtual table.
        _cur.execute('SELECT Id,Name,Street,Locality,Town FROM Ctb') 
        _ctb_ids = _cur.fetchall()

        for _ctb_row in _ctb_ids:
            _str_fld = 'docid,Name,Street,Locality,Town'
            _str_vals = str(_ctb_row[0]) + ','
            _str_vals += '\'' + _ctb_row[1] + '\','
            _str_vals += '\'' + _ctb_row[2] + '\','
            _str_vals += '\'' + _ctb_row[3] + '\','
            _str_vals += '\'' + _ctb_row[4] + '\''

            _str_exec = 'INSERT INTO %s (%s) VALUES (%s)' % ('CtbMem',
                                                              _str_fld,
                                                              _str_vals) 
            con.execute(_str_exec)

        #_ctb_mem_ids = con.execute('SELECT * FROM CtbMem') 

        if use_freq_tables:
            # Select tokens with freq > freq_htb_limit
            _cur.execute("SELECT Token FROM HtbFreq WHERE Freq >?", (freq_htb_limit,)) 
            _freq_htb_tokens = _cur.fetchall()
        else:
            # Select all tokens
            _cur.execute("SELECT Token FROM HtbFreq") 
            _freq_htb_tokens = _cur.fetchall()

        _freq_tokens = []
        for _token in _freq_htb_tokens:
            _freq_tokens.append(_token[0]) 
        
        _tuple_ids = []
        _unmatched_ids = []

        _cnt_htb_row = 0

        # For each row in Htb
        for _htb_row in _htb_ids:
            _cnt_htb_row += 1
            _htb_tokenise = m_tokenise.Tokenise()
            _htb_tokenise.tokenise_address(sqlite_db,
                                            'Htb', 
                                            _htb_row[0],
                                            False,
                                            False,
                                            True,
                                            False,
                                            False,
                                            False)

            if _htb_tokenise.is_tokenised:
                
                _tot_ids = []
                _tot_token = ''
                for  _token in _htb_tokenise.tokens:
                    if (len(_token) > 0) and (_token not in _freq_tokens):
                        _tot_token = _tot_token + _token + ' OR '
                _tot_token = _tot_token[:-4]
                _tot_token = '\'' + _tot_token + '\''
                if (filter_locality == True) and (filter_town == True):
                    _ctb_ids = con.execute("SELECT docid FROM CtbMem WHERE Street MATCH %s AND \
                                            Locality = '%s' AND Town = '%s'" % (_tot_token,
                                                                                _htb_row[1],
                                                                                _htb_row[2])).fetchall()
                elif (filter_locality == True) and (filter_town == False):
                    _ctb_ids = con.execute("SELECT docid FROM CtbMem WHERE Street MATCH %s AND \
                                            Locality = '%s'" % (_tot_token,
                                                                _htb_row[1])).fetchall()
                elif (filter_locality == False) and (filter_town == True):
                    _ctb_ids = con.execute("SELECT docid FROM CtbMem WHERE Street MATCH %s AND \
                                            Town = '%s'" % (_tot_token,
                                                            _htb_row[2])).fetchall()
                else:
                    _ctb_ids = con.execute("SELECT docid FROM CtbMem WHERE Street MATCH %s" % (_tot_token,)).fetchall()

                    
                if _ctb_ids == []:
                    # Select RowIDs from Ctb table (use Name)
                    _ctb_ids = con.execute("SELECT docid FROM CtbMem WHERE Name MATCH %s" % (_tot_token,)).fetchall()
                
                _no_ids = False
                if _ctb_ids == []:
                    # Raise True for empty id list
                    _no_ids = True
                    
                    
                _scores = {}       
                _cnt = len(_ctb_ids)
                print(str(_cnt_htb_row) + ': ' + str(_cnt) + ' M:' + str(_num_matches))
                if not _no_ids:
                    # For each row in Ctb       
                    for _ctb_row in _ctb_ids:
                                              
                        _ctb_tokenise = m_tokenise.Tokenise()
                        if (_htb_row[1] is None) and (_htb_row[2] is None):
                            _ctb_tokenise.tokenise_address(sqlite_db,
                                                           'Ctb', 
                                                           _ctb_row[0],
                                                           True,
                                                           False,
                                                           True,
                                                           True,
                                                           True,
                                                           False)
                        else:
                            _ctb_tokenise.tokenise_address(sqlite_db,
                                                           'Ctb', 
                                                           _ctb_row[0],
                                                           True,
                                                           False,
                                                           True,
                                                           False,
                                                           False,
                                                           False)
                         
                        _tmp_score = self.matching_distance(_htb_tokenise.tokens,
                                                            _ctb_tokenise.tokens,
                                                            0)
                         
                        if _tmp_score == 1:
                            _scores.update({_ctb_row[0] : _tmp_score * 100})
                            break
                        elif _tmp_score >= matching_threshold:
                            _scores.update({_ctb_row[0] : _tmp_score * 100})

                    if len(_scores) > 0:
                        _max_score_row = max(_scores, key=_scores.get)
                        _max_score_val = _scores[_max_score_row]
                        _tuple_ids.append((_htb_row[0], 
                                           _max_score_row, 
                                           _max_score_val))
                        _num_matches += 1
                    else:
                        _unmatched_ids.append(_htb_row[0])
                        _max_score_row = 0
                        _max_score_val = 0
  
                    # 
                    # Write automated matching results to <Ttb> table
                    if len(_tuple_ids) > 1000:
                        # Matched addresses
                        for _ids in _tuple_ids:
                            _htb_data = _cur.execute("SELECT * FROM Htb WHERE Id = ?", (_ids[0],)).fetchall()
                            _ctb_data = _cur.execute("SELECT * FROM Ctb WHERE Id = ?", (_ids[1],)).fetchall()
                            _cur.execute("INSERT INTO Stb (Name,Street,HPCode,Locality,Town) VALUES (?,?,?,?,?)", 
                                         (str(_htb_data[0][2]),
                                          str(_htb_data[0][4]),
                                          str(_htb_data[0][5]),
                                          str(_ctb_data[0][6]),
                                          str(_ctb_data[0][7])))
                            _ins_record = _cur.execute("SELECT SNId FROM Stb ORDER BY SNId DESC LIMIT 1").fetchall()
                            _cur.execute("INSERT INTO Ttb (Cid,Hid,Num,SNId,CPCode,GREasting,GRNorthing, \
                                          StartYear,AutoEval,DistCode,Status) VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
                                          (_ctb_data[0][1],
                                           _htb_data[0][1],
                                           str(_htb_data[0][3]),
                                           _ins_record[0][0],
                                           str(_ctb_data[0][5]),
                                           _ctb_data[0][8],
                                           _ctb_data[0][9],
                                           str(_htb_data[0][8]),
                                           (_ids[2]),
                                           str(_htb_data[0][9]),
                                           100))
                        print('Partial save of 1000 matches!')
                        
                        # Empty 1000 matches list
                        _tuple_ids = [] 

                    if len(_unmatched_ids) > 1000:
                        # Unmatched addresses
                        for _ids in _unmatched_ids:
                            _htb_data = _cur.execute("SELECT * FROM Htb WHERE Id = ?", (_ids,)).fetchall()
                            _cur.execute("INSERT INTO Stb (Name,Street,HPCode) VALUES (?,?,?)", 
                                         (str(_htb_data[0][2]),
                                          str(_htb_data[0][4]),
                                          str(_htb_data[0][5])))
                            _ins_record = _cur.execute("SELECT SNId FROM Stb ORDER BY SNId DESC LIMIT 1").fetchall()
                            _cur.execute("INSERT INTO Ttb (Hid,Num,SNId, \
                                          StartYear,AutoEval,DistCode,Status) VALUES (?,?,?,?,?,?,?)", 
                                          (_htb_data[0][1],
                                           str(_htb_data[0][3]),
                                           _ins_record[0][0],
                                           str(_htb_data[0][8]),
                                           0,
                                           str(_htb_data[0][9]),
                                           101))
                        sqlite_db.conn.commit()
                        print('Partial save of 1000 matches!')
                        
                        # Empty 1000 no-matches list
                        _unmatched_ids = []
                else:
                    _unmatched_ids.append(_htb_row[0])
                
            else:
                _unmatched_ids.append(_htb_row[0])

        # Write the last set of automated matching results to <Ttb> table
        if len(_tuple_ids) > 0:
            # Matched addresses
            for _ids in _tuple_ids:
                _htb_data = _cur.execute("SELECT * FROM Htb WHERE Id = ?", (_ids[0],)).fetchall()
                _ctb_data = _cur.execute("SELECT * FROM Ctb WHERE Id = ?", (_ids[1],)).fetchall()
                _cur.execute("INSERT INTO Stb (Name,Street,HPCode,Locality,Town) VALUES (?,?,?,?,?)", 
                                (str(_htb_data[0][2]),
                                str(_htb_data[0][4]),
                                str(_htb_data[0][5]),
                                str(_ctb_data[0][6]),
                                str(_ctb_data[0][7])))
                _ins_record = _cur.execute("SELECT SNId FROM Stb ORDER BY SNId DESC LIMIT 1").fetchall()
                _cur.execute("INSERT INTO Ttb (Cid,Hid,Num,SNId,CPCode,GREasting,GRNorthing, \
                                StartYear,AutoEval,DistCode,Status) VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
                                (_ctb_data[0][1],
                                _htb_data[0][1],
                                str(_htb_data[0][3]),
                                _ins_record[0][0],
                                str(_ctb_data[0][5]),
                                _ctb_data[0][8],
                                _ctb_data[0][9],
                                str(_htb_data[0][8]),
                                (_ids[2]),
                                str(_htb_data[0][9]),
                                100))
            sqlite_db.conn.commit()

        if len(_unmatched_ids) > 0:
            # Unmatched addresses
            for _ids in _unmatched_ids:
                _htb_data = _cur.execute("SELECT * FROM Htb WHERE Id = ?", (_ids,)).fetchall()
                _cur.execute("INSERT INTO Stb (Name,Street,HPCode) VALUES (?,?,?)", 
                                (str(_htb_data[0][2]),
                                str(_htb_data[0][4]),
                                str(_htb_data[0][5])))
                _ins_record = _cur.execute("SELECT SNId FROM Stb ORDER BY SNId DESC LIMIT 1").fetchall()
                _cur.execute("INSERT INTO Ttb (Hid,Num,SNId, \
                                StartYear,AutoEval,DistCode,Status) VALUES (?,?,?,?,?,?,?)", 
                                (_htb_data[0][1],
                                str(_htb_data[0][3]),
                                _ins_record[0][0],
                                str(_htb_data[0][8]),
                                0,
                                str(_htb_data[0][9]),
                                101))
                        
            sqlite_db.conn.commit()
        print('Save the last set of address matches!')

        # Create HEvents column and update with num of events using <Htb> table - 
        # <CntEvents> column
        #

        print('Create HEvents column and update...')

        # Add CntEvents column to the table
        _cur.execute('ALTER TABLE Ttb ADD COLUMN HEvents INTEGER')
        sqlite_db.conn.commit()

        # Select <Hid> records in <Ttb> table
        tids_recs = _cur.execute('SELECT Id, HId, DistCode, StartYear FROM Ttb').fetchall() 

        for tid in tids_recs:
            hid_rec  = _cur.execute("SELECT HId, DistCode, CntEvents FROM Htb \
                                        WHERE Hid = '%s' AND DistCode = '%s' AND \
                                        HYear = '%s'" % 
                                        (str(tid[1]), tid[2], tid[3])).fetchall()

            if len(hid_rec) == 1:
                _cur.execute('UPDATE Ttb SET HEvents = %i WHERE Id = %i' %  
                                (hid_rec[0][2],tid[0])) 
        sqlite_db.conn.commit()

    # <matching_sec_run> method - Second Round of Matching the unmatched <Ttb> addresses.
    # ---------------------------------------------------------------------------------   
    #@do_cprofile    
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

        _cur = sqlite_db.rCur()

        # Get bounding box coordinates of study area
        x_min_base = _cur.execute('SELECT MIN(%s) FROM Ctb' % (ctb_easting,)).fetchall()[0][0]
        y_min_base = _cur.execute('SELECT MIN(%s) FROM Ctb' % (ctb_northing,)).fetchall()[0][0]
        x_max_base = _cur.execute('SELECT MAX(%s) FROM Ctb' % (ctb_easting,)).fetchall()[0][0] 
        y_max_base = _cur.execute('SELECT MAX(%s) FROM Ctb' % (ctb_northing,)).fetchall()[0][0]


        if rd_bb_method == 1:
            # Get Thiessen centroids
            _thies_centroids = _cur.execute("SELECT RegionId, X(ST_Centroid(Geometry)), Y(ST_Centroid(Geometry)) \
                                             FROM Thiessen WHERE RegionId IS NOT NULL AND MbrMinX(Geometry) > %s \
                                              AND MbrMinY(Geometry) > %s AND MbrMaxX(Geometry) < %s \
                                              AND MbrMaxY(Geometry) < %s" % 
                                              (x_min_base,
                                               y_min_base,
                                               x_max_base,
                                               y_max_base)).fetchall()

            # Aggregate Thiessen centroids grouped by RD code
            lst = []
            lst = itertools.groupby(sorted(_thies_centroids, key=operator.itemgetter(0)),
                    key=operator.itemgetter(0))
            lst_res = []
            for key, item in lst:
                tmp_x = 0
                tmp_y = 0
                cnt = 0
                for i in item:
                    if i[0] == '1':
                        print('X:'+ str(i[1]) + ' Y:' + str(i[2]))
                    cnt += 1
                    tmp_x += i[1]
                    tmp_y += i[2]
                lst_res.append((key,tmp_x/cnt, tmp_y/cnt))
            
            # Create spatial db (in memory)
            mem_conn = sqlite3.connect(":memory:")
            mem_conn.enable_load_extension(True)
            mem_conn.execute('SELECT load_extension("libspatialite-4.dll")')
            #test = mem_conn.execute('SELECT spatialite_version()').fetchall()
            mem_cur = mem_conn.cursor()
            mem_cur.execute(r'SELECT InitSpatialMetaData()')

            # Create thiessen table (in memory)
            mem_cur.execute("CREATE TABLE Thiessen ( \
                          ThiesId integer NOT NULL PRIMARY KEY AUTOINCREMENT, \
                          RegionId text)")
            mem_cur.execute("SELECT AddGeometryColumn('Thiessen', 'Geometry', 27700, \
                              'POLYGON', 'XY')")
            mem_cur.execute("SELECT CreateSpatialIndex('Thiessen', 'Geometry')")
            mem_cur.execute("CREATE INDEX Thiessen_idx_Id ON Thiessen (ThiesId ASC)")

            # Create thiessen centroids table (in memory)
            mem_cur.execute("CREATE TABLE ThiesCent ( \
                          Id integer NOT NULL PRIMARY KEY AUTOINCREMENT, \
                          ThiesId integer, RegionId text)")
            mem_cur.execute("SELECT AddGeometryColumn('ThiesCent', 'Geometry', 27700, \
                              'POINT', 'XY')")
            mem_cur.execute("SELECT CreateSpatialIndex('ThiesCent', 'Geometry')")
            mem_cur.execute("CREATE INDEX ThiesCent_idx_Id ON ThiesCent (Id ASC)")

            # Add RD-region's centroids
            for reg, tmpX, tmpY in lst_res:
                _poly_txt = str(tmpX) + ' ' + str(tmpY)
                mem_cur.execute("INSERT INTO ThiesCent (Id, ThiesId, Geometry, RegionId) \
                                VALUES (NULL, 0, ST_GeomFromText('%s(%s)', %s), '%s')" \
                                % ('POINT',
                                   _poly_txt,
                                   27700,
                                   reg))
            mem_conn.commit()

            ld_sp = m_spatial.SpatialTools()

            ld_sp.update_thiessen(mem_conn,
                                  True,
                                  'ThiesCent',
                                  'Geometry',
                                  'Thiessen',
                                  'Geometry',
                                  27700)
            ld_sp.intersection_point_in_poly(mem_conn,
                                             True,
                                            'ThiesCent',
                                            'Geometry',
                                            'Id',
                                            'ThiesId',
                                            'Thiessen',
                                            'Geometry',
                                            'ThiesId')

            # Get bounding box coordinates for each RD region
            # <bbox_rds>: list of tuples e.g. [(x1_min, y1_min, x1_max, y1_max), 
            #                                  (x2_min, y2_min, x2_max, y2_max)]
            bbox_rds = []
        
            _rd_codes = mem_cur.execute('SELECT Id, ThiesId, RegionId FROM ThiesCent').fetchall()

            out_path = 'C:/Repos/HAG/data/RD_Centroids.csv'
            ofile  = open(out_path, "wb")
            writer = csv.writer(ofile, delimiter=',', quoting=csv.QUOTE_NONE )
            writer.writerow(['RD_ID','Xcoord','Ycoord'])

            for _rd_code in _rd_codes:
                if _rd_code[1] is not None:
                    #Export RD centroids
                    _out_xy = mem_cur.execute("SELECT RegionId, X(Geometry), Y(Geometry) \
                                               FROM ThiesCent WHERE ThiesId = %s" % (_rd_code[1],)).fetchone()
                    writer.writerow(_out_xy)
                    #--------------------

                    _rd_min_xy = mem_cur.execute("SELECT  MbrMinX(Geometry), MbrMinY(Geometry) FROM Thiessen \
                                                  WHERE ThiesId = %s" % (_rd_code[1],)).fetchone()

                    lst_min = list(_rd_min_xy)

                    if _rd_min_xy[0] < x_min_base:
                        lst_min[0] = x_min_base

                    if _rd_min_xy[1] < y_min_base:
                        lst_min[1] = y_min_base
                
                    _rd_max_xy = mem_cur.execute("SELECT MbrMaxX(Geometry), MbrMaxY(Geometry) FROM Thiessen \
                                                  WHERE ThiesId = %s" % (_rd_code[1],)).fetchone()
                    
                    lst_max = list(_rd_max_xy)

                    if _rd_max_xy[0] > x_max_base:
                        lst_max[0] = x_max_base

                    if _rd_max_xy[1] > y_max_base:
                        lst_max[1] = y_max_base

                    bbox_rds.append((_rd_code[2], lst_min[0], lst_min[1], lst_max[0], lst_max[1]))

            ofile.close()


        if (rd_bb_method == 0) or (rd_bb_method > 1):
            # Get bounding box coordinates for each RD region
            # <bbox_rds>: list of tuples e.g. [(x1_min, y1_min, x1_max, y1_max), 
            #                                  (x2_min, y2_min, x2_max, y2_max)]
            bbox_rds = []
        
            _rd_codes = _cur.execute('SELECT DISTINCT RegionId FROM Thiessen').fetchall()

            for _rd_code in _rd_codes:
                if _rd_code[0] is not None:
                    _rd_min_xy = _cur.execute("SELECT  MbrMinX(Geometry), MbrMinY(Geometry) FROM Thiessen \
                                              WHERE RegionId = '%s' AND MbrMinX(Geometry) > %s \
                                              AND MbrMinY(Geometry) > %s" % 
                                              (_rd_code[0], 
                                               x_min_base,
                                               y_min_base)).fetchall()

                    xy_min = map(min, zip(*_rd_min_xy))
                
                    _rd_max_xy = _cur.execute("SELECT MbrMaxX(Geometry), MbrMaxY(Geometry) FROM Thiessen \
                                              WHERE RegionId = '%s' AND MbrMaxX(Geometry) < %s \
                                              AND MbrMaxY(Geometry) < %s" % 
                                              (_rd_code[0], 
                                               x_max_base,
                                               y_max_base)).fetchall()

                    xy_max = map(max, zip(*_rd_max_xy))

                    if xy_max and xy_min:
                        bbox_rds.append((_rd_code[0], xy_min[0], xy_min[1], xy_max[0], xy_max[1]))

        
        for _rd in bbox_rds:

            rd_pointer = bbox_rds.index(_rd)

            # Select all IDs from Htb table
            _ttb_ids = _cur.execute("SELECT Id, Hid, StartYear FROM Ttb WHERE DistCode = '%s' \
                                     AND (AssignedCode IS NULL OR AssignedCode <> DistCode)" % (_rd[0],)).fetchall()  
                  
            _num_matches = 0

            # Create virtual table for Ctb.
            con = sqlite3.connect(":memory:")
            con.execute("CREATE VIRTUAL TABLE CtbMem USING fts3(Name,Street)")

            # Copy Ctb records to the new virtual table.
            _cur.execute('SELECT Id,Name,Street FROM Ctb WHERE GREasting > %s AND \
                          GREasting < %s AND GRNorthing > %s AND GRNorthing < %s' %
                          (_rd[1],_rd[3],_rd[2],_rd[4])) 
            _ctb_ids = _cur.fetchall()

            for _ctb_row in _ctb_ids:
                _str_fld = 'docid,Name,Street'
                _str_vals = str(_ctb_row[0]) + ','
                _str_vals += '\'' + _ctb_row[1] + '\','
                _str_vals += '\'' + _ctb_row[2] + '\''

                _str_exec = 'INSERT INTO %s (%s) VALUES (%s)' % ('CtbMem',
                                                                  _str_fld,
                                                                  _str_vals) 
                con.execute(_str_exec)

            _ctb_mem_ids = con.execute('SELECT * FROM CtbMem') 

      
            _tuple_ids = []
            _unmatched_ids = []

            _cnt_ttb_row = 0

            # For each row in Ttb subset
            for _ttb_row in _ttb_ids:
                _cnt_ttb_row += 1
                _htb_row = _cur.execute("SELECT Id FROM Htb WHERE Hid = %s AND HYear = '%s' \
                                         AND DistCode = '%s'" % (_ttb_row[1], _ttb_row[2], _rd[0])).fetchall()
                _htb_tokenise = m_tokenise.Tokenise()
                _htb_tokenise.tokenise_address(sqlite_db,
                                                 'Htb', 
                                                 _htb_row[0][0],
                                                 True,
                                                 False,
                                                 True,
                                                 False,
                                                 False, 
                                                 False)
                if _htb_tokenise.is_tokenised:
                
                    _tot_ids = []
                    _tot_token = ''
                    for  _token in _htb_tokenise.tokens:
                        if (len(_token) > 2) :
                            _tot_token = _tot_token + _token + ' OR '
                    _tot_token = _tot_token[:-4]
                    _tot_token = '\'' + _tot_token + '\''
                    _ctb_ids = con.execute("SELECT docid, Name, Street FROM CtbMem WHERE Street MATCH ?",
                                           (_tot_token,)).fetchall()

                    
                    if _ctb_ids == []:
                        # Select RowIDs from Ctb table (use Locality)
                        _ctb_ids = con.execute("SELECT docid, Name, Street FROM CtbMem WHERE Name MATCH ?",
                                               (_tot_token,)).fetchall()
                
                    _no_ids = False
                    if _ctb_ids == []:
                        # Raise True for empty id list
                        _no_ids = True
                    
                    
                    _scores = {}       
                    _cnt = len(_ctb_ids)
                    print(str(rd_pointer + 1) + '|' + str(_cnt_ttb_row) + ': ' + str(_cnt) + ' M:' + str(_num_matches))
                    if not _no_ids:
                        # For each row in Ctb       
                        for _ctb_row in _ctb_ids:
                                              
                            _ctb_tokenise = m_tokenise.Tokenise()
                            _ctb_tokenise.tokenise_mem_address(con,
                                                               'CtbMem', 
                                                                _ctb_row[0],
                                                                True,
                                                                True,
                                                                False)
                         
                            _tmp_score = self.matching_distance(_htb_tokenise.tokens,
                                                                _ctb_tokenise.tokens,
                                                                0)
                         
                            if _tmp_score == 1:
                                _scores.update({_ctb_row[0] : _tmp_score * 100})
                                break
                            elif _tmp_score >= matching_threshold:
                                _scores.update({_ctb_row[0] : _tmp_score * 100})

                        if len(_scores) > 0:
                            _max_score_row = max(_scores, key=_scores.get)
                            _max_score_val = _scores[_max_score_row]
                            _tuple_ids.append((_ttb_row[0], 
                                               _max_score_row, 
                                               _max_score_val))
                            _num_matches += 1
                        else:
                            _unmatched_ids.append(_ttb_row[0])
                            _max_score_row = 0
                            _max_score_val = 0
  
                         
                        # Write automated matching results to <Ttb> table
                        if len(_tuple_ids) > 100:
                            # Matched addresses
                            for _ids in _tuple_ids:
                                _ttb_data = _cur.execute("SELECT * FROM Ttb WHERE Id = %s" % (_ids[0],)).fetchall()
                                _ctb_data = _cur.execute("SELECT * FROM Ctb WHERE Id = %s" % (_ids[1],)).fetchall()
                                _cur.execute("UPDATE Stb SET Locality = '%s' ,Town = '%s' WHERE SNId = %s" % 
                                             (_ctb_data[0][6],
                                              _ctb_data[0][7],
                                              _ttb_data[0][4]))
                                _cur.execute("UPDATE Ttb SET Cid = %s, CPCode = '%s', GREasting = %s,\
                                              GRNorthing = %s, AutoEval = %s, AssignedCode = '%s', \
                                              Status = %s WHERE Id = %s" % 
                                              (_ctb_data[0][1],
                                               _ctb_data[0][5],
                                               _ctb_data[0][8],
                                               _ctb_data[0][9],
                                               _ids[2],
                                               _rd[0],
                                               200,
                                               _ids[0]))
                            sqlite_db.conn.commit()
                            print('Partial save of 100 matches!')
                        
                            # Empty 1000 matches list
                            _tuple_ids = [] 

                        if len(_unmatched_ids) > 100:
                            # Unmatched addresses
                            for _ids in _unmatched_ids:
                                _cur.execute("UPDATE Ttb SET Status = %s WHERE Id = %s" % 
                                              (201,
                                               _ids))
                            sqlite_db.conn.commit()
                            print('Partial save of 100 no-matches!')
                        
                            # Empty 1000 no-matches list
                            _unmatched_ids = []
                    else:
                        _unmatched_ids.append(_ttb_row[0])
                
                else:
                    _unmatched_ids.append(_ttb_row[0])

            # Write the last set of automated matching results to <Ttb> table

            if _tuple_ids:
                # Matched addresses
                for _ids in _tuple_ids:
                    _ttb_data = _cur.execute("SELECT * FROM Ttb WHERE Id = %s" % (_ids[0],)).fetchall()
                    _ctb_data = _cur.execute("SELECT * FROM Ctb WHERE Id = %s" % (_ids[1],)).fetchall()
                    _cur.execute("UPDATE Stb SET Locality = '%s' ,Town = '%s' WHERE SNId = %s" % 
                                    (_ctb_data[0][6],
                                    _ctb_data[0][7],
                                    _ttb_data[0][4]))
                    _cur.execute("UPDATE Ttb SET Cid = %s, CPCode = '%s', GREasting = %s,\
                                    GRNorthing = %s, AutoEval = %s, AssignedCode = '%s', \
                                    Status = %s WHERE Id = %s" % 
                                    (_ctb_data[0][1],
                                    _ctb_data[0][5],
                                    _ctb_data[0][8],
                                    _ctb_data[0][9],
                                    _ids[2],
                                    _rd[0],
                                    200,
                                    _ids[0]))
                sqlite_db.conn.commit()

            if _unmatched_ids:
                # Unmatched addresses
                for _ids in _unmatched_ids:
                    _cur.execute("UPDATE Ttb SET Status = ? WHERE Id = ?", 
                                 (201,
                                 _ids))
                sqlite_db.conn.commit()
            print('Save the last set!')


    # <matching_distance> method - Measuring the distance between the <Htb> and 
    # <Ctb>/<Ttb> address tokens.
    # ---------------------------------------------------------------------------------   
    def matching_distance(self,
                          tokens_a,
                          tokens_b,
                          string_type):

        """ <tokens_a>: List of Tokens A
            <tokens_b>: List of Tokens B
            <string_type>: Type of distance algorithm 
                           0 = Levenshtein edit-distance,
                           1 = FREE SLOT
                           2 = FREE SLOT
                           3 = FREE SLOT
                           4 = Similarity ratio
        """
        
        _distance_lst = []
        _distance_fin = 0.0

        # 0: Levenshtein edit-distance
        if string_type == 0:
            for _token_a in tokens_a:
                if tokens_b.count(_token_a) > 0:
                    _distance_lst.append(0.0)
                else:
                    if len(tokens_a)>0 and len(tokens_b)>0:
                        _scores = []
                        for _token_b in tokens_b:
                            _dist_score = distance (_token_a, 
                                                    _token_b)

                            _scores.append(float(_dist_score)/float(len(_token_a)))

                        # stores the smallest score in <_distance_lst>
                        # Note: smallest score = similar A and B tokens
                        _distance_lst.append(min(_scores))
                    else:
                        _distance_lst.append(1)

            for _score in _distance_lst:
                _distance_fin += _score
                
            _distance_fin = float(_distance_fin / float(len(_distance_lst)))

            if len(tokens_a) < len(tokens_b):
                _distance_fin = _distance_fin + (float(len(tokens_b) - len(tokens_a))/10.0)

            if len(tokens_a) > len(tokens_b):
                _distance_fin = _distance_fin + (float(len(tokens_a) - len(tokens_b))/10.0)
            
            if _distance_fin > 1:
                _distance_fin = 0
            else:
                _distance_fin = 1 - _distance_fin


        # 1: FREE SLOT
        if string_type == 1:
            #for _token_a in tokens_a:
            #    if tokens_b.count(_token_a) > 0:
            #        _distance_lst.append(0.0)
            #    else:
            #        if len(tokens_a)>0 and len(tokens_b)>0:
            #            _scores = []
            #            for _token_b in tokens_b:
            #                _dist_score = edit_distance(_token_a, 
            #                                            _token_b, 
            #                                            transpositions=True)

            #                _scores.append(float(_dist_score)/float(len(_token_a)))

            #            # stores the smallest score in <_distance_lst>
            #            # Note: smallest score = similar A and B tokens
            #            _distance_lst.append(min(_scores))
            #        else:
            #            _distance_lst.append(1)

            #for _score in _distance_lst:
            #    _distance_fin += _score
                
            #_distance_fin = float(_distance_fin / float(len(_distance_lst)))

            #if len(tokens_a) < len(tokens_b):
            #    _distance_fin = _distance_fin + (float(len(tokens_b) - len(tokens_a))/10.0)

            #if len(tokens_a) > len(tokens_b):
            #    _distance_fin = _distance_fin + (float(len(tokens_a) - len(tokens_b))/10.0)
            pass

        # 2: Jaccard distance
        if string_type == 2:
            _distance_fin = jaccard_distance (set(tokens_a), set(tokens_b))

        # 3: Measuring Agreement on Set-Valued Items (MASI)
        if string_type == 3:
            _distance_fin = masi_distance(set(tokens_a), set(tokens_b))

        # 4: Similarity ratio - Compute similarity ratio of two strings sets.
        #    The best match between any strings in the first set and the second set 
        #    (passed as sequences) is attempted. I.e., the order doesn't matter here.
        if string_type == 4:
            _distance_fin = setratio(tokens_a, tokens_b)

        return _distance_fin

    # <build_freq_tables> method - Creates frequency tables for Ctb and Htb address 
    #  tokens in the database, selects the top freq tokens based on <freq_ctb_limit>
    #  and <freq_htb_limit> limits and sets the selected tokens in the 
    #  <self.ctb_freq_tokens> and <self.htb_freq_tokens> lists. 
    #  If <freq_tables> is False, selects the top freq tokens based on <freq_ctb_limit>
    #  and <freq_htb_limit> limits and sets the selected tokens in the 
    #  <self.ctb_freq_tokens> and <self.htb_freq_tokens> lists. 
    # --------------------------------------------------------------------------------- 
    def build_freq_tables(self,
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

        if freq_tables == True:
            # Create freq Ctb table
            print('Creating the CtbFreq frequency table using the Ctb address tokens ...')
            _cur = sqlite_db.rCur()
            _ctb_ids = _cur.execute('SELECT Id FROM Ctb').fetchall()        

            tot_tokens = []
            _ctb_freq_tokenise = m_tokenise.Tokenise()
            _ctb_freq_tokenise.tokenise_all(sqlite_db,
                                            'Ctb',
                                            True,
                                            True,
                                            True,
                                            True,
                                            False,
                                            use_alias)
            for token in _ctb_freq_tokenise.tokens:
                tot_tokens.append(token)

            freq_info = collections.Counter(tot_tokens)

            _cur.execute("DROP TABLE if exists CtbFreq")
            _cur.execute("CREATE TABLE CtbFreq (Token text, Freq integer)")

            for key, val in freq_info.items():
                
                _str_fld = 'Token,Freq'
                _str_vals = '\'' + key + '\','
                _str_vals += str(val)
                
                _str_exec = 'INSERT INTO %s (%s) VALUES (%s)' % ('CtbFreq',
                                                                  _str_fld,
                                                                  _str_vals) 
                _cur.execute(_str_exec)
                
                # update Atb table with Ctb freq token value
                _con = sqlite_db.rCur()
                _str_exec = "SELECT Id FROM Atb WHERE Name = '%s'" % (key)
                _con_ids = _con.execute(_str_exec).fetchall()

                if _con_ids is not None:
                    for _ids in _con_ids:
                        _con.execute("UPDATE Atb SET Freq = %s WHERE Id = %i" % 
                                     (val,_ids[0]))
            sqlite_db.conn.commit()

            # Create freq Htb table
            print('Creating the HtbFreq frequency table using the Htb address tokens ...')
            _cur = sqlite_db.rCur()
            _htb_ids = _cur.execute('SELECT Id FROM Htb').fetchall()        

            tot_tokens = []
            _htb_freq_tokenise = m_tokenise.Tokenise()
            _htb_freq_tokenise.tokenise_all(sqlite_db,
                                            'Htb',
                                            True,
                                            True,
                                            True,
                                            True,
                                            False,
                                            use_alias)

            for token in _htb_freq_tokenise.tokens:
                tot_tokens.append(token)

            freq_info = collections.Counter(tot_tokens)

            _cur.execute("DROP TABLE if exists HtbFreq")
            _cur.execute("CREATE TABLE HtbFreq (Token text, Freq integer)")

            for key, val in freq_info.items():
                _str_fld = 'Token,Freq'
                _str_vals = '\'' + key + '\','
                _str_vals += str(val)

                _str_exec = 'INSERT INTO %s (%s) VALUES (%s)' % ('HtbFreq',
                                                                  _str_fld,
                                                                  _str_vals) 
                _cur.execute(_str_exec)

            sqlite_db.conn.commit()

            # Select freq Ctb tokens

            # Select freq Htb tokens 
         

        else:

            # Select freq Ctb tokens 

            # Select freq Htb tokens 

            pass


