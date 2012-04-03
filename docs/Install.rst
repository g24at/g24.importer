g24.importer Installation
-------------------------

Use zc.buildout to install the package or depend in your integration product's
setup.py on it.

* Add the package to the list of eggs to install, e.g.:

    [buildout]
    ...

    [instance]
    eggs =
        ...
        g24.importer
    zcml =
        ...
      

* Re-run buildout, e.g. with:

    $ ./bin/buildout
        
You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.
