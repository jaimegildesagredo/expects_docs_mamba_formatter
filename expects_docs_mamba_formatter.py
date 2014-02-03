# -*- coding: utf-8 -*-

import re
import inspect

from mamba.formatters import Formatter

KEY = {
    'code': [
    ],
    'mappings': {
        'code': {
            '_.dct': "{'bar': 0, 'baz': 1}",
            '_.str': "'My foo string'"
        },
        'failures': {
            '_.dct': "{'bar': 0, 'baz': 1}",
            '_.str': "'My foo string'"
        }
    }
}

PROPERTY = {
    'code': [
        'class Foo(object):',
        '    bar = 0',
        '    baz = 1',
        '',
        'obj = Foo()',
        ''
    ],
    'mappings': {
        'code': {
            '_.obj': 'obj'
        },
        'failures': {
            '_.obj': '<Foo object at 0x7ff289cb4310>'
        }
    }
}


class RSTFormatter(Formatter):

    statics = {
        'a': PROPERTY,
        'an': PROPERTY,
        'be': {
            'code': [
                'value = 1',
                ''
            ],
            'mappings': {
                'code': {},
                'failures': {}
            }
        },
        'have': {
            'code': [
                "lst = ['bar', 'baz]",
                'itr = iter(lst)',
                ''
            ],
            'mappings': {
                'code': {
                    '_.lst': 'lst',
                    '_.itr': 'itr'
                },
                'failures': {
                    '_.lst': "['bar', 'baz']",
                    '_.itr': "<listiterator object at 0x7ff289cb4310>"
                }
            }
        },
        'key': KEY,
        'keys': KEY,
        'property': PROPERTY,
        'properties': PROPERTY
    }

    def __init__(self, settings):
        self.settings = settings
        self.expectations = {}
        self.current = None
        self._in_code_block = False

    def example_group_started(self, example_group):
        if example_group.parent is None:
            self.current = self.expectations[example_group.name] = {
                'successes': [],
                'failures': []
            }

    def example_passed(self, example):
        expectation, failure = None, None

        for line in inspect.getsourcelines(example.test)[0]:
            if 'expect(' in line:
                expectation = line.strip()

            if 'failure(' in line:
                failure = self.__failure(line)

        if failure is not None:
            self.current['failures'].append((expectation, failure))
        else:
            self.current['successes'].append(expectation)

    def __failure(self, raw):
        match = re.search(r"""failure\((?P<actual>[\w\.]+),\s+('|")(?P<message>.*)('|").*\)""", raw)
        actual, message = match.group('actual'), match.group('message')
        return 'Expected {} {}'.format(actual, message)

    def summary(self, *args, **kwargs):
        for name in sorted(self.expectations.keys()):
            self.write('{}\n{}\n'.format(name, '-'*len(name)))

            static = self.statics.get(name)

            if static is not None:
                for static_code in static['code']:
                    self.code(static_code)

            expectation = self.expectations[name]

            for success in expectation['successes']:
                if static is not None:
                    for mapping_src, mapping_dst in static['mappings']['code'].items():
                        success = success.replace(mapping_src, mapping_dst)

                self.code(success)

            for failure in expectation['failures']:
                failure_code, failure_message = failure

                if static is not None:
                    for mapping_src, mapping_dst in static['mappings']['code'].items():
                        failure_code = failure_code.replace(mapping_src, mapping_dst)

                    for mapping_src, mapping_dst in static['mappings']['failures'].items():
                        failure_message = failure_message.replace(mapping_src, mapping_dst)

                self.code(failure_code)
                self.failure(failure_message)

            self._in_code_block = False

    def code(self, value):
        if not self._in_code_block:
            self.write('.. code-block:: python\n')
            self._in_code_block = True

        self.write('    {}'.format(value))

    def failure(self, value):
        self._in_code_block = False
        self.write('.. admonition:: Failure\n\n    {}\n'.format(value))

    def write(self, content):
        print(content)
