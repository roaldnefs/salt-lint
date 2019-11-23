# -*- coding: utf-8 -*-
# Copyright (c) 2016 Will Thames and contributors
# Copyright (c) 2018 Ansible Project
# Modified work Copyright (c) 2019 Warpnet B.V.

from saltlint.linter import SaltLintRule


class LineTooLongRule(SaltLintRule):
    id = '204'
    shortdesc = 'Lines should be no longer that 160 chars'
    description = (
        'Long lines make code harder to read and '
        'code review more difficult'
    )
    severity = 'VERY_LOW'
    tags = ['formatting']
    version_added = 'v0.0.1'

    def match(self, _, line):
        return len(line) > 160
