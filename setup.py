#!/usr/bin/env python

###
# Copyright (c) 2002-2005, Jeremiah Fincher
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

plugins = [
    'Admin',
    'Alias',
    'Anonymous',
    'AutoMode',
    'Channel',
    'ChannelLogger',
    'ChannelStats',
    'Config',
    'Ctcp',
    'Dict',
    'Factoids',
    'Filter',
    'Format',
    'Games',
    'Google',
    'Herald',
    'Internet',
    'Karma',
    'Lart',
    'Later',
    'Limiter',
    'Math',
    'Misc',
    'MoobotFactoids',
    'Network',
    'NickCapture',
    'Nickometer',
    'Note',
    'Owner',
    'Plugin',
    'Praise',
    'Protector',
    'Quote',
    'QuoteGrabs',
    'Relay',
    'Reply',
    'RSS',
    'Scheduler',
    'Seen',
    'Services',
    'ShrinkUrl',
    'Status',
    'String',
    'Time',
    'Todo',
    'Topic',
    'URL',
    'User',
    'Utilities',
    'Web',
    ]

import sys

if sys.version_info < (2, 3, 0):
    sys.stderr.write("Supybot requires Python 2.3 or newer.\n")
    sys.exit(-1)

import textwrap

clean = False
while '--clean' in sys.argv:
    clean = True
    sys.argv.remove('--clean')

import glob
import shutil
import os.path

def normalizeWhitespace(s):
    return ' '.join(s.split())

try:
    from distutils.core import setup
    from distutils.sysconfig import get_python_lib
except ImportError, e:
    s = normalizeWhitespace("""Supybot requires the distutils package to
    install. This package is normally included with Python, but for some
    unfathomable reason, many distributions to take it out of standard Python
    and put it in another package, usually caled 'python-dev' or python-devel'
    or something similar. This is one of the dumbest things a distribution can
    do, because it means that developers cannot rely on *STANDARD* Python
    modules to be present on systems of that distribution. Complain to your
    distribution, and loudly. If you how much of our time we've wasted telling
    people to install what should be included by default with Python you'd
    understand why we're unhappy about this.  Anyway, to reiterate, install the
    development package for Python that your distribution supplies.""")
    sys.stderr.write(os.linesep*2)
    sys.stderr.write(textwrap.fill(s))
    sys.stderr.write(os.linesep*2)
    sys.exit(-1)

srcFiles = glob.glob(os.path.join('src', '*.py'))
pluginFiles = glob.glob(os.path.join('plugins', '*.py'))

if clean:
    previousInstall = os.path.join(get_python_lib(), 'supybot')
    if os.path.exists(previousInstall):
        try:
            print 'Removing current installation.'
            shutil.rmtree(previousInstall)
        except Exception, e:
            print 'Couldn\'t remove former installation: %s' % e
            sys.exit(-1)

packages = ['supybot',
            'supybot.utils',
            'supybot.drivers',
            'supybot.plugins',] + \
            ['supybot.plugins.'+s for s in plugins] + \
            ['supybot.plugins.Time.dateutil',]

package_dir = {'supybot': 'src',
               'supybot.utils': 'src/utils',
               'supybot.plugins': 'plugins',
               'supybot.drivers': 'src/drivers',
               'supybot.plugins.Time.dateutil': 'plugins/Time/dateutil',}

for plugin in plugins:
    package_dir['supybot.plugins.' + plugin] = 'plugins/' + plugin

version = '0.80.1+darcs'
setup(
    # Metadata
    name='supybot',
    version=version,
    author='Jeremy Fincher',
    url='http://supybot.com/',
    author_email='jemfinch@supybot.com',
    download_url='http://www.sf.net/project/showfiles.php?group_id=58965',
    description='A flexible and extensible Python IRC bot and framework.',
    long_description=normalizeWhitespace("""A robust, full-featured Python IRC
    bot with a clean and flexible plugin API.  Equipped with a complete ACL
    system for specifying user permissions with as much as per-command
    granularity.  Batteries are included in the form of numerous plugins
    already written."""),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        ],

    # Installation data
    packages=packages,

    package_dir=package_dir,

    scripts=['scripts/supybot',
             'scripts/supybot-test',
             'scripts/supybot-botchk',
             'scripts/supybot-wizard',
             'scripts/supybot-adduser',
             'scripts/supybot-plugin-doc',
             'scripts/supybot-plugin-create',
             'scripts/supybot-plugin-package',
             ]
    )


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
