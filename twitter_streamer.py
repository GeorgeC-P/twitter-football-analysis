import json

from datetime import *

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from football_sentiment import twitter_connection, sentiment_juicer, pandas_juicer

auth = OAuthHandler(twitter_connection.key, twitter_connection.secret)
auth.set_access_token(twitter_connection.token, twitter_connection.token_secret)
api = tweepy.API(auth)

stop_words = set(stopwords.words("english"))
sid = SentimentIntensityAnalyzer()

timer = datetime.now() + timedelta(seconds=5)
neg_sent = 0
pos_sent = 0


class StreamTweets(StreamListener):
    def on_data(self, data):
        try:
            # clean tweet
            parsed_tweet = json.loads(data)
            tweet_text = parsed_tweet['text']
            break_tweet = word_tokenize(tweet_text)
            remove_stopwords = [word for word in break_tweet if not word in stop_words]
            cleaned_tweet = ' '.join(remove_stopwords)

            # NLTK stuffs
            sentiment_score = sid.polarity_scores(cleaned_tweet)
            for k in sorted(sentiment_score):
                if (k == 'neg' or k == 'pos') and sentiment_score[k] != 0.0:
                    # print (k, sentiment_score[k])
                    global neg_sent, pos_sent
                    if k == 'neg':
                        neg_sent += -sentiment_score[k]
                        sentiment_juicer.tweet_analyse(cleaned_tweet, k)
                    elif k == 'pos':
                        pos_sent += sentiment_score[k]
                        sentiment_juicer.tweet_analyse(cleaned_tweet, k)

            if datetime.now() > timer:
                #print('5 seconds elapsed'.format(timer))
                update_timer()
            return True

        except BaseException as e:
            print('error on data: %e' % str(e))
            return True

    def on_error(self, status):
        print(status)
        return True


def update_timer():
    global timer, neg_sent, pos_sent
    #print('the positive score was: {0}, the negative score was: {1}'.format(pos_sent,neg_sent))
    timer = datetime.now() + timedelta(seconds=5)
    pandas_juicer.twitter_sent_build_dict(pos_sent,neg_sent)
    neg_sent = 0
    pos_sent = 0
    return timer, neg_sent, pos_sent


twitter_stream = Stream(auth, StreamTweets())
twitter_stream.filter(track=['brexit'])
