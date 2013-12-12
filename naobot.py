#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from core.naobot import Nicebot
import ConfigParser

if __name__ == '__main__':

    config = ConfigParser.RawConfigParser()
    config.read('settings/settings.conf')

    print config.get('core', 'server')
    print config.get('core', 'plugins').split(",");

    parser = argparse.ArgumentParser(description='Nicelab IRC bot', version='%(prog)s 0.5')
    parser.add_argument('-d', '--daemon', action='store_true', default=False, dest='daemon', help='start bot as a daemon')
    parser.add_argument('-c', '--config-file', action='store', dest='config_file', default='settings', help='use given file in ./settings/ dir for bot configuration')

    results = parser.parse_args()

    if results.daemon:
        try:
            pid = os.fork()
        except OSError, e:
            raise Exception, '%s [%d]' % (e.strerror, e.errno)

        if pid == 0:
            os.setsid()
            try:
                pid = os.fork()
            except OSError, e:
                raise Exception, '%s [%d]' % (e.strerror, e.errno)

            if pid == 0:
                pass
            else:
                os._exit(0)
        else:
            os._exit(0)

    exec('from settings.%s import conf, plugins_conf' % results.config_file)

    Nicebot(conf, plugins_conf, results.config_file).start()
