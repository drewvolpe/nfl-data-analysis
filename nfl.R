
library(randomForest)
library(tree)

# load cleaned data of history game results
data_nfl <- read.csv('nfl_cleaned.csv', header=TRUE, sep=",")

# lm_diff <- lm(data_nfl$Diff ~ data_nfl$Line)
# plot(data_nfl$Line, data_nfl$Diff)
# abline(lm_diff, col="blue")

# Prediction model
set.seed(23)
num_rows = nrow(data_nfl)
trainSamples <- sample(1:num_rows, size=num_rows-2000, replace=F)
data_nfl_train <- data_nfl[trainSamples, ]
data_nfl_test <- data_nfl[-trainSamples, ]

forestNFL = randomForest(Winner ~ Diff, data=data_nfl_train)
p = predict(forestNFL, newdata=data_nfl_test)
table(p, data_nfl_test$Winner)

glm_nfl <- glm(Winner ~ Line + Home.Team, data=data_nfl_train, family="binomial")
p = predict(glm_nfl, new_data=data_nfl_test)
table(data_nfl_test$Winner, p)

# Compare Line to Win%
d_winpct <- read.csv('win_pct_Winner.csv', header=TRUE, sep=',')
plot(d_winpct$line, d_winpct$pct)
lm_pct <- lm(pct ~ line, data=d_winpct)
abline(lm_pct, col="blue")
