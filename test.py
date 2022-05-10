import unittest
import MySQLdb
from flask import request, url_for
from main import app

class FlaskTest(unittest.TestCase):

    connection = None


    def test_index(self):
        tester= app.test_client(self)
        response = tester.get("/")
        status_code=response.status_code
        self.assertEqual(status_code,200)
        
    def test_login(self):
        tester= app.test_client(self)
        response = tester.get("/login")
        status_code=response.status_code
        self.assertEqual(status_code,200)
          
    def test_logout(self):
        tester= app.test_client(self)
        response = tester.get("/logout",follow_redirects=True)
        status_code=response.status_code
        self.assertEqual(status_code,200)
        assert response.request.path=='/login'
    
    def test_dashboard(self):
        tester= app.test_client(self)
        response = tester.get("/dashboard")
        status_code=response.status_code
        self.assertEqual(status_code,200)
    
    
    def test_upload(self):
        tester= app.test_client(self)
        response = tester.get("/upload")
        status_code=response.status_code
        self.assertEqual(status_code,200)
    
"""  def test_connection(self):
        self.assertTrue(self.connection)  """  
"""  def setUp(self):        
        config= {
            'user' : 'root',
            'password':'root',
            'host' : 'mysqldb', 
            'database' : 'spe_proj',
            'auth_plugin' : 'mysql_native_password'
        }
        self.connection = MySQLdb.connect(**config)


def tearDown(self):
        if self.connection is not None and self.connection:
            self.connection.close()"""
    
if __name__=="__main__":
    unittest.main()
