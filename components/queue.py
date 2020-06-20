class SimpleQueue:
    '''
    this is a first in first out queue with no length limit
    '''
    def __init__(self, component_ID):
        self.container = list()
        self.cID = component_ID
        self.is_occupied = False
        self.length = 0

    def check_occupation(self, inc):
        self.length += inc        
        if self.length > 0:
            self.is_occupied = True
        elif self.length < 0:
            raise Exception("Length of queue should not be negative")
        else:
            self.is_occupied = False

    def put(self, client, t):
        '''
        put a client in the queue
        '''
        client.record(t, self.cID, 'put')
        self.container.append(client)
        self.check_occupation(1)
        
    def get(self, t):
        '''
        take the first client out of the queue
        '''
        # get the client from the top
        client = self.container.pop(0)
        self.check_occupation(-1)
        client.record(t, self.cID, 'get')
            
        # return the client
        return client