library(rmgarch)
library(parallel)
library(xts)
library(ccgarch)

rm(list=ls())

# djia and nasdaq compare
setwd("/home/rahul/Documents/gits/cn_stock_analysis/djia_and_nasdaq/data")
djia <- read.csv("djia_return.csv")
nasdaq <- read.csv("nasdaq_return.csv")
data <- cbind(djia, nasdaq[,2])
names(data) <- c("date", "djia", "nasdaq")
data <- xts(data[,-1], as.Date(data[,1]))

fit1 <- dcc_rmgarch(data)
plot(fit1, which=4)
fit2 <- dcc_ccgarch(data)
plot(seq(1,nrow(data)), fit2$DCC[,2], "l")



# A-share stock compre
setwd("/home/rahul/Documents/gits/cn_stock_analysis/data")
all_data <- read.csv("close_all.txt")
all_data <- xts(all_data[,-1], as.Date.factor(all_data[,1]))
return_data <- diff(all_data)[-1,]

data <- return_data[, seq(1, 50)]

fit1 <- dcc_rmgarch(data, threads = 4)
# plot(fit1, which=4)
fit2 <- dcc_ccgarch(data)
# plot(seq(1,nrow(data)), fit2$DCC[,2], "l")
cor1 <- matrix(rcor(fit1), ncol=ncol(data) * ncol(data), byrow=T)
cor2 <- fit2$DCC
plot(seq(1, nrow(data)), cor1[,2], 'l')
plot(seq(1, nrow(data)), cor2[,2], 'l')


dcc_rmgarch <- function(data, threads=2) {
  # using rmgarch
  xspec = ugarchspec(mean.model = list(armaOrder = c(0, 0)), variance.model = list(garchOrder = c(1,1), model = 'sGARCH'), distribution.model = 'norm')
  uspec = multispec(replicate(ncol(data), xspec))
  spec1 = dccspec(uspec = uspec, dccOrder = c(1, 1), distribution = 'mvnorm')
  # fit1 = dccfit(spec1, data = dvar, fit.control = list(eval.se = TRUE))
  cl = makePSOCKcluster(threads)
  multf = multifit(uspec, data, cluster = cl)
  fit1 = dccfit(spec1, data = data, fit.control = list(eval.se = TRUE), fit = multf, cluster = cl)
  stopCluster(cl)
  
  # plot(fit1, which=4)
  
  return(fit1)
}

dcc_ccgarch <- function(data) {
  # using ccgarch
  n <- ncol(data)
  inia <- rep(0.1, n)
  iniA <- diag(rep(0.1, n))
  iniB <- diag(rep(0.1, n))
  inidcc <- c(0.1, 0.1)
  
  dcc.results = dcc.estimation(inia, iniA, iniB, inidcc, data, "diagonal")
  # plot(seq(1,nrow(data)), dcc.results$DCC[,2], "l")
  return(dcc.results)
}
