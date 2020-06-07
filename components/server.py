'''
This is the server
'''
from numpy import np

class Server:
    '''
    this is a machine class that is initiated with mu and 
    will service clients with an exponential distribution (mu)
    it will take a queue to hold clients when not available
    it will be connected to another server or system exit
    '''
    def __init__(self, mu, component_ID, queue, event_queue):
        self.mu = mu
        self.cID = component_ID
        self.is_available = True
        self.client = None
        self.queue = queue
        self.event_queue = event_queue
        
    def process_time(self):
        return np.random.exponential(self.mu)
    
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
        if self.queue.check():
            next_client = self.queue.get(t)
            self.put(next_client, t)

        # finally return the client
        return client