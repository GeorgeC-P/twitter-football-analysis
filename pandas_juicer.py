import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

tweets_over_time = {}

def twitter_sent_build_dict(pos_sent, neg_sent):
    tweets_over_time[datetime.datetime.now()] = pos_sent + neg_sent
    #print(tweets_over_time)
    s = pd.Series(tweets_over_time)
    s.index.name='date'
    #s.reset_index()
    if len(s) > 80:
        s.plot()
        plt.show()



