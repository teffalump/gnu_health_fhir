from distutils.core import setup

setup(name = 'health_fhir',
        version = '0.0.1',
        description = 'Provides FHIR interface to GNU Health.',
        url = 'https://github.com/teffalump/health_fhir',
        author = 'teffalump',
        packages = ['health_fhir'],
        install_requires = ['fhirclient'],
        zip_safe = False,
        classifiers = ['Development Status :: 2 - Pre-Alpha',
                       'Programming Language :: Python',
                       'Programming Language :: Python :: 3',
                       'Intended Audience :: Developers',
                       'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                       'Operating System :: OS Independent'])
