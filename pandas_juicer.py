import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib import style

from football_sentiment import config

tweets_over_time = []
volume = {}


def twitter_sent_build_dicts(pos_sent, neg_sent, count):
    now = datetime.datetime.now()
    tweets_over_time.append((now, pos_sent, neg_sent, count))
    volume[datetime.datetime.now()] = count
    multi_graph(tweets_over_time)
    if len(volume) % 10 == 0:
        volume_analyser(volume)


def volume_analyser(volume):
    vol_graph = pd.Series(volume)
    vol_graph.index.name='date'
    print (len(vol_graph))
    vol_graph.plot()
    plt.show()


def multi_graph(tweets_over_time):
    labels = ['date_time', 'pos_sent', 'neg_sent', 'count']
    df = pd.DataFrame.from_records(tweets_over_time, columns=labels)
    df.set_index('date_time', inplace = True)
    if len(df) > 5:
        df.iplot(secondary_y=['count'], filename='test_second_y')