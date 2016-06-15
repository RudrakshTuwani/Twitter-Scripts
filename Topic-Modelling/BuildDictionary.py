import pandas as pd
import enchant
import string
import pickle

# Reads tweets into a df.
loc = "C:/Users/Vedika/Desktop/Twitter/Tweets PreProcessed/TweetsTopicModelling.csv"
tweets = pd.read_csv(loc)

# Set up enchant.
d = enchant.Dict("en_US")

# function to remove any punctuations from words.
def remove_punctuation(s):
    s = s.translate(None, string.punctuation)
    if len(s) == 0:
        return None
    else:
        return s

# Gets srongly spelt words from text and asks user for correct spelling.
def build_dictionary(text,d, corrected_words, ignore_list):
    words = text.split()
    final_words = [remove_punctuation(str(word)) for word in words]
    for word in final_words:
        if not d.check(word):
            if (word not in corrected_words) & (word not in ignore_list):
                print "Please enter the correct spelling for %s"%word
                correction = raw_input()
                if correction != '':
                    corrected_words[word] = correction
                else:
                    ignore_list.append(word)
    return corrected_words, ignore_list
    
corrected_words = {}
ignore_list = []
weird_texts = []
for i in range(len(tweets)):
    text = tweets.ProcessedText[i]
    try:
        corrected_words, ignore_list = build_dictionary(text,d,corrected_words, ignore_list)  
    except:
        weird_texts.append(i)

tweets = tweets.drop(tweets.index[weird_texts])
tweets.index = [i for i in range(len(tweets))]
    
pickle.dump(corrected_words, open("E:/Rudraksh/CorrectedWords.p", "wb"))
pickle.dump(ignore_list, open("E:/Rudraksh/IgnoreList.p", "wb"))