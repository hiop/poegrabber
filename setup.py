from distutils.core import setup
import py2exe

setup(
	console=['poescrpt.py'],
    options={
        'py2exe': 
        {
            'includes': ['lxml.etree', 'lxml._elementpath', 'gzip'],
			'compressed': True,
			'bundle_files': 1
        }
    }
)