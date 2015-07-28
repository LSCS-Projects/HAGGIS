# v_clean.py - Python class (View) for presenting cleaning results.
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

class VClean(object):
    """<VClean> class for presenting messages and information of the cleaning
       process.
    """

    # <load_yaml_file> method - presents a load message.
    # --------------------------------------------------------------------------------
    def cmd_clean(self, table_name, field_name):
        print ('Cleaning <' + field_name + '> field in <' + table_name + '> table...')


