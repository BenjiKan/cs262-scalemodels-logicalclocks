# cs262-scalemodels-logicalclocks
CS 262 Design Exercise 2: Scale Models and Logical Clocks

Following the example given in section, we initialize three separate processes, each with two threads: a listening consumer and a sending producer. Since connections are bidirectional, we only need to initialize three connections between our three processes, although this can be relatively easily scaled for a larger number of processes.
