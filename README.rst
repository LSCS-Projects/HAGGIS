===========================================================
Historical Address Geocoder (HAG) 0.5.0 installation instructions
===========================================================

Konstantinos Daras, 04 June 2014


The basic HAG-0.5.0 installation requires Python  2.7, with
additional modules and libraries needed for the graphical user interface
(GUI) and the support vector machine (SVM) classification method.

Python:
  http://www.python.org

For the GUI, PyGTK and Matplotlib are required:
  http://www.pygtk.org
  http://matplotlib.sourceforge.net

The SVM classifier is based on libsvm:
  http://www.csie.ntu.edu.tw/~cjlin/libsvm/

  Follow the installation instruction within the python directory once
  you have downloaded and unpacked libsvm.


Test of installed modules:
--------------------------

To test if the required libraries are installed in your Python
distribution, start Python and try the following:

>>> import matplotlib
>>> matplotlib.use('GTK')

>>> import pygtk
>>> pygtk.require("2.0")

>>> import gtk
>>> import gtk.glade

>>> import svm

None of these import commands should give you an error.


HAG-0.5.0 installation:
-------------------------

Unpack the febrl-0.4.2.tar.gz or febrl-0.4.2.zip archive and a new
directory named 'febrl-0.4.2' will be created containing all the
necessary Febrl modules and additional files such as example data sets,
documentation, the Febrl data set generator and testing programs.

Go into the 'tests' sub-directory within 'febrl-0.4.2' and either run
all tests using the corresponding script provided:

>>> ./allTests.sh

or run the tests individually, for examples:

>>> python indexingTest.py
>>> python datasetTest.py

Note (by Van Ly, FSF): Due to differences in the end of line convention
for Mac (CR or \r), for Linux (LF or \n) and for Windows (CRLF or \r\n),
allTests.sh currently has the Windows end of line convention which
misbehaves on Linux Fedora 9 (in VirtualBox on Windows). Thus, the test
script does not execute properly, the work around I used was to apply

>>> cat allTests.sh |sed -e ',\r,,' > allTests_1.sh
>>> chmod u+x allTests_1.sh ; ./allTests_1.sh


Starting HAG-0.5.0
--------------------

The HAG GUI can be started using:

>>> ./guiFebrl.py

(you might have to set the execute permission for the file guiFebrl.py),
or using:

>>> python guiFebrl.py

Traditional HAG project modules (either implemented manually or
saved from within the GUI) can be run outside the GUI, for example:

>>> python my-linkage-project.py


Problems and errors:
--------------------

Please note that this is the initial 'alpha' distribution of HAG-0.5.0
which has only been tested to a limited extent on an Windows platform
(specifically Windows 7 & 8 with Python 2.7).

Please report any problems and bugs to: konstantinos.Daras@gmail.com


HAG-0.5.0 updates:
--------------------------

To receive updates and news on HAG please visit the following open source lists at:

.. image:: https://badge.fury.io/py/hag.png
    :target: http://badge.fury.io/py/hag
    
.. image:: https://badge.fury.io/gh/gisdarcon%2Fhag.png
        :target: https://github.com/gisdarcon/HAG

.. image:: https://pypip.in/d/hag/badge.png
        :target: https://pypi.python.org/pypi/hag


Historical Address Geocoder

* Free software: BSD license
* Documentation: http://hag.readthedocs.org.

Features
--------

* TODO