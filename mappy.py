#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, url_for, redirect
app = Flask(__name__)

import yaml, markdown2
import copy

site = yaml.load(open('data/site.yaml').read())['site']

tmpl_vars = { 'site' : copy.deepcopy(site) }
for z in site['macros']:
  exec site['macros'][z] in tmpl_vars

tmpl_vars['site'] = False
tmpl_vars['content'] = False
tmpl_vars['title'] = False


@app.route("/admin/<path:admin_path>")
def admin(admin_path):
  """Only two routes are configured by default, admin and index.
  
  Admin takes care of any posting or viewing that should only be allowed
  for administrators of the site. Index is the public facing url resolver.
  """
  return "Index function"

@app.route("/<path:page_path>")
def index(page_path):
  """ All public pages are routed through this path
  
  First we convert slash paths to dot paths
  Then we resolve: page.title, page.content, template.content
  """
  
  page_name = ".".join(page_path.rstrip("/").lstrip("/").split("/"))
  
  if site['routes'].has_key(page_name):
    this_page_name = site['routes'][page_name]['page']
    this_template_name = site['routes'][page_name]['page']
  else:
    this_page_name = 'default'
    this_template_name = 'default'
  
  if site['pages'].has_key(this_page_name):
    tmpl_vars['title'] = site['pages'][this_page_name]['title']
    content = site['pages'][this_page_name]['content']
    
    """ The content field can be supplied from a file using a $stub redirect.
    Eventually I'd like to implement a generic handler so any field can be masked
    in this way """
    
    if content == "$stub":
      try:
        f_path = "data/site/pages/" + page_path.lstrip("/").rstrip("/") + ".mkd"
        content = open(f_path).read()
      except:
        content = "file not found..."
    tmpl_vars['content'] = markdown2.markdown(content)
  
  else:
    """ Page name not found 404. """
    tmpl_vars['content'] = "The page you were looking for doesn't seem to exist."
    tmpl_vars['title'] = "404 Page Not Found"
  
  if site['templates'].has_key(this_template_name):
    tmpl = site['templates'][this_template_name]['content'] % tmpl_vars
  else:
    tmpl = site['templates']['default']['content'] % tmpl_vars
  
  content = tmpl % tmpl_vars
  
  return content

@app.route("/")
def index_redirect():
  return redirect(url_for("index", page_path="index"))

if __name__ == "__main__":
    app.run(debug=True)

def test_run():
   app.run(debug=True)
