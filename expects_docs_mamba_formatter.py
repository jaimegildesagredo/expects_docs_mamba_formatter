# -*- coding: utf-8 -*-

import re
import inspect

from mamba.formatters import Formatter


class RSTFormatter(Formatter):
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

            expectation = self.expectations[name]

            for success in expectation['successes']:
                self.code(success)

            for failure in expectation['failures']:
                self.code(failure[0])
                self.failure(failure[1])

            self._in_code_block = False

    def code(self, value):
        if not self._in_code_block:
            self.write('.. code-block:: python\n')
            self._in_code_block = True

        self.write('\t{}\n'.format(value))

    def failure(self, value):
        self._in_code_block = False
        self.write('.. warning:: {}\n'.format(value))

    def write(self, content):
        print(content)
