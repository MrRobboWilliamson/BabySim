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