Expects docs Mamba formatter
============================

`Mamba <https://github.com/nestorsalceda/mamba>`_ formatter to build the `Expects <https://github.com/jaimegildesagredo/expects>`_ docs.

Installation
------------

You can install it directly from github::

    $ pip install -e git+git://github.com/jaimegildesagredo/expects_docs_mamba_formatter.git#egg=expects_docs_mamba_formatter

Usage
-----

Once installed you can run the `Expect specs <https://github.com/jaimegildesagredo/expects#specs>`_ with mamba and the installed formatter to generate the examples in `RST <http://sphinx-doc.org/rest.html>` format::

    $ cd expects
    $ mamba spec/expects --format=expects_docs > docs/expectations.rst
