"""
This distributes clients to a list of connected nodes based on a condition
"""
import numpy as np

class Distributor:
    """
    conditions:
    - is available - first look for available nodes, then
    - smallest - looks for the node with the smallest queue
    - potential for others

    otherwise (used when more than one connection satisfies that condition):
    - uniform random

    connections:
    - these are components (objects) to distribute clients to based on the conditions and otherwise
    """
    def __init__(self, connections, condition, otherwise):
        # connections will be a list of the service objects connected to this component
        self.connections = connections

        # set the condition behaviour
        if condition == 'smallq':
            self.condition = self.get_smallest
        else:
            raise Exception('Distributor Error: Condition does not exist')

        # set the otherwise behaviour
        if otherwise == 'random':
            self.otherwise = self.get_random
        else:
            raise Exception('Distributor Error: Otherwise option does not exist')
        
    def get_smallest(self):
        # first check if any of the connections are available
        available = [idx for idx, node in enumerate(self.connections) if node.is_available]

        # if none are available look for the smallest queue
        if len(available) > 0:
            return available
        else:
            # for condition smallest, return a list of components with length == min(lengths)
            # print(self.connections[0].queue.length)
            lengths = [node.queue.length for node in self.connections]
            minval = min(lengths)
            smallest = [idx for idx, l in enumerate(lengths) if l==minval]
            return smallest

    def get_random(self, short_list):
        # for if condiction or otherwise are "random" return a uniform random selection of
        # given elements
        return np.random.choice(short_list)

    def put(self, client, t):
        """
        puts the client in a connected node
        """
        # get the index of the node that satisfies the condition and otherwise
        short_list = self.condition()
        node_id = self.otherwise(short_list)

        # put the client in the selected node
        selection = self.connections[node_id]
        selection.put(client, t)
