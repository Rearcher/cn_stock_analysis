library(rmgarch)
library(parallel)
library(xts)

setwd("/home/rahul/Documents/gits/cn_stock_analysis/djia_and_nasdaq/data")

djia <- read.csv("djia_return.csv")
nasdaq <- read.csv("nasdaq_return.csv")
data <- cbind(djia, nasdaq[,2])

names(data) <- c("date", "djia", "nasdaq")
dvar <- xts(data[,-1], as.Date(data[,1]))

xspec = ugarchspec(mean.model = list(armaOrder = c(1, 1)), variance.model = list(garchOrder = c(1,1), model = 'sGARCH'), distribution.model = 'norm')
uspec = multispec(replicate(ncol(dvar), xspec))
spec1 = dccspec(uspec = uspec, dccOrder = c(1, 1), distribution = 'mvnorm')

# fit1 = dccfit(spec1, data = dvar, fit.control = list(eval.se = TRUE))

cl = makePSOCKcluster(2)
multf = multifit(uspec, dvar, cluster = cl)

fit1 = dccfit(spec1, data = dvar, fit.control = list(eval.se = TRUE), fit = multf, cluster = cl)

stopCluster(cl)

# write.csv(matrix(rcor(fit1), ncol=ncol(dvar) * ncol(dvar), byrow=T), file = "correlation.csv", row.names = F, quote = F)