'''
This file will have common analysis scripts
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def confidence_interval(x, variable_name):
    mean = np.mean(x)
    std = np.std(x)
    se = 1.96*std/np.sqrt(len(x))
    lower = mean - se
    upper = mean + se
    print(f"{variable_name} 95% CI is ({lower:0.2f}, {upper:0.2f})")

def plot_qocc(df, title, order):
    # plot the queue occupancy over time
    counter = dict(put=1, get=-1)
    df['counter'] = df['event'].map(counter)
    df = df.sort_values(['time_stamp'])

    # group by component and do a cumulative sum to get the occupancy
    df['occupancy'] = df.groupby(['comp_id'])['counter'].apply(lambda x: np.cumsum(x))

    # plot the queue occupancies
    fig, ax = plt.subplots(figsize=[10, 5])
    queues = df[df['comp_id'].str[0]=='q']
    sns.lineplot(x='time_stamp', y='occupancy', hue='comp_id', hue_order=order,
                 data=queues, drawstyle='steps-post', alpha=0.5)
    plt.title(title)

def get_cdf(x):
    # return a cdf from a vector
    n = len(x)
    x = np.sort(x)
    pos = np.array(range(1, n+1))
    prb = pos / n
    
    # return values, and probabilities
    return x, prb

class ConsoleBar:
    def __init__(self, num_ticks):
        # check that end - start is greater than one and that they are both integers
        if type(num_ticks) is not int:
            raise TypeError('arg "num_ticks" must be type int')
        if num_ticks < 1:
            raise ValueError("num_ticks not > 0")

        #  get the absolute size and normalise
        self.num_ticks = num_ticks
        self.ticker = 0

        # start the ticker
        # print('\r   {:>3.0f}%[{: <101}]'.format(0, '='*0+'>'), end='\r')

    def tick(self, step=1):
        print_end = '\r'
        self.ticker += step
        if self.ticker > self.num_ticks:
            self.ticker = self.num_ticks
            # print a warning
            print('Warning: The ticker is overreaching and has been capped at the end point', end='\r')
        elif self.ticker == self.num_ticks:
            print_end = '\n'

        progress = int((self.ticker/self.num_ticks)*100)
        print('   {:>3.0f}%[{: <101}]'.format(progress, '='*progress+'>'), end=print_end)
