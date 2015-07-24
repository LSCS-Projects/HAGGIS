# m_spatial.py - Python class (Model) for spatial properties and 
# methods.
#
# Copyright (C) 2014-5 Digitising Scotland Project
#
# Author: Konstantinos Daras <konstantinos.daras@gmail.com>
# Source code: https://github.com/LSCS-Projects/HAGGIS
# Web site: http://lscs-projects.github.io/HAGGIS/
# =============================================================================
#
#  This Source Code is subject to the terms of the BSD license. For license
#  information, see LICENSE.TXT 
#
# =============================================================================


# -------------------------------------------------------------------------------------
# Import necessary modules
import sys
import numpy as np
from scipy.spatial import Voronoi
from scipy.spatial import KDTree
from itertools import groupby
from operator import itemgetter
from decimal import *

class SpatialTools(object):
    """Collection of Spatial algorithms"""

    # Constructor: Initialises the properties of <Match> instance.
    # ---------------------------------------------------------------------------------
    def __init__(self):
        self.vor_list = []

    # <update_geometry_txt> method - Updates geometries using coordinates formatted 
    #                                as text. 
    # ---------------------------------------------------------------------------------   
    def update_geometry_txt(self,
                            sqlite_db,
                            origin_table,
                            origin_id_column,
                            target_table,
                            target_id_column,
                            coord_x_column,
                            coord_y_column,
                            geom_column,
                            geom_type,
                            srid_code):

        _cur = sqlite_db.rCur()
        # Select all RowID from table
        _all_ids = _cur.execute('SELECT * FROM %s' %
                                (origin_table,)).fetchall()

        for _row in _all_ids:
            _xy_values = _cur.execute('SELECT %s,%s FROM %s \
                                        WHERE %s=%s' % (coord_x_column,
                                                        coord_y_column,
                                                        origin_table,
                                                        origin_id_column,
                                                        str(_row[0]))).fetchall()
            _sql_command = "UPDATE %s SET %s = ST_GeomFromText('%s(%s %s)', %s) WHERE %s=%s" \
                            % (target_table,
                            geom_column,
                            geom_type,
                            str(_xy_values[0][0]),
                            str(_xy_values[0][1]),
                            srid_code,
                            target_id_column,
                            str(_row[0]))

            _cur.execute(_sql_command)
        sqlite_db.conn.commit()
        _distinct_ids = _cur.execute('SELECT X(Geometry), Y(Geometry) FROM %s \
                                      WHERE Geometry IS NOT NULL \
                                      GROUP BY X(Geometry), Y(Geometry)' 
                                      % (origin_table,)).fetchall()
        
        # Build unique point addresses table
        _cur.execute("SELECT DisableSpatialIndex('Unique_Points', 'Geometry')")
        _cur.execute("DROP TABLE if exists Unique_Points")
        _cur.execute("VACUUM")

        _cur.execute("CREATE TABLE Unique_Points (Id INTEGER PRIMARY KEY AUTOINCREMENT)")
        _cur.execute("SELECT AddGeometryColumn('Unique_Points', 'Geometry', %s, 'POINT', 'XY')" 
                     % (srid_code,)) 

        for _row in _distinct_ids:
            _sql_command = "INSERT INTO Unique_Points (Id, Geometry) VALUES \
                            (NULL, ST_GeomFromText('%s(%s %s)', %s))" \
                            % ('POINT',
                               str(_row[0]),
                               str(_row[1]),
                               srid_code)
            _cur.execute(_sql_command)
        sqlite_db.conn.commit()


    # <update_thiessen> method - Updates 'Thiessen' table using the geometries of 
    #                            'Unique_Points' table. 
    # ---------------------------------------------------------------------------------   
    def update_thiessen(self,
                        sqlite_db,
                        in_memory,
                        points_table,
                        p_geom_column,
                        thiess_table,
                        t_geom_column,
                        srid_code):

        if in_memory == True:    
            _cur = sqlite_db.cursor()
        else:
            _cur = sqlite_db.rCur()

        # Select all RowID from table
        _all_ids = _cur.execute('SELECT ST_X(%s), ST_Y(%s) FROM %s' 
                                % (p_geom_column,
                                   p_geom_column,
                                   points_table)).fetchall()
        
        # Compute Voronoi tesselation
        print ('Compute Voronoi tesselation...')
        _xy_list = []
        for x,y in _all_ids:
            _xy_list.append([x,y])
        points = np.array(_xy_list)
        self.vor_list = Voronoi(points)
        regions, vertices = self.assemble_voronoi_polygons()

        # Insert regions to Thiessen table
        print ('Save Thiessen polygons in the database...')
        for _reg in regions:
            _poly_txt = ''
            for _point in _reg:
                _poly_txt += str(vertices[_point][0]) + ' ' +  str(vertices[_point][1]) + ','
            _poly_txt += str(vertices[_reg[0]][0]) + ' ' +  str(vertices[_reg[0]][1])
            _sql_command = "INSERT INTO Thiessen (ThiesId, Geometry) \
                            VALUES (NULL, ST_GeomFromText('%s((%s))', %s))" \
                            % ('POLYGON',
                               _poly_txt,
                               srid_code)
            _cur.execute(_sql_command)

        if in_memory == True:
            sqlite_db.commit()
        else:
            sqlite_db.conn.commit()

    # <intersection_point_in_poly> method - links a polygon geometry to a point geometry  
    # ---------------------------------------------------------------------------------   
    def intersection_point_in_poly (self, 
                                    sqlite_db,
                                    in_memory,
                                    point_table,
                                    p_geom_column,
                                    p_id_column,
                                    p_poly_id_column,
                                    polygon_table,
                                    t_geom_column,
                                    t_id_column):
        
        if in_memory == True:    
            _cur = sqlite_db.cursor()
        else:
            _cur = sqlite_db.rCur()
        # Select all polyId from the polygon table
        _poly_ids = _cur.execute('SELECT %s FROM %s' % (t_id_column,
                                                         polygon_table)).fetchall()
        _poly_list = []
        print ('Intersect address points in Thiessen polygons ...') # TODO : MOVE MESSAGE TO VIEWER!!! 
        for _poly_id in _poly_ids:

            _sql_command = "SELECT %s FROM %s AS pt, %s AS pl \
                            WHERE ST_Within (pt.%s, pl.%s) \
                            AND pl.%s = %s \
                            AND pt.ROWID IN \
                            (SELECT ROWID FROM SpatialIndex  \
                            WHERE f_table_name='%s' AND search_frame=pl.%s)" \
                            % (p_id_column,
                               point_table,
                               polygon_table,
                               p_geom_column,
                               t_geom_column,
                               t_id_column,
                               str(_poly_id[0]),
                               point_table,
                               t_geom_column
                               )

            _point_ids = _cur.execute(_sql_command).fetchall()
            _poly_list.append([_poly_id,_point_ids])

        print ('Update Addresses table with Thiessen Id ...') # TODO : MOVE MESSAGE TO VIEWER!!! 
        
        for _poly_id, _point_ids in _poly_list:

            for _point_id in _point_ids:
                _cur.execute("UPDATE %s SET %s = %s WHERE %s=%s" \
                                % (point_table,
                                    p_poly_id_column,
                                    str(_poly_id[0]),
                                    p_id_column,
                                    str(_point_id[0])))
        if in_memory == True:
            sqlite_db.commit()
        else:
            sqlite_db.conn.commit()

        pass
    

    # <euclidean_distance> method - returns the Euclidean distance between P1 and P2
    #                      points  
    # ---------------------------------------------------------------------------------   
    def euclidean_distance (self, p1, p2):
        return sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 )

    # <assemble_voronoi_polygons> method - returns thiessen regions and vertices 
    #                                      as a list of tuples.  
    # ---------------------------------------------------------------------------------
    def assemble_voronoi_polygons(self, radius=None):
        """
        Reconstruct infinite voronoi regions in a 2D diagram to finite
        regions.

        Parameters
        ----------
        vor : Voronoi
            Input diagram
        radius : float, optional
            Distance to 'points at infinity'.

        Returns
        -------
        regions : list of tuples
            Indices of vertices in each revised Voronoi regions.
        vertices : list of tuples
            Coordinates for revised Voronoi vertices. Same as coordinates
            of input vertices, with 'points at infinity' appended to the
            end.

        """

        if self.vor_list.points.shape[1] != 2:
            raise ValueError("Requires 2D input")

        new_regions = []
        new_vertices = self.vor_list.vertices.tolist()

        center = self.vor_list.points.mean(axis=0)
        if radius is None:
            radius = self.vor_list.points.ptp().max()*2

        # Construct a map containing all ridges for a given point
        all_ridges = {}
        for (p1, p2), (v1, v2) in zip(self.vor_list.ridge_points, 
                                      self.vor_list.ridge_vertices):
            all_ridges.setdefault(p1, []).append((p2, v1, v2))
            all_ridges.setdefault(p2, []).append((p1, v1, v2))

        # Reconstruct infinite regions
        for p1, region in enumerate(self.vor_list.point_region):
            vertices = self.vor_list.regions[region]

            if all([v >= 0 for v in vertices]):
                # finite region
                new_regions.append(vertices)
                continue

            # reconstruct a non-finite region
            ridges = all_ridges[p1]
            new_region = [v for v in vertices if v >= 0]

            for p2, v1, v2 in ridges:
                if v2 < 0:
                    v1, v2 = v2, v1
                if v1 >= 0:
                    # finite ridge: already in the region
                    continue

                # Compute the missing endpoint of an infinite ridge

                t = self.vor_list.points[p2] - self.vor_list.points[p1] # tangent
                t /= np.linalg.norm(t)
                n = np.array([-t[1], t[0]])  # normal

                midpoint = self.vor_list.points[[p1, p2]].mean(axis=0)
                direction = np.sign(np.dot(midpoint - center, n)) * n
                far_point = self.vor_list.vertices[v2] + direction * radius

                new_region.append(len(new_vertices))
                new_vertices.append(far_point.tolist())

            # sort region counter-clockwise
            vs = np.asarray([new_vertices[v] for v in new_region])
            c = vs.mean(axis=0)
            angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
            new_region = np.array(new_region)[np.argsort(angles)]

            # finish
            new_regions.append(new_region.tolist())

        return new_regions, np.asarray(new_vertices)

    # <calculate_point_density> method - calculate Point Density using 
    #                                    KDTree (http://en.wikipedia.org/wiki/K-d_tree).  
    # 
    # Note: The maximum recursion limit can be exceeded for large data sets.  
    #       If this happens, increase the recursion limit by setrecursionlimit(10000)
    # ---------------------------------------------------------------------------------
    def calculate_point_density(self, 
                                list_points,
                                list_ids,
                                radius):

        sys.setrecursionlimit(10000) # TODO: Check alternatives

        # Set precision for decimal numbers
        getcontext().prec = 4

        tree = KDTree(np.array(list_points))
        neighbors = tree.query_ball_tree(tree, radius)
        frequency = np.array(map(len, neighbors))
        density_list = ((frequency/Decimal(len(list_ids)))*100).tolist()

        density = zip(list_ids, density_list)

        # Remove double id codes 
        res = set()
        res = [item for item in density if item[0] not in res and not res.add(item[0])]

        return res

    # <assign_density_region_codes> method - calculate Point Densities for each Thiessen 
    #                                        code and computes the assigned region
    #                                        codes (in column 'AssignedCode').  
    # ---------------------------------------------------------------------------------
    def assign_density_region_codes(self, 
                                    sqlite_db,
                                    point_table,
                                    p_geom_column,
                                    p_id_column,
                                    p_region_column,
                                    p_code_column,
                                    p_dens_column,
                                    p_thies_column,
                                    thies_table,
                                    t_id_column,
                                    t_region_column,
                                    radius,
                                    eval_limit,
                                    dens_limit):

        _cur = sqlite_db.rCur()

        # Select all RowID from table
        _region_ids = _cur.execute('SELECT DISTINCT %s FROM %s' 
                                % (p_region_column,
                                   point_table)).fetchall()
        
        _fin_regional_density = []

        for _region in _region_ids:
            _points = _cur.execute("SELECT %s, ST_X(%s), ST_Y(%s), HEvents FROM %s \
                                    WHERE %s = '%s' AND %s IS NOT NULL" 
                                    % (p_id_column,
                                       p_geom_column,
                                       p_geom_column,
                                       point_table,
                                       p_region_column,
                                       _region[0],
                                       p_geom_column)).fetchall()
            _list_points = []
            _list_ids = []
            for _point in _points:
                # Fill up the <_list_points> list with X,Y coordinates for each point
                # times the <HEvents> number.
                for x in range(0, _point[3]): 
                    _list_points.append((_point[1], _point[2]))

                    # Fill up the <_list_ids> list with unique Ids for each point
                    _list_ids.append(_point[0])

            if len(_list_points) > 1:
                # Calculate point density values
                _regional_density = self.calculate_point_density(_list_points, 
                                                                 _list_ids,
                                                                 radius)

                # Add Regional densities to a final list
                for _id, _density in _regional_density:
                    _fin_regional_density.append((_id,
                                                  _region[0],
                                                  _density))

        
        # Sort is needed for the groupby
        _fin_regional_density.sort()

        fin_list = [(max(g,key=itemgetter(2))) for i,g in groupby(_fin_regional_density, itemgetter(0))] 

        # update AssignedDens column
        print ('Update density values of the <%s> table...' % (point_table,))
        for _id, _region, _dens in fin_list:
            _cur.execute("UPDATE %s SET %s = %s WHERE %s=%s" \
                         % (point_table,
                            p_dens_column,
                            str(int(_dens)),
                            p_id_column,
                            str(_id)))

        sqlite_db.conn.commit()

        # update AssignedCode column
        print ('Update region codes of the <%s> table...' % (thies_table,))
        _thies_ids = _cur.execute('SELECT DISTINCT %s FROM %s' 
                                % (p_thies_column,
                                   point_table)).fetchall()
        for _thies in _thies_ids:
            _points = _cur.execute("SELECT %s, %s, %s, %s FROM %s \
                                    WHERE %s = '%s' AND %s IS NOT NULL" 
                                    % (p_id_column,
                                       'AutoEval', # TODO: Hardcode parameter
                                       p_dens_column,
                                       p_region_column,
                                       point_table,
                                       p_thies_column,
                                       _thies[0],
                                       p_geom_column)).fetchall()

            # Select all records with density value > 0
            _p_filter = [p for p in _points if p[2] >= dens_limit and p[1] >= eval_limit]

            if _p_filter:
                if len(_p_filter) == 1:
                    _cur.execute("UPDATE %s SET %s = '%s' WHERE %s=%s" \
                                % (thies_table,
                                   t_region_column,
                                   str(_p_filter[0][3]),
                                   t_id_column,
                                   str(_thies[0])))

                elif len(_p_filter) > 1:
                    # Select the record with maximum evaluation value
                    _pp_filter = [(i, e, d, r, (e+d)/2) for i, e, d, r in _p_filter]

                    _max_point = [(max(_pp_filter, key=itemgetter(2)))]  # itemgetter: 2 = density
                                                                         #             4 = (eval+dens)/2

                    _cur.execute("UPDATE %s SET %s = '%s' WHERE %s=%s" \
                                % (thies_table,
                                   t_region_column,
                                   str(_max_point[0][3]),
                                   t_id_column,
                                   str(_thies[0])))
        
        # Assign RD codes to unassigned Thiessen polygons using RD code of the nearest 
        # assigned Thiessen polygon 
        # 
        # TODO!!!
        

        # Update AssignedCode in the <Ttb> table 
        _thies_polys = _cur.execute('SELECT %s, %s FROM %s' \
                                     % (t_id_column,
                                        t_region_column,
                                        thies_table)).fetchall()

        for _thies in _thies_polys:
            _thies_points = _cur.execute("SELECT %s, %s, %s, %s, %s FROM %s \
                                        WHERE %s = %s" 
                                        % (p_id_column,
                                            'AutoEval', # TODO: Hardcode parameter
                                            p_dens_column,
                                            p_thies_column,
                                            p_code_column,
                                            point_table,
                                            p_thies_column,
                                            _thies[0])).fetchall()

            if len(_thies_points) >= 1:
                for _t_point in _thies_points:
                    if (_thies[1] <> '0') and (_thies[1] <> '') and (_thies[1] is not None):
                        _cur.execute("UPDATE %s SET %s = '%s' WHERE %s=%s" \
                                    % (point_table,
                                        p_code_column,
                                        _thies[1],
                                        p_thies_column,
                                        _thies[0]))
                 
                      
        sqlite_db.conn.commit()


           








