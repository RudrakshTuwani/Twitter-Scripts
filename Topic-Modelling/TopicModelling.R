# Post the running of python script for building dictionary and spell
# correction.

tweets <- read.delim("E:/Data Science/Safecity/Twitter/Tweets PreProcessed/TweetsTopicModellingSpellCorrected.csv", 
                     stringsAsFactors=FALSE)

# Tweet text PreProcessing.
library(tm)
library(SnowballC)

corpus = Corpus(VectorSource(tweets$FinalText))

# Remove any punctuation that might have creeped in.
corpus = tm_map(corpus, removePunctuation)
corpus = tm_map(corpus, PlainTextDocument)

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

# Remove whitespace.
corpus = tm_map(corpus, stripWhitespace)
corpus = tm_map(corpus, PlainTextDocument)

# Stem Document.
library(SnowballC)
corpus = tm_map(corpus, stemDocument)

# Create DocumentTermMatrix.
dtm = DocumentTermMatrix(corpus)

#convert rownames to TweetID
rownames(dtm) = tweets$Tweet.text

#collapse matrix by summing over columns
freq <- colSums(as.matrix(dtm))

#length should be total number of terms
length(freq)

#create sort order (descending)
ord <- order(freq,decreasing=TRUE)

#List top 10 terms in decreasing order of freq.
freq[ord][1:10]

# Remove tweets which have no words.
rowTotals <- apply(dtm , 1, sum)          # Find the sum of words in each Document
dtm.new   <- dtm[rowTotals> 0, ]          # remove all tweets without words

#load topic models library and ldatuning library
library(topicmodels)
library(ldatuning)

# Find the optimum no. of topics
a = ldatuning::FindTopicsNumber(dtm.new, topics = seq(2,20,1))
ldatuning::FindTopicsNumber_plot(a)

#Set parameters for Gibbs sampling
burnin = 5000
iter = 2000
thin = 500 
seed = list(2003,5,63,100001,765, 420, 2709, 4182, 1001, 2050)
nstart = 10
best = TRUE

#Number of topics, ldatuning gives 9.
k = 13


#Run LDA using Gibbs sampling
ldaOut = LDA(dtm.new,k, method="Gibbs", control=list(nstart=nstart, seed = seed, best=best, burnin = burnin, iter = iter, thin=thin))

#write out results
#docs to topics
ldaOut.topics = as.matrix(topics(ldaOut))
write.csv(ldaOut.topics,file=paste("E:/Data Science/Safecity/Twitter/Tweets PreProcessed/LDAGibbs",k,"DocsToTopics.csv"))

#Get modified tweets dataset along with topics.
a = as.data.frame(as.matrix(dtm.new))
a$Tweet.text = rownames(a)
b = subset(a, select = c("Tweet.text"))
b$Topics = ldaOut.topics
tweetsnew = merge(tweets, b, by="Tweet.text")
tweetsnew = unique(tweetsnew)
tweetsnew$X.1 = NULL
tweetsnew$X = NULL

write.csv(tweetsnew, file = "E:/Data Science/Safecity/Twitter/Tweets PreProcessed/TweetsWithTopics13.csv")

#top 15 terms in each topic
ldaOut.terms <- as.matrix(terms(ldaOut,15))
write.csv(ldaOut.terms,file=paste("E:/Data Science/Safecity/Twitter/Tweets PreProcessed/LDAGibbs",k,"TopicsToTerms.csv"))

#probabilities associated with each topic assignment
topicProbabilities = as.data.frame(ldaOut@gamma)
write.csv(topicProbabilities,file=paste("E:/Data Science/Safecity/Twitter/Tweets PreProcessed/LDAGibbs",k,"TopicProbabilities.csv"))
