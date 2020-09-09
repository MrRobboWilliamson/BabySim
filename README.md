# BabySim
## Introduction
BabySim is a simple simulation tool developed to undertake discrete event simulation as part of an assignemt for the Statistical Methods for Data Science course under the Master of Data Science program at the University of Queensland, Australia.

## Modules
BabySim contains the following codefiles

### Main file: run.py
Executes actions in the event queue
and schedules the next action

#### Initiation
This file initiates the system parameters and runs the simulations. The example contains 10 scenarios developed with 1 to 10 servers made
available for customers of a fictitious AirSecure company.

First an event queue is instantiated, then n servers are instantiated each with a simple queue, an id and pointers to the service
time samples and the event queue.

Next a distributor is instantiated with the list of servers. A dictionary of server ids and pointers is created as nodes along with a
list of origin destination tuples representing their connections. These are used to instantiate a network representing the Air
Secure system.

#### Start simulation
The function run_simulation is executed with the system and event queue as input. This function schedules the first event and
executes the event loop. First the simulation run time 𝑇 is set and the event logger is instantiated along with the first client. The
client is instantiated with a unique id and a pointer to the event logger to record events (actions) as they occur. Finally, the first
inject is scheduled and the simulation enters the event loop.

#### Event loop
The event loop repeats while t < T and takes the top event from the event queue. Events contain the time of the event and the
event details. Details consist of a client, component and action, which is either:

• Inject – put a client into the injection point (first node), create a new client, sample the inter-arrival time and schedule the
next inject action.

• Put – put the client in the component

• Get – get a client from the component, get the next component from the network – if the next component is “end”,
remove the client or else schedule its put action in the next node
(puts are never scheduled as the next node is always “end” in the Air Secure System)

With each event the system time is set to the event time and the event loop will continue until 𝑡 ≥ 𝑇 – as the event time is set in
the loop it will execute one final loop when 𝑡 ≥ 𝑇.

After exiting the event loop, the event logs are returned and saved to file.

### Network (system): network.py
Contains system nodes (components)
and edges (connections)

Represents the nodes and edges that make up the system. It is used to determine the injection point (where new clients enter
the system when an inject action is scheduled) and the next node a client is to go after a get action is executed from a server and
a put action is scheduled. The next node is returned by executing the next_node method.

### Event queue: event_queue.py





