Turtles
=======

Turtles is a log-based performance profiler.  Parse a log with the appropriate
time information (see below) into a semicolon delimited DSV and then visualize
it.

Requirements
------------

 * python2.7 2.7.6-8ubuntu0.2
 * r-base 3.0.2-1ubuntu1
 * r-base-core 3.2.2-1trusty0

Example
-------

    # turtles parse --parser=ursula_log_parser test.log > graph.csv
    # turtles graph graph.csv
    Wrote: profile.png
    # eog profile.png

Parsers
-------

Parsing is left as an exercise to the user.  If there is a log you want to
parse time data from to visualize th progression of events, please create it
and then contribute it back to turtles.  Your parser should:

 1. Take a log as input
 2. Produce a semicolon-delimited DSV file as output

Data File Format
----------------

The graphing library expects as input a semicolon-delimited DSV file with the
following information:

    event;start;end;label;color

 * event - the thing being measured
 * start - the start time of the event (format: "%Y-%m-%d %H:%M:%OS3")
 * end - the end of the of the event (format: "%Y-%m-%d %H:%M:%OS3")
 * label - the label you want printed next to the line segment for the event
 * color - the color of the line segment for the event
