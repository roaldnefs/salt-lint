# -*- coding: utf-8 -*-
# Copyright (c) 2016 Will Thames and contributors
# Copyright (c) 2018 Ansible Project
# Modified work Copyright (c) 2020 Warpnet B.V.

from saltlint.linter.rule import Rule


class NoTabsRule(Rule):
    id = '203'
    shortdesc = 'Most files should not contain tabs'
    description = 'Tabs can cause unexpected display issues, use spaces'
    severity = 'LOW'
    tags = ['formatting']
    version_added = 'v0.0.1'

    def match(self, file, line):
        return '\t' in line
