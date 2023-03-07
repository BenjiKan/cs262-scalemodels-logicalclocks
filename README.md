# cs262-scalemodels-logicalclocks
CS 262 Design Exercise 2: Scale Models and Logical Clocks

## Data Logs
Each experiment is saved in a separate folder containing a log for each process under the experiments directory, named as follows:
```d[event prob]-[clock rate 1]-[clock rate 2]-[clock rate 3]```

The event probability is determined by a n-sided die (d10 for the original specs), with a 2/n probability of sending to only one of the machines (1/n each), and also a 1/n probability of sending to both. The clock rates are the number of logical clock ticks per real second. Note that these rates are not necessarily corresponding to the ordered processes; rather, they are ordered in ascending order for ease of comparison. 

Each processes' log will list the clock rate for that process; each log is run for just over a minute. The log contains message receives and queue lengths, message sends, and the logical clock and system time for each of those.

## Design Journal
Following the example given in section, we initialize three separate processes with multithreading to simulate virtual machines, each with two threads: a listening consumer and a sending producer. The advantage of this structure is that global variables will be shared across threads in the same process, allowing for a shared clock value, message queue, and log; all desiderata of our simulation. Thus, we can easily create a P2P network with 3 machines each with 2 threads, as well as 6 connections (to represent the 6 ways that messages can be sent: all directed edges in the complete graph for 3 machines).

For each of three virtual machines, the consumer will always be listening on the socket; it will eventually receive two connections from the other two machines, and create threads to handle those. Whenever it receives a message, it instanteously adds it to the message queue for that machine.

On each machine, in its producer thread, we connect to the other two machine's sockets. It is via these connections that messages are sent. Within each machine's producer thread, we simulate the events per the spec: updating the internal logical clock value each tick and then generating a random integer, which determines whether to treat it as an internal event or sending a message to either one or both of the other machines.





