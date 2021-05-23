EQVersion [DEPRECATED, NOT USE]
=========

.. image:: https://github.com/snakypy/eqversion/workflows/Python%20package/badge.svg
    :target: https://github.com/snakypy/dotctrl


The purpose of **EQVersion** is to remove the change redundancy in the project version in two places, in the **pyproject.toml** and in the **__init__.py** of the main package. **EQVersion** is especially for those who work with `Poetry`_.


Using:
------

In a project using `Poetry`_ and an active virtual environment, add **EQVersion** as a development dependency:

.. code-block:: shell

    $ poetry add eqversion --dev


Now simply run the command below for the versions to be matched:

.. code-block:: shell

    $ eqversion

**Specifying a package:**

By default, **EQVersion** takes the name of the main package via **pyproject.toml**, in the key **name**, but it may happen that the name of the main package is not the same as in **pyproject.toml**. If this happens, the **--package** option should be used to specify the main package:

.. code-block:: shell

    $ eqversion --package=<PACKAGE MAIN NAME>

Using with tests:

You must call **EQVersion** before performing your tests.

Example of `tox.ini` file:

.. code-block:: ini

    [tox]
    isolated_build = True
    
    [testenv]
    setenv =
        PYTHONPATH = {toxinidir}
    deps =
        poetry
    commands =
        pip install --upgrade pip
        poetry install
        poetry run eqversion
    ;   Or use the named option:
    ;   poetry run eqversion --package=<PACKAGE MAIN NAME>
        poetry run pytest --basetemp={envtmpdir}

Links
-----

* Authors: https://github.com/snakypy/eqversion/blob/master/AUTHORS.rst
* Code: https://github.com/snakypy/eqversion
* Documentation: https://github.com/snakypy/eqversion/blob/master/README.rst
* Releases: https://pypi.org/project/eqversion/#history
* Issue tracker: https://github.com/snakypy/eqversion/issues

Donation
--------

If you liked my work, buy me a coffee <3

.. image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif
    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YBK2HEEYG8V5W&source

License
-------

The gem is available as open source under the terms of the `MIT License`_ ©


.. _MIT License: https://github.com/snakypy/zshpower/blob/master/LICENSE
.. _Poetry: https://python-poetry.org/
