import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

tweets_over_time = {}
volume = {}


def twitter_sent_build_dicts(pos_sent, neg_sent, count):
    tweets_over_time[datetime.datetime.now()] = pos_sent + neg_sent
    # print(tweets_over_time)
    volume[datetime.datetime.now()] = count
    # print(volume)
    if len(volume) % 5:
        volume_analyser(volume)


def volume_analyser(volume):
    s = pd.Series(volume)
    s.index.name='date'
    print(s)
    # if len(s) > 80:
    #     s.plot()
    #     plt.show()
    #





    # s = pd.Series(tweets_over_time)
    # s.index.name='date'
    # #s.reset_index()
    # if len(s) > 80:
    #     s.plot()
    #     plt.show()



