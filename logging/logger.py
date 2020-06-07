'''
This module contains all of the logging stuff
'''
import pandas as pd

class Logger:
    '''
    to pass to the clients to record their experiences
    '''
    def __init__(self):
        self.all_records = list()
        
    def record(self, time, client, component, action):
        self.all_records.append(dict(time_stamp=time, clnt_id=client, comp_id=component, event=action))
        
    def get_logs(self):
        return pd.DataFrame(self.all_records)