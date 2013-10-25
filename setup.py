from setuptools import setup, find_packages

version = '0.1'
shortdesc = "g24 content importer"
longdesc = """"""

setup(name='g24.importer',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Environment :: Web Environment',
            'Framework :: Zope2',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
      keywords='',
      author='Johannes Raggam',
      author_email='johannes@raggam.co.at',
      url='http://github.com/g24at/g24.importer',
      license='General Public Licence',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['g24',],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.setuphandlertools',
          'postmarkup',
          'requests',
      ],
      extras_require={
          'sqlimport': [
              'MySQL-python',
            ]
      },
  )
