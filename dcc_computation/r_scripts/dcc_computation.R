setwd('/home/rahul/Documents/gits/cn_stock_analysis/data/aligned_data')

library(rmgarch)
library(parallel)
library(xts)

dcc_rmgarch <- function(data) {
  # using rmgarch
  xspec = ugarchspec(mean.model = list(armaOrder = c(1, 1)), variance.model = list(garchOrder = c(1,1), model = 'sGARCH'), distribution.model = 'norm')
  uspec = multispec(replicate(ncol(data), xspec))
  spec1 = dccspec(uspec = uspec, dccOrder = c(1, 1), distribution = 'mvnorm')
  #fit1 = dccfit(spec1, data, fit.control = list(eval.se = TRUE))
  cl = makePSOCKcluster(2)
  multf = multifit(uspec, data, cluster = cl)
  fit1 = dccfit(spec1, data = data, fit.control = list(eval.se = TRUE), fit = multf, cluster = cl)
  stopCluster(cl)
  #plot(fit1, which=4)
  return(fit1)
}

dcc_compute <- function(file1, file2) {
  begin <- proc.time()
  
  data1 <- read.csv(file1)
  data1 <- xts(data1[,-1], as.Date.factor(data1[,1]))
  close1 <- data1[, 'close']
  series1 <- diff(log(close1))
  
  data2 <- read.csv(file2)
  data2 <- xts(data2[,-1], as.Date.factor(data2[,1]))
  close2 <- data2[, 'close']
  series2 <- diff(log(close2))
  
  data = cbind(series1, series2)[-1,]
  fit <- dcc_rmgarch(data)
  
  cor_matrix = matrix(rcor(fit), ncol=ncol(data) * ncol(data), byrow=T)
  output <- paste('cor', substr(file1, 1, 6), substr(file2, 1, 6), sep = '_')
  write.table(cor_matrix[,2], file = output, row.names = F, col.names = F, quote = F)
  
  end <- proc.time()
  
  print(end - begin)
  
  return(fit)
}

compute_job <- function(begin, limit) {
  for (i in begin:(limit-1)) {
    for (j in (i+1):limit) {
      print(paste(i, j))
      #dcc_compute(files[i], files[j])
    }
  }
}

files <- dir()
files_size <- length(files)
limit <- 10
compute_job(1, limit)
