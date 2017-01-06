library(rmgarch)
library(parallel)
library(quantmod)
library(xts)
library(ccgarch)

rm(list=ls())
setwd("/home/rahul/Documents/gits/cn_stock_analysis/data_normalization")

setwd("/home/rahul/Documents/gits/cn_stock_analysis/djia_and_nasdaq/data")
djia <- read.csv("djia_return.csv")
nasdaq <- read.csv("nasdaq_return.csv")
data <- cbind(djia, nasdaq[,2])
names(data) <- c("date", "djia", "nasdaq")
data <- xts(data[,-1], as.Date(data[,1]))


all_data <- read.csv("close_all.txt")
all_data <- xts(all_data[,-1], as.Date.factor(all_data[,1]))

data <- all_data

# using ccgarch
dcc.results = dcc.estimation(c(0.5, 0.5), diag(c(0.2, 0.4)), diag(c(0.8, 0.8)), c(0.02, 0.97), data, "diagonal")
plot(seq(1,nrow(data)), dcc.results$DCC[,2], "l")
dcc.results$out

# using rmgarch
xspec = ugarchspec(mean.model = list(armaOrder = c(0, 0)), variance.model = list(garchOrder = c(1,1), model = 'sGARCH'), distribution.model = 'norm')
uspec = multispec(replicate(ncol(data), xspec))
spec1 = dccspec(uspec = uspec, dccOrder = c(1, 1), distribution = 'mvnorm')
# fit1 = dccfit(spec1, data = dvar, fit.control = list(eval.se = TRUE))
cl = makePSOCKcluster(2)
multf = multifit(uspec, data, cluster = cl)
fit1 = dccfit(spec1, data = data, fit.control = list(eval.se = TRUE), fit = multf, cluster = cl)
stopCluster(cl)
plot(fit1, which=4)
