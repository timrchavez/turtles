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

import inspect
import os
import subprocess
import sys


class Graph(object):
    @classmethod
    def render(cls, dsvfile, imagefile, title, subtitle):
        # XXX: ugh :)
        r_script = os.path.join(
            os.path.dirname(
                os.path.abspath(inspect.getfile(inspect.currentframe()))),
            "profile.R"
        )
        proc = subprocess.Popen(
            [r_script,
             "datafile='%s'" % dsvfile,
             "imagefile='%s'" % imagefile,
             "title='%s'" % title,
             "subtitle='%s'" % subtitle],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            sys.exit("Profile generation failed!\nOUTPUT:\n%s" % stderr)

        return imagefile
