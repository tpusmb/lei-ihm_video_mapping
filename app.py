#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main script to run the degree management web-app.
Usage:
   app.py <port> [--mode=<mode>]

Options:
    -h --help                   Show this screen.
    <port>                      Port to run the server example 8080, [default 8080]
    --mode=<mode>               Debug or prod, else prod, [default: debug]
"""

from docopt import docopt

from web import app, py_video_mapping

if __name__ == '__main__':
    args = docopt(__doc__)

    try:
        port = int(args["<port>"])
    except ValueError:
        port = 8080
    try:
        debug_mode = args["--mode"] == 'debug'
    except ValueError:
        debug_mode = False

    app.run(debug=debug_mode, port=port)
    py_video_mapping.stop()
