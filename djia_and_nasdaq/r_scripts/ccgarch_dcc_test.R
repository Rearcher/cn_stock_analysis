library(data.table)
library(ccgarch)

rm(list=ls())

setwd("/home/rahul/Documents/gits/cn_stock_analysis/djia_and_nasdaq/data")

nasdaq_data = read.csv("nasdaq_return.csv")
djia_data = read.csv("djia_return.csv")
time_col = nasdaq_data[,1]
nasdaq_col = nasdaq_data[,2]
djia_col = djia_data[,2]

plot(as.Date.factor(time_col), nasdaq_col, "l")
plot(as.Date.factor(time_col), djia_col, "l")

data = cbind(nasdaq_col, djia_col)

dcc.results = dcc.estimation(c(0.5, 0.5), diag(c(0.2, 0.4)), diag(c(0.8, 0.8)), c(0.02, 0.97), data, "diagonal")
plot(as.Date.factor(time_col), dcc.results$DCC[,2], "l")
plot(as.Date.factor(time_col), dcc.results$DCC[,2], type="l", xlim=c(as.POSIXct('1999-04-01', format="%Y-%m-%d"),as.POSIXct('2000-03-31', format="%Y-%m-%d")))

plot(as.Date.factor(time_col)[2370:2632], dcc.results$DCC[,2][2370:2632], "l")

