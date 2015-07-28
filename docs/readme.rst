=====================================================================
HAGGIS 1.0.0 - Installation instructions
=====================================================================

**Konstantinos Daras, July 2015**


The basic HAGGIS-1.0.0 installation requires Python  2.7, with
additional packages and libraries needed for the spatial analysis and database
managment of data.

Python 2.7:

http://www.python.org

To install pip, securely download get-pip.py (https://bootstrap.pypa.io/get-pip.py). Then run the following (which may require administrator access)::

> python get-pip.py

If setuptools is not already installed, get-pip.py will install setuptools for you. To upgrade an existing setuptools::

> pip install -U setuptools.

Additional Python packages (**pip package is required**)

wheel package::

> pip install wheel==0.24.0

PyYAML package::

> pip install PyYAML==3.11

python-Levenshtein package::

> pip install python-Levenshtein==0.11.2

scipy package::

> pip install scipy==0.15.1

numpy package::

> pip install numpy==1.9.2

nose package::

> pip install nose==1.3.7

tqdm package::

> pip install tqdm==1.0


External Libraries:
  
Follow the installation instructions as suggested at the official sites of the following libraries.

Qhull library (scipy depedency) at http://www.qhull.org/

SpatiaLite v4.0 library (sqlite depedency) at http://www.gaia-gis.it/gaia-sins/


Test of installed modules:
--------------------------

To test if the required libraries are installed in your Python
distribution, start Python and try the following:

>>> from scipy.spatial import Voronoi
>>> from scipy.spatial import KDTree

>>> import Levenshtein
>>> import tqdm

>>> import PyYAML
>>> import numpy

None of these import commands should give you an error.


HAGGIS-1.0.0 installation:
-------------------------

Unpack the archive and a new directory named 'HAGGIS' will be created containing all the necessary HAGGIS modules and additional files such as example data sets, documentation and testing programs.

Go into the 'haggis' sub-directory within 'HAGGIS' and run all tests using the corresponding command provided::

> nosetests

or run the tests individually (within 'HAGGIS/haggis/tests' folder), for example::

> python test_spatial.py



Starting HAGGIS-1.0.0
--------------------

The HAGGIS can be started using::

> python haggis.py

or

> python haggis.py <config file>

where <config file> is a given configuration file.


Problems and errors:
--------------------

Please note that this is the initial distribution of HAGGIS-1.0.0
which has only been tested to a limited extent on an Windows platform
(specifically Windows 7 & 8 with Python 2.7).

Please report any problems and bugs to: konstantinos.Daras@gmail.com


HAGGIS-1.0.0 updates:
--------------------------

To receive updates and news on HAG please visit the following open source lists at:
    
.. image:: https://badge.fury.io/gh/LSCS-Projects%2FHAGGIS.png
        :target: https://github.com/LSCS-Projects/HAGGIS


Historical Address Geocoder

* Free software: GPL 3.0 license
* Documentation: http://www.gnu.org/licenses/gpl.html.

Future features
--------

ToDo list

*	Documentation
*   Export Geocoded Historical addresses and RD polygon cendroids [Priority]
*	Use Q-Gram algorithm
*	Use Jaro-Winkler algorithm
*	Introduce weights in each token [Priority]
*	Use Classification after address comparison [Priority]