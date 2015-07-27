import unittest
import sys
import db.dbTools as DB

class Test_dbTools(unittest.TestCase):
    def test_dbTools(self):
        newdb = DB.dbSQLiteManager('test.db')
        newdb.open_db('test.db')

        self.fail("Not implemented")
        
if __name__ == '__main__':
    unittest.main()
