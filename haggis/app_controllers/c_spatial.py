# c_spatial.py - Python class (Controller) for controling the tasks of the 
# <m_spatial> and <v_spatial>.
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
from app_models import m_spatial


class CSpatial(object):
    """<CSpatial> class for spatial tools.
    """
    # Constructor: Initialises the properties of <CSpatial> instance.
    # ---------------------------------------------------------------------------------
    def __init__(self):
        self.model = m_spatial.SpatialTools()
    
    # <update_geometry_txt> method - Updates geometries using coordinates as text. 
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
        """ <sqlite_db>: sqlite database 
            <origin_table>: Origin table name 
            <origin_id_column>: Row identification number (in Origin table)
            <target_table>: Target table name
            <target_id_column>: Row identification number (in Target table)
            <coord_x_column>: X Coordinate column
            <coord_y_column>: Y Coordinate column
            <geom_column>: Geometry column
            <geom_type>: Type of Geometry ['POINT']
            <srid_code>: SRID code
        """
        
        self.model.update_geometry_txt(sqlite_db,
                                       origin_table,
                                       origin_id_column,
                                       target_table,
                                       target_id_column,
                                       coord_x_column,
                                       coord_y_column,
                                       geom_column,
                                       geom_type,
                                       srid_code)

    # <update_thiessen> method - Updates Thiessen table. 
    # ---------------------------------------------------------------------------------   
    def update_thiessen(self,
                        sqlite_db,
                        in_memory,
                        points_table,
                        p_geom_column,
                        thiess_table,
                        t_geom_column,
                        srid_code):
        """ sqlite_db: sqlite database
            in_memory: Is memory database [Boolean]
            points_table: Unique points table
            p_geom_column: Geometry column (in Unique points table)
            thiess_table: Thiessen table
            t_geom_column: Geometry column (in Thiessen table)
            srid_code: SRID code
        """
        
        self.model.update_thiessen(sqlite_db,
                                   in_memory,
                                   points_table,
                                   p_geom_column,
                                   thiess_table,
                                   t_geom_column,
                                   srid_code)

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
        """ sqlite_db: sqlite database
            in_memory: Is memory database [Boolean]
            point_table: Point table
            p_geom_column: Geometry column (in Point table)
            p_id_column: Point ID column
            p_poly_id_column: Polygon ID column(in Point table)
            polygon_table: Polygon table
            t_geom_column: Geometry column (in Polygon table)
            t_id_column: Polygon ID column
        """
        
        self.model.intersection_point_in_poly (sqlite_db,
                                               in_memory,
                                               point_table,
                                               p_geom_column,
                                               p_id_column,
                                               p_poly_id_column,
                                               polygon_table,
                                               t_geom_column,
                                               t_id_column)
    
    # <assign_density_region_codes> method - calculate Point Densities for each Region 
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
        """ sqlite_db: sqlite database
            point_table: Point table
            p_geom_column: Geometry column (in Point table)
            p_id_column: Point ID column
            p_region_column: RD code column 
            p_code_column: Assigned RD code column
            p_dens_column: Density column
            p_thies_column: Thiessen ID column (in Point table)
            thies_table: Thiessen table
            t_id_column: Thiessen ID column (in Thiessen table)
            t_region_column: Region column (in Thiessen table)
            radius: The radius of a circle used by the K-D Tree method (FLOAT)
            eval_limit: The matching threshold used by the system to compute the weights
            dens_limit: The point density threshold used by the system to compute the weights
        """

        self.model.assign_density_region_codes(sqlite_db,
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
                                               dens_limit)


