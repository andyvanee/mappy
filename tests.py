import unittest, mappy, os


class ContentExists(unittest.TestCase):
   def setUp(self):
      self.app = mappy.app.test_client()
      f = open("static/tst_contentX8FF0S2442.js", "w")
      f.write("testing")
      f.close()
      
   def tearDown(self):
      os.remove("static/tst_contentX8FF0S2442.js")
      
   def test_content_exists(self):
      """ Content exists and doctype declared """
      content = self.app.get("/")
      assert content.data[0:9] == "<!DOCTYPE"
       
   def test_static_content_exists(self):
      """ Static content is being served """
      content = self.app.get("/static/tst_contentX8FF0S2442.js")
      assert content.data == "testing"

class AdminTests(unittest.TestCase):
   def setUp(self):
      self.app = mappy.app.test_client()
            
   def tearDown(self):
      pass

   def test_admin_page_content(self):
      """ Admin page has content """
      content = self.app.get("/admin/test")
      assert len(content.data) > 5


if __name__ == "__main__":
   unittest.main()