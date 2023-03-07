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

This enables the die roll for the event to be isolated to the producer thread, which minimizes overheard. Allowing the consumer thread to listen in a busy loop without having to send also prevents deadlock, and circumvents needing to wait during send, which sometimes causes received messages to be jumbled and concatenating logical clock values.

## Experiment Observations
In the logs, we see that there is generally greater drift when the clock rates between the three machines differ the most (e.g. `d10-1-2-4` and `d10-1-2-5`).

Indeed, we note that the Lamport clock construction ensures that the logical clock values are determined by the largest logical value in a distributed system. Then, the synchronization of the slower clocks is only determined by their tick speeds, as well as the send rate of the fastest clock. Since the fastest logical clock will tick by exactly its clock rate each second, the final "true" logical clock value of any experiment should be roughly `60*max`, where `max` is the largest clock rate of the three processes; any deviations are due to drift.

Sometimes, if the send rate of the fastest machine is greater than the tick rate of the slowest machine, then the slowest machine will experience increasing drift and simply never synchronize. That is, the queue length continues to grow until the slow machine is hopelessly out of sync with the others. Mathematically, this occurs when `max*2/d > min`, where `d` is the dice size for the event probabilities, and `max` and `min` refer to the largest and smallest clock rates, respectively. This can be most clearly seen in `d5-1-4-7`, where the final queue length is 118 by the end for the slowest macine, and we see that the queue has been steadily growing throughout the runtime of the experiment.

Conversely, when there is a smaller variation in clock cycles and smaller internal events (thus relatively higher send rates), the machines tend to stay more synchronized. When the clock rates do not differ much, there are few jumps due to message receives and the clocks stay roughly aligned (e.g. `d10-1-2-2` and `d10-2-3-3`). 