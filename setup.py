#!/usr/bin/env python

from distutils.core import setup
from main import __version__

setup(name = 'CMarkEd',
      version = __version__,
      description = 'A multi platform CommonMark (Markdown) editor',
      author = 'Sergio de la Cruz, Armando Pereda',
      author_email = 'sergiodlc@gmail.com, armando.p.labrador@gmail.com',
      url = 'https://github.com/sergiodlc/cmarked',
      license = 'MIT',
      packages = ['ui'],
      package_data = {'ui':['*.qrc', '*.ui']},
      scripts=['main.py']
     )
