'''
This is the event queue the manages all of the events
'''

class EventQueue:
    '''
    This holds the events and ensures no concurrent events
    - init with time units and schedule concurrent events a very small unit apart
      using nanoseconds
    '''
    def __init__(self, time_units):
        # to store events and their details
        self.__queue = list()
        self.__details = dict()
        self.units = time_units
        self.cf = 1
        
        # set the conversion factor based on the units
        self.set_cf()
    
    def set_cf(self):
        '''
        check the time units and set the conversion factor 
        for converting to nano seconds
        '''
        if self.units == 'S':
            # divide by 1,000,000,000
            self.cf = 10**9
        elif self.units == 'M':
            self.cf = 10**9*60
        else:
            raise Exception('Unit error: only accepts "M" (minutes) or "S" (seconds)')
        
    def convert_time(self, delta):
        return delta*self.cf
        
    def get_units(self):
        return self.units
    
    def check_queue(self, st):
        # recursively checks that the small time does not
        # exist the returns a unique time to add to the list
        if st in self.__queue:
            st += 1
            self.check_queue(st)
        else:
            return st        
    
    def put_event(self, time, details):
        # conver time to nanoseconds
        small_time = self.cf * time
        
        # check queue and put event in the list
        st = self.check_queue(small_time)
        self.__queue.append(st)
        
        # sort the queue
        self.__queue.sort()
        
        # add the event details
        self.__details[st] = details
        
    def get_event(self):
        # return the next event
        t = self.__queue.pop(0)
        big_time = t / self.cf
        details = self.__details.pop(t)
        return big_time, details