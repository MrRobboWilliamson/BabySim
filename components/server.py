'''
This is the server
'''
import numpy as np

class Server:
    '''
    this is a machine class that is initiated with mu and 
    will service clients with an exponential distribution (mu)
    it will take a queue to hold clients when not available
    it will be connected to another server or system exit
    '''
    def __init__(self, component_ID, queue, event_queue, mu=None, samples=None):
        self.mu = mu
        self.cID = component_ID
        self.is_available = True
        self.client = None
        self.queue = queue
        self.event_queue = event_queue
        self.samples = samples

        if samples is not None:
            self.process_time = self.take_sample
        else:
            self.process_time = self.exponential

    # for using with a parameter mu        
    def exponential(self):
        return np.random.exponential(self.mu)

    # for using a random sample
    def take_sample(self):
        return np.random.choice(self.samples)

    # for a given data set    
    def record(self, next_action):
        '''
        sends and event record to the event queue
        '''
        return dict(client=self.client, component=self.cID, action=next_action)
    
    def put(self, client, t):
        '''
        if not busy, set to busy
        return the processing time
        communicate with the client
        store the client
        
        if busy put in the queue
        '''
        if self.is_available:
            client.record(t, self.cID, 'put')
            self.client = client
            self.is_available = False
            
            # schedule the get
            service_time = self.process_time()
            self.event_queue.put_event(t + service_time,
                                 self.record('get'))        
        else:
            # add this client to the queue
            self.queue.put(client, t)
            return None
    
    def get(self, t):
        # return the client and record the event        
        client = self.client
        client.record(t, self.cID, 'get')
        self.is_available = True
        
        # check if there is another client in the queue
        if self.queue.is_occupied:
            next_client = self.queue.get(t)
            self.put(next_client, t)

        # finally return the client
        return client