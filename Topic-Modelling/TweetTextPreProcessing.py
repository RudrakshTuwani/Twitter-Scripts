import pandas as pd
import re

def main():
    # Reads files from Analytics Dashboard into df.
    loc = "E:/Data Science/Safecity/Twitter/Tweets Dataset/"
    TweetActv1 = pd.read_csv(loc + 'April15.csv')
    TweetActv2 = pd.read_csv(loc + 'May15.csv')
    TweetActv3 = pd.read_csv(loc + 'June15.csv')
    TweetActv4 = pd.read_csv(loc + 'July15.csv')
    TweetActv5 = pd.read_csv(loc + 'Aug15.csv')
    TweetActv6 = pd.read_csv(loc + 'Sep15.csv')
    TweetActv7 = pd.read_csv(loc + 'Oct15.csv')
    TweetActv8 = pd.read_csv(loc + 'Nov15.csv')
    TweetActv9 = pd.read_csv(loc + 'Dec15.csv')
    TweetActv10 = pd.read_csv(loc + 'Jan.csv')
    TweetActv11 = pd.read_csv(loc + 'Feb.csv')
    TweetActv12 = pd.read_csv(loc + 'March.csv')
    TweetActv13 = pd.read_csv(loc + 'April.csv')
    TweetActv14 = pd.read_csv(loc + 'May.csv')

    # Concat Data
    TweetActv = pd.concat([TweetActv1,
                           TweetActv2,
                           TweetActv3,
                           TweetActv4,
                           TweetActv5,
                           TweetActv6,
                           TweetActv7,
                           TweetActv8,
                           TweetActv9,
                           TweetActv10,
                           TweetActv11,
                           TweetActv12,
                           TweetActv13,
                           TweetActv14])


    #Cleaning Data by getting specific columns
    col_list = ['Tweet id', 'Tweet text','impressions','engagements','engagement rate']
    TweetActv = TweetActv[col_list]
    
    TweetActv = PreProcess(TweetActv)
    TweetActv.to_csv("E:/Data Science/Safecity/Twitter/Tweets PreProcessed/TweetsforWC.csv", 
                 sep='\t', encoding='utf-8')
                 
def PreProcess(TweetActv):
    # Identify which tweets are replies.
    def is_reply(s):
        if s[0] == '@':
            return 1
        else:
            return 0
    
    TweetActv['IsReply'] = TweetActv['Tweet text'].apply(is_reply)
    
    # Extract or Remove Tagged People
    def remove_tagged(s):
        tagged = list(part for part in s.split() if (part.startswith('@')))
        words = list(s.split())
        final_words = [word for word in words if (word not in tagged)]
        if len(final_words) == 0:
            return ''
        else:
            a = ''
            for word in final_words:
                a = a + word + ' '
            return a
    
    def extract_tagged(s):
        tagged = list(part for part in s.split() if (part.startswith('@')))
        if len(tagged) == 0:
            return ''
        else:
            a = ''
            for tag in tagged:
                a = a + tag + ' '
            return a

    # Extract links or remove links.
    def extract_links(s):
        links = re.findall(r'(https?://\S+)', s)
        a = ''
        for link in links:
            a = a + link + ' '
        return a

    def remove_links(s):
        links = re.findall(r'(https?://\S+)', s)
        words = list(s.split())
        final_words = [word for word in words if (word not in links)]
        a = ''
        for word in final_words:
            a = a + word + ' '
        return a


    TweetActv['Links'] = TweetActv['Tweet text'].apply(extract_links)
    TweetActv['ProcessedText'] = TweetActv['Tweet text'].apply(remove_links)

    TweetActv['ProcessedText'] = TweetActv['ProcessedText'].apply(remove_tagged)
    TweetActv['Tags'] = TweetActv['Tweet text'].apply(extract_tagged)

    return TweetActv
    
if __name__ == "__main__":
    main()