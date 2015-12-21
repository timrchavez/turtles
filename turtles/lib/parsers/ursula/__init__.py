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

import pytz
import re

from datetime import datetime, timedelta


TASK_RE = re.compile("TASK: \[(?P<task>[\w\W|\- ]+)\]")
PLAY_RE = re.compile("PLAY \[(?P<play>[\w ]+)\]")
DATE_RE = re.compile(
    "(?P<date>(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) "
    "\d+ (January|February|March|April|May|June|July|August|September"
    "|October|November|December) \d{4}\s+\d{2}:\d{2}:\d{2} (\+|\-)\d{4}) "
    "\((?P<duration>\d+:\d+:\d+\.\d+)\)\s+(?P<total_time>\d+:\d+:\d+\."
    "\d+)")
FACTS_RE = re.compile("GATHERING FACTS")


class UrsulaTestLogParser(object):
    name = "ursula-test-log-parser"
    help = "Parse log files generated by an ursula test run"

    @classmethod
    def parse(cls, logfile, min_duration):
        current_play = None
        current_color = 0
        colors = {}
        tasks = []
        times = []
        with open(logfile) as log:
            for line in log:
                match = PLAY_RE.search(line)
                if match:
                    current_play = match.group("play").lower()
                    current_color += 1
                    colors[current_play] = current_color
                    continue

                if current_play is None:
                    continue

                match_facts = FACTS_RE.search(line)
                if match_facts:
                    tasks.append(
                        "{0} | Gathering Facts".format(current_play))
                match_task = TASK_RE.search(line)
                if match_task:
                    tasks.append(
                        "{0} | {1}".format(
                            current_play, match_task.group("task")))
                if match_facts or match_task:
                    match = DATE_RE.search(next(log))
                    if match:
                        duration = datetime.strptime(
                            match.group("duration"), "%H:%M:%S.%f")
                        times.append(duration)

        task_counts = {}
        start_time = datetime(1901, 1, 1, 0, 0, 0, 0, pytz.UTC)
        min_duration = datetime.strptime(min_duration, "%H:%M:%S.%f")
        min_duration = timedelta(
            hours=min_duration.hour,
            minutes=min_duration.minute,
            seconds=min_duration.second,
            microseconds=min_duration.microsecond
        )
        print "event;start;end;label;color"
        for idx, full_task in enumerate(tasks):
            play = full_task.split("|")[0].strip()
            if idx+1 >= len(times):
                continue
            duration = times[idx+1]
            duration = timedelta(
                hours=duration.hour,
                minutes=duration.minute,
                seconds=duration.second,
                microseconds=duration.microsecond
            )
            if duration.total_seconds() < min_duration.total_seconds():
                continue

            if full_task in task_counts:
                task_counts[full_task] += 1
            else:
                task_counts[full_task] = 1
            full_task = "{0} #{1}".format(full_task, task_counts[full_task])

            color = colors[play]
            label = "{0}={1}".format(full_task, duration.total_seconds())

            relative_duration = start_time + duration

            print "{0};{1};{2};{3};{4}".format(
                full_task, start_time, relative_duration, label, color)
            start_time = relative_duration
