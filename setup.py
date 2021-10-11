# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Will Thames <will@thames.id.au>
# Copyright (c) 2018 Ansible by Red Hat
# Modified work Copyright (c) 2019-2021 Warpnet B.V.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from setuptools import setup, find_packages

from saltlint import (__author__, __license__,
                      NAME, VERSION, DESCRIPTION)


def long_description():
    """
    Returns the long description containing both the README.md and CHANGELOG.md
    files.
    """
    # Read content from the README.md file
    with open('README.md') as readme_file:
        readme = readme_file.read()

    # Read content from the CHANGELOG.md file
    with open('CHANGELOG.md') as changelog_file:
        changelog = changelog_file.read()

    return readme + changelog


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION.split('\n')[0],  # pylint: disable=C0207
    long_description=long_description(),
    long_description_content_type='text/markdown',
    author=__author__,
    author_email='info@warpnet.nl',
    url='https://github.com/warpnet/salt-lint',
    packages=find_packages(exclude=['tests', 'tests.*']),
    entry_points={
        'console_scripts': [
            'salt-lint = saltlint.cli:run',
        ]
    },
    include_package_data=True,
    python_requires='>=3.6.*',
    install_requires=['pyyaml', 'pathspec>=0.6.0'],
    license=__license__,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    keywords=['salt', 'saltstack', 'lint', 'linter', 'checker']
)
