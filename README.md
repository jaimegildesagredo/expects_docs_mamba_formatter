# Expects docs Mamba formatter

[Mamba](https://github.com/nestorsalceda/mamba>) formatter to build the [Expects](https://github.com/jaimegildesagredo/expects>) docs.

## Installation

You can install it directly from github:

```bash
$ git clone git://github.com/jaimegildesagredo/expects_docs_mamba_formatter.git
$ cd expects_docs_mamba_formatter
$ python setup.py install
```

## Usage

Once installed you can run the [Expects specs](https://github.com/jaimegildesagredo/expects#specs>) with mamba and the installed formatter to generate the examples in [RST](http://sphinx-doc.org/rest.html>) format:

```bash
$ cd expects
$ mamba spec/expects --format=expects_docs > docs/expectations.rst
```
