'''
These are clients
'''

# create a client class
class Client:
    '''
    this is a client class that is initiated with an
    arrival time
    '''
    def __init__(self, ID, logger):
        self.ID = ID
        self.logger = logger
        
    def record(self, t, comp_id, event):
        # returns the record of experiences in the system
        self.logger.record(t, self.ID, comp_id, event)