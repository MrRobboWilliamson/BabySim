# BabySim
BabySim is a simple simulation tool developed to undertake discrete event simulation as part of an assignemt for the Statistical Methods for Data Science course under the Master of Data Science program at the University of Queensland, Australia.

Please see RobWilliamson_A4, from Question 2 onwards for use case.

## Code files
BabySim contains the following codefiles - each is explained below in the context of undertaking a simulation to determine the minimum service desk requirement to satisfy quality of service standards.

### Main file: run.py
Example uitilisation of BabySim to undertake a discrete event simulation of a service desk at an Airport 

#### Initiation
This file initiates the system parameters and runs the simulations. The example contains 10 scenarios developed with 1 to 10 servers made available for customers of a fictitious AirSecure company.

First an event queue is instantiated, then n servers are instantiated each with a simple queue, an id and pointers to the service time samples and the event queue.

Next a distributor is instantiated with the list of servers. A dictionary of server ids and pointers is created as nodes along with a list of origin destination tuples representing their connections. These are used to instantiate a network representing the Air Secure system.

#### Start simulation
The function run_simulation is executed with the system and event queue as input. This function schedules the first event and executes the event loop. First the simulation run time 𝑇 is set and the event logger is instantiated along with the first client. The client is instantiated with a unique id and a pointer to the event logger to record events (actions) as they occur. Finally, the first inject is scheduled and the simulation enters the event loop.

#### Event loop
The event loop repeats while t < T and takes the top event from the event queue. Events contain the time of the event and the event details. Details consist of a client, component and action, which is either:

• Inject – put a client into the injection point (first node), create a new client, sample the inter-arrival time and schedule the next inject action.

• Put – put the client in the component

• Get – get a client from the component, get the next component from the network – if the next component is “end”, remove the client or else schedule its put action in the next node (puts are never scheduled as the next node is always “end” in the Air Secure System)

With each event the system time is set to the event time and the event loop will continue until 𝑡 ≥ 𝑇 – as the event time is set in the loop it will execute one final loop when 𝑡 ≥ 𝑇.

After exiting the event loop, the event logs are returned and saved to file.

### Network (system): network.py
Contains system nodes (components) and edges (connections)

Represents the nodes and edges that make up the system. It is used to determine the injection point (where new clients enter the system when an inject action is scheduled) and the next node a client is to go after a get action is executed from a server and a put action is scheduled. The next node is returned by executing the next_node method.

### Event queue: event_queue.py
Priority queue that prioritises earliest event

A priority queue that maintains the time and details of scheduled events. Events are prioritised by the earliest time. Details include a client, component and action, to determine which client is actioned where. The event queue ensures non-concurrent events by incrementing a subsequent event by 1 nanosecond, if two events share an event time. Events are scheduled via the put_event method and the top event is returned via the get_event method.

### Logger: logger.py
Keeps a record of all put and get events

A global event logger – each client receives a pointer to the event logger that is accessed by the simple queue or server components to record when a client’s action is executed with that component (i.e. put or get). Events are recorded via the record method by creating a dictionary with the time, client id, component id and action of each event. The dictionary is added to a list and all the records are returned as a pandas dataframe via the get_logs method.

### Client: client.py
Customer representation

Created when an inject action is scheduled with a unique identifier and given a pointer to the logger to record put and get actions in components. It interacts with components through the record method to record events taking the event time, component id and action.

### Distributor: distributor.py
Allocates clients to components when there is a choice

The distributor is instantiated with a list of servers it is connected to and interacts with the event loop via the put method. This method takes a client and event time. It randomly distributes customers to service desks when more than one is available. If not, the desk with the smallest queue will be allocated as per the customer behaviour findings. If more than one queue has the minimum length, a random choice will be made between those.

### Server: server.py
Service desk queue representation

Represents a system component that processes clients. On creation a server is allocated a service time distribution, a queue and a pointer to the event queue. The service time distribution can be provided as an exponential distribution parameter μ or a sample of service times. Service times are chosen when a client goes into service, either uniformly at random from the samples provided or sampled from the exponential distribution.

The server interacts with the system loop through the put and get methods. A put, puts the client straight in the queue and simultaneously processes the head of the queue. If the server is available, the client at the head of the queue is retrieved, it’s put action is recorded and it’s get action is scheduled in the event queue. If the server is in service, it stays in the queue. 

When a get is executed in the system loop, the event is recorded with the client and the client is returned to the event loop. If the simple queue is occupied, the head of the queue is processed to put the next client into service.

### Simple queue
Service desk queue representation

A container that holds clients as a first in first out queue. It has a put and get method. The put method takes a client and time, appends the client to the tail of the container and records a put event with the client. The get method takes a client from the head of the queue and records a get event with the client.











