library(rmgarch)
library(parallel)
library(quantmod)

setwd("/home/rahul/PycharmProjects/data_normalization")

dvar <- read.csv("output_new.csv")
dvar <- dvar[, 1:101]
dvar <- data.frame(dvar)
dvar <- xts(dvar[,-1], as.Date(dvar[,1]))

xspec = ugarchspec(mean.model = list(armaOrder = c(0, 0)), variance.model = list(garchOrder = c(1,1), model = 'sGARCH'), distribution.model = 'norm')
uspec = multispec(replicate(ncol(dvar), xspec))
spec1 = dccspec(uspec = uspec, dccOrder = c(1, 1), distribution = 'mvnorm')

# fit1 = dccfit(spec1, data = dvar, fit.control = list(eval.se = TRUE))

cl = makePSOCKcluster(2)
multf = multifit(uspec, dvar, cluster = cl)

fit1 = dccfit(spec1, data = dvar, fit.control = list(eval.se = TRUE), fit = multf, cluster = cl)

stopCluster(cl)

write.csv(matrix(rcor(fit1), ncol=ncol(dvar) * ncol(dvar), byrow=T), file = "correlation.csv", row.names = F, quote = F)
