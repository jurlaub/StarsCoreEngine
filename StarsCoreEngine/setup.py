


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