from collections import Counter
from nltk.tokenize import word_tokenize

def tweet_analyse(tweet, sent):
    count_all = Counter()
    count_all.update(word_tokenize(tweet))
    print(count_all.most_common(5))
    print(sent)
    return True;