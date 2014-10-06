"""
    This file is part of Stars Core Engine, which provides an interface and processing of Stars data.
    Copyright (C) 2014  <Joshua Urlaub + Contributors>

    Stars Core Engine is free software: you can redistribute it and/or modify
    it under the terms of the Lesser GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Stars Core Engine is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Lesser GNU General Public License for more details.

    You should have received a copy of the Lesser GNU General Public License
    along with Stars Core Engine.  If not, see <http://www.gnu.org/licenses/>.


"""


try: 
	from setuptools import setup
except ImportError:
	from distutils.core import setup


config = {
	'description' : 'stars core engine',
	'author' : 'sw',
	'url' : 'URL to get at it',
	'download_url' : 'where to download',
	'author_email' : 'My email',
	'version' : '0.1',
	'install_requires' : ['nose'],
	'packages' : ['starscoreengine'],
	'scripts' : [],
	'name' : 'starscoreengine'
}

setup(**config)