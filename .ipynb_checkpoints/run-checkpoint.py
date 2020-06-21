'''
This is the main module for running simulations
'''
from event_queue.event_queue import EventQueue
from components.client import Client
from components.server import Server
from components.queue import SimpleQueue
from components.distributor import Distributor
from event_logger.logger import Logger
from network.network import Network
from utils.tools import ConsoleBar

import numpy as np
import pandas as pd

### get the data and define the global parameters
data = pd.read_csv(r'..\data.csv')
INJECT_SAMPLES = data['inter_arrival_time'].values
SERVICE_SAMPLES = data['service_time'].values
PERIOD = 3000
UNITS = 'M'

def run_simulation(system):
    # lambda corresponds to the distribution of the inter-arrival time
    # mu1 and mu2 are the time to service distributions for server1 and server2
    # assume time is in seconds and we are plotting an 8 hour shift of operations
    T = PERIOD

    # initiate time and client index
    t = 0
    cindex = 0

    # schedule the first event by instantiating a client and 
    # adding the first event to the event queue
    # schedule the next injection too
    t1 = np.random.choice(INJECT_SAMPLES)
    t += t1
    event_log = Logger()
    c0 = Client(cindex, event_log)
    injection_point = system.injection_point
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
                system.nodes[comp_id].put(clnt, t)
                cindex += 1

                # schedule the next injection
                tn = t + np.random.choice(INJECT_SAMPLES)
                cn = Client(cindex, event_log)
                details = dict(client=cn, component=injection_point, action='inject')
                eq.put_event(tn, details)

            # action the event and schedule another event
            # don't think this actually happens
            elif action == 'put':
                # put client - component will schedule get
                system.nodes[comp_id].put(clnt, t)

            elif action == 'get':
                # get client and schedule put in the next component
                client = system.nodes[comp_id].get(t)

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
    
    ### main body of the simulation ###
    # for this task we can create a range of scenarios where we have 1 to 10 service desks
    N = 10
    num_servers = range(1, N+1)
    bar = ConsoleBar(N)
    results = list()
    print("Running simulation")
    for n in num_servers:
        # create an event queue
        eq = EventQueue(UNITS)

        # create n servers and n queues (one per server)
        servers = [Server(component_ID=f"s{idx}", queue=SimpleQueue(f"q{idx}"), event_queue=eq, samples=SERVICE_SAMPLES) for idx in range(n)]

        # create the distributor that distributes to the smallest queue and random otherwise
        d0 = Distributor(servers, "smallq", "random")

        # define the network as nodes and edges
        # nodes
        nodes = {srvr.cID:srvr for srvr in servers}
        nodes['d0'] = d0

        # all nodes connect to the distributor, but this won't need to be defined
        # as the distributor stores it's connections
        # this is a simple system, so each service connects to an endpoint
        edges = [(srvr.cID, 'end') for srvr in servers]
        system = Network(edges, nodes, injection_point='d0')

        # run the simulation and get the logs
        scenario_log = run_simulation(system=system)

        # label the scenario
        scenario_log['scenario'] = n
        results.append(scenario_log)
        bar.tick()

    print("Simulation finished")

    # concatenate the results and save to file
    results = pd.concat(results).reset_index(drop=True)
    results.to_csv("sim_results.csv", index=False)



