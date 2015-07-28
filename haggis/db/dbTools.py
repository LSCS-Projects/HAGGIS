# dbTools.py - Python module to manage databases (only SQLite supported).
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

"""Module containing several classes to manage RDBMS databases.
"""

# -----------------------------------------------------------------------------
# Import necessary modules
import os
import sqlite3
import shutil 
import time

# =============================================================================
# Class for managing the SQLite database
# =============================================================================
class dbSQLiteManager(object):
    """Database Manager for SQLite database.
    """
        

    # Constructor: Creates the SQLite connection for a given <db> database
    # database path.
    # -------------------------------------------------------------------------
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.conn.execute('PRAGMA count_changes = OFF')
        self.conn.commit()
        self.cur = self.conn.cursor()
    # -------------------------------------------------------------------------

    # Applies the <sqlschema> schema to the <db> initialised SQLite database
    # -------------------------------------------------------------------------
    def apply_schema_db(self, db, sqlschema):
        if os.path.exists(db):
           print ('Creating schema "%s"' % sqlschema)
           with open(sqlschema, 'r') as f:
               schema = f.read()
           self.cur.executescript(schema)
        self.conn.commit()
    # -------------------------------------------------------------------------
    
    # Applies the <indexes> for indexing the fields of SQLite database
    # -------------------------------------------------------------------------
    def apply_indexes_db(self, db, sqlindexes):
        if os.path.exists(db):
           print ('Creating indexes"%s"' % sqlindexes)
           with open(sqlindexes, 'r') as f:
               index = f.read()
           self.cur.executescript(index)
        self.conn.commit()
    # -------------------------------------------------------------------------

    # Opens the SQLite connection for a given <db> database path.
    # -------------------------------------------------------------------------
    def open_db(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.enable_load_extension(True)
        self.cur = self.conn.cursor()
        self.cur.execute(r'SELECT load_extension("libspatialite-4.dll")')
        # self.cur.execute(r'SELECT InitSpatialMetaData();')
        self.conn.commit()
    # -------------------------------------------------------------------------

        # Returns cursor
    # -------------------------------------------------------------------------
    def rCur(self):       
        return self.conn.cursor()
    # -------------------------------------------------------------------------

    # Executes single arg
    # -------------------------------------------------------------------------
    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur
    # -------------------------------------------------------------------------

     # Executes many arg 
    # -------------------------------------------------------------------------
    def queryMany(self, arg):
        self.cur.executemany(arg)
        self.conn.commit()
        return self.cur
    # -------------------------------------------------------------------------

    # Close SQLite connection 
    # -------------------------------------------------------------------------
    def close_db(self):
        self.conn.commit()
        self.conn.close()
    # -------------------------------------------------------------------------

    # Clone SQLite database.
    # -------------------------------------------------------------------------
    def backup_db (self, db, prefix):
       backupfile = os.path.join ( os.path.dirname(db), os.path.basename(db) + 
                                   prefix + time.strftime(".%Y%m%d-%H%M") )
       shutil.copyfile ( db, backupfile )
    # -------------------------------------------------------------------------

    # Initialise Spatial-SQLite database (use of Spatialite).
    # -------------------------------------------------------------------------
    def init_spatial_db (self):

        self.cur.execute(r'SELECT InitSpatialMetaData()')

    # -------------------------------------------------------------------------

    # Update database with spatial tables/columns.
    # -------------------------------------------------------------------------
    def update_spatial_db (self,
                           srid_code):

        self.cur.execute("SELECT AddGeometryColumn('Ttb', 'Geometry', %s, \
                          'POINT', 'XY')" % (srid_code,))
        self.cur.execute("SELECT CreateSpatialIndex('Ttb', 'Geometry')")
        self.cur.execute("SELECT AddGeometryColumn('SSCtb', 'Geometry', %s, \
                          'POINT', 'XY')" % (srid_code,))
        self.cur.execute("SELECT CreateSpatialIndex('SSCtb', 'Geometry')")

    # -------------------------------------------------------------------------

    # Initialise Thiessen table.
    # -------------------------------------------------------------------------
    def init_thiessen_tbl (self,
                           srid_code):

        self.cur.execute("SELECT DisableSpatialIndex('Thiessen', 'Geometry')")
        self.cur.execute("DROP TABLE if exists idx_Thiessen_Geometry")
        self.cur.execute("DROP INDEX if exists Thiessen_idx_Id")
        self.cur.execute("DROP TABLE if exists Thiessen")
        self.cur.execute("VACUUM")

        self.cur.execute("CREATE TABLE Thiessen ( \
                          ThiesId integer NOT NULL PRIMARY KEY AUTOINCREMENT, \
                          RegionId text)")
        self.cur.execute("SELECT AddGeometryColumn('Thiessen', 'Geometry', %s, \
                          'POLYGON', 'XY')" % (srid_code,))
        self.cur.execute("SELECT CreateSpatialIndex('Thiessen', 'Geometry')")
        self.cur.execute("CREATE INDEX Thiessen_idx_Id ON Thiessen (ThiesId ASC)")

    # -------------------------------------------------------------------------

    # Initialise LUT_Regions table.
    # -------------------------------------------------------------------------
    def init_regions_tbl (self):

        self.cur.execute("DROP INDEX if exists LUT_Regions_idx_Id")
        self.cur.execute("DROP TABLE if exists LUT_Regions")
        self.cur.execute("VACUUM")
        
        self.cur.execute("CREATE TABLE LUT_Regions ( \
                          RegionId integer NOT NULL PRIMARY KEY AUTOINCREMENT, \
                          RegionCode text, \
                          EvalIndex real, \
                          Density real)")
        self.cur.execute("CREATE INDEX LUT_Regions_idx_Id ON LUT_Regions (RegionId ASC)")
    # -------------------------------------------------------------------------
