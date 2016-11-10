from setuptools import setup

setup(
        name='health_fhir',
        version='0.1',
        description='FHIR interface for GNU Health data models',
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Environment :: Plugins',
            'Intended Audience :: Healthcare Industry',
            'Intended Audience :: Developers',
            'Topic :: Scientific/Engineering :: Medical Science Apps.',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            ],
        url='https://github.com/teffalump/health_fhir',
        author='teffalump',
        author_email='chris@teffalump.com',
        keywords='hl7 fhir gnuhealth',
        license='GPL-3',
        install_requires=[
            'fhirclient',
            'trytond'
            ],
        packages=['health_fhir'],
        zip_safe=False
)
