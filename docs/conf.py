import sys

from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from django.conf import settings

settings.configure()

project = 'django-slack'
version = ''
release = ''
copyright = '2014, 2015 Chris Lamb'
author = 'lamby'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']
html_title = "%s documentation" % project
html_theme = "sphinx_rtd_theme"
master_doc = 'index'
exclude_trees = ['_build']
templates_path = ['_templates']
latex_documents = [
    ('index', '%s.tex' % project, html_title, author, 'manual', True),
]
intersphinx_mapping = {'http://docs.python.org/': None}
