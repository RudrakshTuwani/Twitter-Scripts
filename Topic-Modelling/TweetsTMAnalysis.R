# Read tweets into a df.

tweets <- read.csv("E:/Data Science/Safecity/Twitter/Tweets PreProcessed/TweetsWithTopics.csv", 
                   comment.char="#", stringsAsFactors=FALSE)

words <- read.csv("E:/Data Science/Safecity/Twitter/Tweets PreProcessed/LDAGibbs 9 TopicsToTerms.csv", 
                  stringsAsFactors=FALSE)

# Find topics which had the most engagement.
tapply(tweets$engagements, tweets$Topics, mean)
tapply(tweets$engagements, tweets$Topics, summary)

# Topic 4, 8 and 9 have the highest mean engagement
words$Topic.4 ## Sexual harassment 
words$Topic.8 ## Twitter Chat invitations 
words$Topic.9 ## Enivironmental issues

# Topic 1 has the least impressions.
words$Topic.1 ## rapes

# For impressions:
tapply(tweets$impressions, tweets$Topics, summary)

# Topic 1,2,5 and 6 have the lowest impressions
words$Topic.2 ## Tweetchat plans, thank you notes. (the least)
words$Topic.5 ## transport and sustainable development but with unique hashtags
words$Topic.6
