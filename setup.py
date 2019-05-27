""" Wrapper script to ObsPy to search and pull station metadata
from IRIS FDSN server. Search is based on
center lat/lon and search radius. 

See:
https://github.com/flyrok/fdsn_station_info
"""

from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).resolve().parent

# Get the long description from the README file
readme=here / 'README.md'
with open(readme, encoding='utf-8') as f:
    long_description = f.read()

PROJECT_NAME="fdsn_station_info"
exec(open(here / "fdsn_station_info/version.py").read())

VERSION=__version__
DESCRIPTION="Search and pull station metadata from FDSN server"
URL="https://github.com/flyrok/fdsn_station_info"
AUTHOR="A Ferris"
EMAIL="aferris@flyrok.org"
CLASSIFIERS=['Development Status :: 3 - Alpha',
    'Intended Audience :: Seismic Researchers',
    'Topic :: Obspy/FDSN :: Helper Scripts',
    'License :: OSI Approved :: GPL-3 License',
     'Programming Language :: Python :: 3']
KEYWORDS="seismology obspy earthquakes fdsn"     

setup(
    name=PROJECT_NAME,  # Required
    version=VERSION,  # Required
    description=DESCRIPTION,  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url=URL,  # Optional
    author=AUTHOR,  # Optional
    author_email=EMAIL,  # Optional
    classifiers=CLASSIFIERS ,
    keywords=KEYWORDS,  # Optional
    python_requires='>=3.6',
    include_package_data=True,
    packages=['fdsn_station_info'],
    entry_points={  # Optional
        'console_scripts': [
            'fdsn_station_info=fdsn_station_info.fdsn_station_info:main',
        ],
    },
    extras_require={  # Optional
    },
    package_data={  
    },
    project_urls={  # Optional
        'Source': URL,
    },
)

