
# Playoff lines, historically by week

library(Hmisc)  # for cut2
library(ggplot2)
library(reshape2) # for melt
library(plyr)  # for ddply
data_nfl <- read.csv('./playoffs_nfl_cleaned.csv', header=TRUE, sep=",")

# bar plot of winner by line
data_nfl$id <- 1:nrow(data_nfl) # create id variable
data_nfl.melted <- melt(data_nfl, id='id')
ggplot(data_nfl.melted, aes(x=data_nfl$Line, fill=data_nfl$Winner)) + 
    geom_bar(binwidth=0.5)


# Winner Home/Visitor -> 1/0
data_nfl$Winnern <- sapply(data_nfl$Winner, function(x) if (x == 'Home') {1 } else {0})

# bar by Line Bins
data_nfl$LineBin <- cut2(data_nfl$Line, g=10)
ggplot(data_nfl.melted, aes(x=data_nfl$LineBin, fill=data_nfl$Winner)) + 
    geom_bar(binwidth=0.5)


# How often lines occur by week

data_nfl$Line = abs(data_nfl$Line)  # make all Lines positive
data_nfl_wc <- data_nfl[data_nfl$Round=='WC',]
data_nfl_dp <- data_nfl[data_nfl$Round=='DP',]
data_nfl_cc <- data_nfl[data_nfl$Round=='CC',]
data_nfl_sb <- data_nfl[data_nfl$Round=='SB',]

binw = 0.5
ggplot(data_nfl, aes(x=Line)) + geom_histogram(binwidth=binw, color='black', fill='#eeaaaa') + ggtitle("All Playoffs")
ggplot(data_nfl_wc, aes(x=Line)) + geom_histogram(binwidth=binw, color='black', fill='#eeaaaa') + ggtitle("Wildcard")
ggplot(data_nfl_dp, aes(x=Line)) + geom_histogram(binwidth=binw, color='black', fill='#eeaaaa') + ggtitle("Div Playoffs")
ggplot(data_nfl_cc, aes(x=Line)) + geom_histogram(binwidth=binw, color='black', fill='#eeaaaa') + ggtitle("Conf Champ")
ggplot(data_nfl_sb, aes(x=Line)) + geom_histogram(binwidth=binw, color='black', fill='#eeaaaa') + ggtitle("Superbowl")


# density plots
ggplot(data_nfl, aes(x=Line, colour=Round)) + geom_density() +
xlab("Line Size") +
ylab("Number of occurences") +
ggtitle("Playoff Lines by Round")


# facets
ggplot(data_nfl, aes(x=Line)) + geom_histogram(binwidth=.5, colour="black", fill="white") + 
    facet_grid(Round ~ .)


