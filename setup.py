from setuptools import setup
import os

try:
    from pypandoc import convert
    read_md = lambda f: convert_file(f, 'rst')
except ImportError:
    print('warning: pypandoc module not found, cannot covert Markdown to RST')
    read_md = open(f, 'r').read()

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'health_fhir', '__version__.py')) as v:
    exec(v.read(), about)


setup(name = 'health_fhir',
        version = about['__version__'],
        description = 'Provides FHIR interface to GNU Health.',
        long_description = read_md(os.path.join(here, 'README.md')),
        url = 'https://github.com/teffalump/health_fhir',
        author = 'teffalump',
        author_email = 'chris@teffalump.com',
        packages = ['health_fhir'],
        install_requires = ['fhirclient'],
        include_package_data = True,
        zip_safe = False,
        classifiers = ['Development Status :: 2 - Pre-Alpha',
                       'Programming Language :: Python',
                       'Programming Language :: Python :: 3',
                       'Intended Audience :: Developers',
                       'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                       'Operating System :: OS Independent'])
