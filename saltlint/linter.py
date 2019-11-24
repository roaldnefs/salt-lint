# -*- coding: utf-8 -*-
# Copyright (c) 2013-2014 Will Thames <will@thames.id.au>
# Modified work Copyright (c) 2019 Warpnet B.V.

from __future__ import print_function

from collections import defaultdict
import os
import re
import sys
import codecs

# import Salt libs
from salt.ext import six

import saltlint.utils
from saltlint.config import SaltLintConfig


class SaltLintRule(object):

    def __init__(self, config=None):
        self.config = config

    def __repr__(self):
        return self.id + ": " + self.shortdesc

    def verbose(self):
        return self.id + ": " + self.shortdesc + "\n " + self.description

    match = None
    matchtext = None

    @staticmethod
    def unjinja(text):
        return re.sub(r"{{[^}]*}}", "JINJA_VAR", text)

    def matchlines(self, file, text):
        matches = []
        if not self.match:
            return matches

        # arrays are 0-based, line numbers are 1-based
        # so use prev_line_no as the counter
        for (prev_line_no, line) in enumerate(text.split("\n")):
            if line.lstrip().startswith('#'):
                continue

            rule_id_list = saltlint.utils.get_rule_skips_from_line(line)
            if self.id in rule_id_list:
                continue

            result = self.match(file, line)
            if not result:
                continue
            message = None
            if isinstance(result, six.string_types):
                message = result
            matches.append(Match(prev_line_no+1, line,
                                 file['path'], self, message))

        return matches

    def matchfulltext(self, file, text):
        matches = []
        if not self.matchtext:
            return matches

        results = self.matchtext(file, text)

        for line, section, message in results:
            matches.append(Match(line, section, file['path'], self, message))

        return matches


class RulesCollection(object):

    def __init__(self, config=SaltLintConfig()):
        self.rules = []
        self.config = config

    def register(self, obj):
        self.rules.append(obj)

    def __iter__(self):
        return iter(self.rules)

    def __len__(self):
        return len(self.rules)

    def extend(self, more):
        self.rules.extend(more)

    # pylint: disable=dangerous-default-value
    def run(self, statefile, tags=[], skip_list=frozenset()):
        text = ""
        matches = []

        try:
            with codecs.open(statefile['path'], mode='rb', encoding='utf-8') as f:
                text = f.read()
        except IOError as e:
            print("WARNING: Couldn't open %s - %s" %
                  (statefile['path'], e.strerror),
                  file=sys.stderr)
            return matches

        for rule in self.rules:
            skip = False
            if not tags or not set(rule.tags).union([rule.id]).isdisjoint(tags):
                rule_definition = set(rule.tags)
                rule_definition.add(rule.id)

                # Check if the file is in the rule specific ignore list.
                for definition in rule_definition:
                    if self.config.is_file_ignored(statefile['path'], definition):
                        skip = True
                        break

                if not skip and set(rule_definition).isdisjoint(skip_list):
                    matches.extend(rule.matchlines(statefile, text))
                    matches.extend(rule.matchfulltext(statefile, text))

        return matches

    def __repr__(self):
        return "\n".join([rule.verbose()
                          for rule in sorted(self.rules, key=lambda x: x.id)])

    def listtags(self):
        tags = defaultdict(list)
        for rule in self.rules:
            for tag in rule.tags:
                tags[tag].append("[{0}]".format(rule.id))
        results = []
        for tag in sorted(tags):
            results.append("{0} {1}".format(tag, tags[tag]))
        return "\n".join(results)

    @classmethod
    def create_from_directory(cls, rulesdir, config):
        result = cls(config)
        result.rules = saltlint.utils.load_plugins(os.path.expanduser(rulesdir), config)
        return result


class Match(object):

    def __init__(self, linenumber, line, filename, rule, message=None):
        self.linenumber = linenumber
        self.line = line
        self.filename = filename
        self.rule = rule
        self.message = message or rule.shortdesc

    def __repr__(self):
        formatstr = u"[{0}] ({1}) matched {2}:{3} {4}"
        return formatstr.format(self.rule.id, self.message,
                                self.filename, self.linenumber, self.line)


class Runner(object):

    def __init__(self, rules, state, config, checked_files=None):
        self.rules = rules

        self.states = set()
        # Assume state is directory
        if os.path.isdir(state):
            self.states.add((os.path.join(state, 'init.sls'), 'state'))
        else:
            self.states.add((state, 'state'))

        # Get configuration options
        self.config = config
        self.tags = config.tags
        self.skip_list = config.skip_list
        self.verbosity = config.verbosity
        self.exclude_paths = config.exclude_paths

        # Set the checked files
        if checked_files is None:
            checked_files = set()
        self.checked_files = checked_files

    def is_excluded(self, file_path):
        # Check if the file path matches one of the exclude paths
        return self.exclude_paths.match_file(file_path)

    def run(self):
        files = []
        for state in self.states:
            if self.is_excluded(state[0]):
                continue
            files.append({'path': state[0], 'type': state[1]})

        matches = []

        # remove duplicates from files list
        files = [value for n, value in enumerate(files) if value not in files[:n]]

        # remove files that have already been checked
        files = [x for x in files if x['path'] not in self.checked_files]
        for file in files:
            if self.verbosity > 0:
                print("Examining %s of type %s" % (file['path'], file['type']))
            matches.extend(self.rules.run(file, tags=set(self.tags),
                                          skip_list=self.skip_list))
        # update list of checked files
        self.checked_files.update([x['path'] for x in files])

        return matches
