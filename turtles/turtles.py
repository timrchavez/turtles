#!/usr/bin/env python
# Copyright 2015 Blue Box Cloud, an IBM Company
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import inspect
import sys


from lib import parsers
from lib.graph import Graph


def get_log_parsers():
    log_parsers = {}
    for name, obj in inspect.getmembers(parsers):
        if inspect.isclass(obj):
            log_parsers[obj.name] = obj
    return log_parsers


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    log_parsers = get_log_parsers()
    parse_cmd_parser = subparsers.add_parser("parse")
    parse_cmd_parser.add_argument(
        "--parser",
        help=(
            "The parser used to extract time information from a log. Valid "
            "options: {0}".format(", ".join(log_parsers.keys()))
        )
    )
    parse_cmd_parser.add_argument(
        "--min-duration",
        default="00:00:10.000",
        help="The minimum duration of a valid task"
    )
    parse_cmd_parser.add_argument(
        "logfile",
        help=(
            "Log file containing necessary timing information.  See README.md "
            "for more information"
        )

    )
    parse_cmd_parser.set_defaults(which="parse")

    graph_cmd_parser = subparsers.add_parser("graph")
    graph_cmd_parser.add_argument(
        "--imagefile",
        default="graph.png",
        help="File location to write image to"
    )
    graph_cmd_parser.add_argument(
        "--title",
        default="Performance Profile",
        help="Title to appear on graph"
    )
    graph_cmd_parser.add_argument(
        "--subtitle",
        default="",
        help="Subtitle to appear on graph"
    )
    graph_cmd_parser.add_argument(
        "dsvfile",
        help=(
            "File containing semicolon-delimited values.  See README.md "
            "for more information"
        )
    )
    graph_cmd_parser.set_defaults(which="graph")

    args = parser.parse_args()

    if args.which == "parse":
        if args.parser in log_parsers:
            log_parsers[args.parser].parse(args.logfile, args.min_duration)
        else:
            sys.exit("Please specify a valid parser")
    elif args.which == "graph":
        print "Wrote: " + Graph.render(
            args.dsvfile, args.imagefile, args.title, args.subtitle),
        print


if __name__ == "__main__":
    main()
