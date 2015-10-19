Turtles
=======

Turtles is an Ansible Playbook Performance Profiler.  It will let you visualize
the performance of an ansible playbook run by parsing the ansible logfile into
a DSV file and then feeding it to an R script which will then generate a graph
depicting task run times.

Requirements
------------

 * python2.7 2.7.6-8ubuntu0.2
 * r-base 3.0.2-1ubuntu1
 * r-base-core 3.2.2-1trusty0

Example
-------

    # ./parse-ansible-log test.log > profile.csv
    # ./generate-profile profile.csv
    Wrote: profile.png
    # eog profile.png

Parsing Notes
-------------

The log file is parsed line by line.  If a Play is found, it updates the
"current" Play, and it is used in task labels until the next Play is found.
When a Task is found, it expects the very next line to be date and time info
related to that Task.  See below for an example of what the parser expects the
format to be.  If a Task is run multiple times in the same Play, a number is
incremented and included in the label to indicate which run of the Task it is.

### Plays ###

    PLAY [some text]

### Tasks ###

    TASK: [some text]
    Saturday 17 October 2015  03:43:31 +0000 (0:00:19.617)       2:49:02.025
