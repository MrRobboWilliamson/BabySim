

class SimpleQueue:
    '''
    this is a queue first in last out style doesn't pay attention to
    anything and does not have a length limit
    '''
    def __init__(self, component_ID):
        self.container = list()
        self.cID = component_ID
        self.is_occupied = False
        self.length = 0
        
    def put(self, client, t):
        '''
        put a client in the queue
        '''
        client.record(t, self.cID, 'put')
        self.container.append(client)
        self.is_occupied = True
        self.length += 1
        
    def get(self, t):
        '''
        take the first client out of the queue
        '''
        # get the client from the top
        client = self.container.pop(0)
        client.record(t, self.cID, 'get')
        
        # check the length of the queue, if it's zero then 
        # flag is_occupied = False
        if len(self.container) == 0:
            self.is_occupied = False
            
        # return the client
        self.length =- 1
        return client