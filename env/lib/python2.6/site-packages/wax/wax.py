""" A standalone Python CGI Document generator library.

The idea of wax is to provide a thin layer of abstraction
over the basic CGI features of Python. It's not a server or
framework, just some tools to make utility scripts with.

Wherever possible, I'm just wrapping the default Python
functionality. No external libraries should be necessary.
"""

import cgi, cgitb
cgitb.enable()

import urllib, sqlite3, re, os
import httplib
import lib.yaml
import lib.markdown2

class Page:
   def __init__(self, headers):
      """Page is a web document. It is initalized with the Content-type header."""
      print headers
      print
   
   def send(self, x):
      """Wrapper over print to ensure that headers get sent properly."""
      print x
   
   def render(self, x):
      """
      Just a simple wrapper over reading a file into a string. Example:
      x = page.read('templates/index.html') % (title, content, welcome)
      """
      return open(x).read()
      
   def yaml(self, x):
      template = '  '.join(open(x, 'rb').read().split('\t'))
      t = lib.yaml.load(template)
      return t
      
   def markdown(self, x):
      return lib.markdown2.markdown(x)
      
class Site:
   def __init__(self, doc_root):
      """Defines the primary interface for dealing with content on the site."""
      self.doc_root = doc_root
      site = yaml_load('data/site.yaml')['site']
      self.site = site

   def request(self):
      page_name = 'index'
      template = 'default'
      page = {'page': page_name, 'template': template}

      query_string = os.environ['QUERY_STRING']
      request_uri = os.environ['REQUEST_URI']
      
      """
      # Parse Request URI
      
      Now we map request_uri to site.routes to resolve the pathname.
      """
      
      for key in self.site['routes']:
         if self.doc_root % self.site['routes'][key][0] == request_uri:
            page_name = key
            template = self.site['routes'][key][2]
      
      """Try to resolve stub content"""
      page['page'] = self.site['pages'][page_name]
      if page['page']['content'] == "$stub":
            path = "data/pages/%s.mkd" % page_name
            if os.path.exists(path):
               page['page']['content'] = open(path).read()
      page['template'] = self.site['templates'][template]

      self.page = page
      return page
      
class Form:
   def __init__(self):
      self.form = cgi.FieldStorage()
   def value(self, x):
      if self.form.has_key(x):
         return self.form[x].value
      else:
         return False
      
class Db:
   def __init__(self, db_file):
      """c.execute('create table pages (title text, parent int, content text)') """
      pass

def markdown(text):
   return lib.markdown2.markdown(text)
def yaml_load(f):
   template = '  '.join(open(f, 'rb').read().split('\t'))
   t = lib.yaml.load(template)
   return t

def http_get(host, path):
   connection = httplib.HTTPConnection(host, 80)
   connection.request("GET", path)
   response = connection.getresponse()
   # print r1.status, r1.reason
   return response.read()

# def table(xy):
#    tbl = "<table>"
#    for x in xy:
#       tbl += "<tr>"
#       for y in x:
#          tbl += "<td>"+y+"</td>"
#       tbl += "</tr>"
#    tbl += "</table>"
#    return tbl