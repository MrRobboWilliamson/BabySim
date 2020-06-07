'''
This module will manage the flow of clients between nodes

Will need to implement a splitter/decision node that assigns the next node based on a condition
'''


class Network:
    '''
    Network of nodes
    '''
    def __init__(self, edges):
        self.network = self.generate_network(edges)
        
    def generate_network(self, edges):
        '''
        creates a dictionary of nodes as keys and the next node as the value
        '''
        network = dict()
        for e in edges:
            network[e[0]] = e[1]            
        return network
        
    def get_next(self, node):
        return self.network[node]