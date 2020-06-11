'''
This is the main module for running simulations
'''
from event_queue.event_queue import EventQueue
from components.client import Client
from components.server import Server
from components.queue import SimpleQueue
from event_logger.logger import Logger
from network.network import Network

import numpy as np
import pandas as pd

### get the data
data = pd.read_csv(r'..\data.csv')
print(data.head())

#### define the system
# we will have a distributor node that allocates between the servers
# allocation will depend on the size of the queue
# otherwise random

UNITS = 'M'
# INTER = 

# def inject(sampl)


def run_simulation(period, time_units, lam):
    # lambda corresponds to the distribution of the inter-arrival time
    # mu1 and mu2 are the time to service distributions for server1 and server2
    # assume time is in seconds and we are plotting an 8 hour shift of operations
    T = period

    # parameters
    lam = lam
    mu1 = 1
    mu2 = 2

    # initiate time
    t = 0

    # initiate components and put them in a dictionary
    eq = EventQueue(time_units)
    q1 = SimpleQueue('q1')
    s1 = Server(mu1, 's1', q1, eq)
    q2 = SimpleQueue('q2')
    s2 = Server(mu2, 's2', q2, eq)
    nodes = dict()
    nodes['s1'] = s1
    nodes['s2'] = s2

    # the edges define the connetions in the network
    # server 1 is connected to server 2 and after server 2
    # the client is done "end"
    edges = [('s1', 's2'), ('s2', 'end')]

    # put into network - this will help us call the next node
    system = Network(edges)

    # schedule the first event by instantiating a client and 
    # adding the first event to the event queue
    # schedule the next injection too
    cindex = 0
    t1 = np.random.exponential(lam)
    t += t1
    event_log = Logger()
    c0 = Client(t, cindex, event_log)
    injection_point = 's1'
    details = dict(client=c0, component=injection_point, action='inject')
    eq.put_event(t, details)

    # do while t is less than T
    iteration = 0
    while t < T:
        try:
            # get the next event on the list
            t, details = eq.get_event()

            # get the event details
            clnt = details['client']
            comp_id = details['component']
            action = details['action']

            # this is the injection and will schedule a put at the injection point
            # and schedule the next injection
            if action == 'inject':
                # put client and schedule get
                # the component will return the new time and the next event
                # next_event will be none if the client is placed in a queue
                nodes[comp_id].put(clnt, t)
                cindex += 1

                # schedule the next injection
                tn = t + np.random.exponential(lam)
                cn = Client(tn, cindex, event_log)
                details = dict(client=cn, component=injection_point, action='inject')
                eq.put_event(tn, details)

            # action the event and schedule the another event
            elif action == 'put':
                # put client - component will schedule get
                nodes[comp_id].put(clnt, t)

            elif action == 'get':
                # get client and schedule put in the next component
                client = nodes[comp_id].get(t)

                # get the next component in the network
                next_comp = system.get_next(comp_id)

                # schedule next put for the client
                # if the next_comp is end then destroy the client
                if next_comp == 'end':
                    del(client)
                else:
                    details = dict(client=client, component=next_comp, action='put')
                    eq.put_event(t, details)
        except Exception as ex:
            print(f"Error on iteration {iteration}:", ex)
            print(event_log.get_logs().tail())
            break

        iteration += 1
        
    return event_log.get_logs()


if __name__ == "__main__":
    logs = run_simulation(period=20000, time_units='S', lam=2.5)
    print(logs.head())