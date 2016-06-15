import pandas as pd
import pickle

# Reads tweets into a df.
loc = "E:/Data Science/Safecity/Twitter/Tweets PreProcessed/TweetsTopicModelling.csv"
tweets = pd.read_csv(loc)

# Import corrected words as well as ignore list.
loc = "E:/Data Science/Safecity/Twitter/Pickles/"

corrected_words = pickle.load(open(loc + "CorrectedWords.p", "rb"))
ignore_list = pickle.load(open(loc+"IgnoreList.p","rb"))

# Decompose tweets and then compose again with corrected spellings.

def spellcorrection(text, cw):
    try:
        all_words = text.split()
        final_words = []    
        for word in all_words:
            if word in cw:
                word = cw[word]
            final_words.append(word)
        
        s = ''
        for word in final_words:
            s = s + word + ' '
        return s
    except:
        return ''

tweets['FinalText'] = tweets.ProcessedText.apply(spellcorrection, cw=corrected_words)

# Remove empty tweets or tweets with strange characters.
rogue_tweets = []    
for i in range(len(tweets)):
    if len(tweets.FinalText[i]) == 0:
        rogue_tweets.append(i)

tweets = tweets.drop(tweets.index[rogue_tweets])
tweets.index = [i for i in range(len(tweets))]

tweets.to_csv("E:/Data Science/Safecity/Twitter/Tweets PreProcessed/TweetsTopicModellingSpellCorrected.csv", 
              sep='\t')
