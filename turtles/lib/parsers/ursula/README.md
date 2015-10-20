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
