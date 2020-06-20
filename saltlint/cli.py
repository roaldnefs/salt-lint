# -*- coding: utf-8 -*-
# Copyright (c) 2013-2014 Will Thames <will@thames.id.au>
# Modified work Copyright (c) 2019 Warpnet B.V.

from __future__ import print_function

import argparse
import os
import sys
import tempfile
import codecs

from saltlint import formatters, NAME, VERSION
from saltlint.config import SaltLintConfig, SaltLintConfigError, default_rulesdir
from saltlint.linter import RulesCollection, Runner


def run(args=None):
    # Wrap `sys.stdout` in an object that automatically encodes an unicode
    # string into utf-8, in Python 2 only. The default encoding for Python 3
    # is already utf-8.
    if sys.version_info[0] < 3:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    parser = argparse.ArgumentParser(prog=NAME)
    parser.add_argument('--version', action='version',
                        version='{} {}'.format(NAME, VERSION))

    parser.add_argument('-L', dest='listrules', default=False,
                        action='store_true', help="list all the rules")
    parser.add_argument('-r', action='append', dest='rulesdir',
                        default=[], type=str,
                        help="specify one or more rules directories using "
                             "one or more -r arguments. Any -r flags override "
                             "the default rules in %s, unless -R is also used."
                        % default_rulesdir)
    parser.add_argument('-R', action='store_true', default=False,
                        dest='use_default_rules',
                        help="Use default rules in %s in addition to any extra "
                             "rules directories specified with -r. There is "
                             "no need to specify this if no -r flags are used."
                        % default_rulesdir)
    parser.add_argument('-t', dest='tags', action='append', default=[],
                        help="only check rules whose id/tags match these values")
    parser.add_argument('-T', dest='listtags', action='store_true',
                        help="list all the tags")
    parser.add_argument('-v', dest='verbosity', action='count',
                        help="Increase verbosity level",
                        default=0)
    parser.add_argument('-x', dest='skip_list', default=[], action='append',
                        help="only check rules whose id/tags do not " +
                        "match these values")
    parser.add_argument('--nocolor', '--nocolour', dest='colored',
                        default=hasattr(sys.stdout, 'isatty') and sys.stdout.isatty(),
                        action='store_false',
                        help="disable colored output")
    parser.add_argument('--force-color', '--force-colour', dest='colored',
                        action='store_true',
                        help="Try force colored output (relying on salt's code)")
    parser.add_argument('--exclude', dest='exclude_paths', action='append',
                        help='path to directories or files to skip. This option'
                             ' is repeatable.',
                        default=[])
    parser.add_argument('--json', dest='json', action='store_true', default=False,
                        help='parse the output as JSON')
    parser.add_argument('--severity', dest='severity', action='store_true', default=False,
                        help='add the severity to the standard output')
    parser.add_argument('-c', help='Specify configuration file to use.  Defaults to ".salt-lint"')

    # Parse the arguments
    (options, parsed_args) = parser.parse_known_args(args if args is not None else sys.argv[1:])

    stdin_state = None
    states = set(parsed_args)
    matches = []
    checked_files = set()

    # Read input from stdin
    if not sys.stdin.isatty():
        stdin_state = tempfile.NamedTemporaryFile('w', suffix='.sls', delete=False)
        stdin_state.write(sys.stdin.read())
        stdin_state.flush()
        states.add(stdin_state.name)

    # Read, parse and validate the configuration
    options_dict = vars(options)
    try:
        config = SaltLintConfig(options_dict)
    except SaltLintConfigError as exc:
        print(exc)
        return 2

    # Show a help message on the screen
    if not states and not (options.listrules or options.listtags):
        parser.print_help(file=sys.stderr)
        return 1

    # Collect the rules from the configution
    rules = RulesCollection(config)
    for rulesdir in config.rulesdirs:
        rules.extend(RulesCollection.create_from_directory(rulesdir, config))

    # Show the rules listing
    if options.listrules:
        print(rules)
        return 0

    # Show the tags listing
    if options.listtags:
        print(rules.listtags())
        return 0

    # Define the formatter
    if config.json:
        formatter = formatters.JsonFormatter()
    elif config.severity:
        formatter = formatters.SeverityFormatter(config.colored)
    else:
        formatter = formatters.Formatter(config.colored)

    for state in states:
        runner = Runner(rules, state, config, checked_files)
        matches.extend(runner.run())

    # Sort the matches
    matches.sort(key=lambda x: (x.filename, x.linenumber, x.rule.id))

    # Show the matches on the screen
    formatter.process(matches)

    # Delete stdin temporary file
    if stdin_state:
        os.unlink(stdin_state.name)

    # Return the exit code
    if matches:
        return 2

    return 0
