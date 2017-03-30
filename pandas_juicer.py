import pandas as pd
import datetime, time
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

tweets_over_time = {}
volume = {}


def twitter_sent_build_dicts(pos_sent, neg_sent, count):
    tweets_over_time[datetime.datetime.now()] = pos_sent + neg_sent
    volume[datetime.datetime.now()] = count
    if len(volume) % 10 == 0:
        volume_analyser(volume)


def volume_analyser(volume):
    vol_graph = pd.Series(volume)
    vol_graph.index.name='date'
    print (len(vol_graph))
    vol_graph.plot()
    plt.show()






    # s = pd.Series(tweets_over_time)
    # s.index.name='date'
    # #s.reset_index()
    # if len(s) > 80:
    #     s.plot()
    #     plt.show()



