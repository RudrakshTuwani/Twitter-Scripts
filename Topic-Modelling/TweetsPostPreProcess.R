# Most of the preprocessing has been done in Python. 
tweets <- read.delim("E:/Data Science/Safecity/Twitter/Tweets PreProcessed/TweetsforWC.csv", stringsAsFactors=FALSE)
tweets$IsReply = as.factor(tweets$IsReply)

# Remove replies
tweets = subset(tweets,IsReply == 0)

# Tweet text PreProcessing.
library(tm)
library(SnowballC)

corpus = Corpus(VectorSource(tweets$ProcessedText))

#Convert to lowercase
corpus = tm_map(corpus, tolower)
corpus = tm_map(corpus, PlainTextDocument)

#remove potentially problematic symbols
toSpace <- content_transformer(function(x, pattern) { return (gsub(pattern, " ", x, fixed = TRUE))})
corpus <- tm_map(corpus, toSpace, "-")
corpus <- tm_map(corpus, toSpace, "'")
corpus <- tm_map(corpus, toSpace, "\"")
corpus <- tm_map(corpus, toSpace, ".")
corpus <- tm_map(corpus, toSpace, "#")
corpus <- tm_map(corpus, toSpace, ",")
corpus <- tm_map(corpus, toSpace, "?")
corpus <- tm_map(corpus, toSpace, "!")
corpus <- tm_map(corpus, toSpace, "&")
corpus <- tm_map(corpus, toSpace, ";")
corpus <- tm_map(corpus, toSpace, ":")

#Strip Whitespace
corpus = tm_map(corpus, stripWhitespace)

# Remove stopwords
# Remove custom words.
myStopwords = c("can", "say","one","way","use", "also","tell","will",
                "much","need","take","tend","even","like","particular",
                "rather","said","get","well","make","ask","come","end",
                "first","two","help","often","may","might","see",
                "something","thing","point","post","look","right","now",
                "think","'ve ","'re ","another","put","set","new","good",
                "want","sure","kind","larg","yes,","day","etc","quit",
                "since","attempt","lack","seen","aware","little","ever",
                "moreover","though","found","able","enough","far",
                "earlier","away","achieve","draw","last","never","brief",
                "bit","entire","brief","great","lot","amp", "r", "u", 
                "s", "t", "d")
corpus = tm_map(corpus, removeWords, 
                c(stopwords(kind = "en"), myStopwords))
                                       
dataframe <- data.frame(text=unlist(sapply(corpus, `[`, "content")), stringsAsFactors=F)
tweets$ProcessedText = dataframe$text

write.csv(tweets, file = "E:/Data Science/Safecity/Twitter/Tweets PreProcessed/TweetsTopicModelling.csv", 
          row.names = FALSE)
#####  Run Python Script now for spell checking and correction ####