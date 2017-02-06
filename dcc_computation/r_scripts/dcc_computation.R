setwd('/home/rahul/tmp/data/aligned_data')

library(rmgarch)
library(parallel)
library(xts)
library(foreach)
library(doParallel)

dcc_rmgarch <- function(data) {
  xspec = ugarchspec(mean.model = list(armaOrder = c(1, 1)), variance.model = list(garchOrder = c(1,1), model = 'sGARCH'), distribution.model = 'norm')
  uspec = multispec(replicate(ncol(data), xspec))
  spec1 = dccspec(uspec = uspec, dccOrder = c(1, 1), distribution = 'mvnorm')
  
  fit1 = dccfit(spec1, data, fit.control = list(eval.se = TRUE))
  
  return(fit1)
}

dcc_rmgarch_parallel <- function(data) {
  # using rmgarch
  xspec = ugarchspec(mean.model = list(armaOrder = c(1, 1)), variance.model = list(garchOrder = c(1,1), model = 'sGARCH'), distribution.model = 'norm')
  uspec = multispec(replicate(ncol(data), xspec))
  spec1 = dccspec(uspec = uspec, dccOrder = c(1, 1), distribution = 'mvnorm')
  # fit1 = dccfit(spec1, data = dvar, fit.control = list(eval.se = TRUE))
  cl = makeCluster(2)
  multf = multifit(uspec, data, cluster = cl)
  fit1 = dccfit(spec1, data = data, fit.control = list(eval.se = TRUE), fit = multf, cluster = cl)
  stopCluster(cl)
  
  # plot(fit1, which=4)
  
  return(fit1)
}

dcc_compute <- function(file1, file2) {
  # begin <- proc.time()
  
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
  output <- paste('../correlations/cor', substr(file1, 1, 6), substr(file2, 1, 6), sep = '_')
  write.table(cor_matrix[,2], file = output, row.names = F, col.names = F, quote = F)
  
  # end <- proc.time()
  
  # print(end - begin)
  
  return(fit)
}

dcc_compute2 <- function(series1, file1, file2) {
  
  data2 <- read.csv(file2)
  data2 <- xts(data2[,-1], as.Date.factor(data2[,1]))
  close2 <- data2[, 'close']
  series2 <- diff(log(close2))
  
  data = cbind(series1, series2)[-1,]
  fit <- dcc_rmgarch(data)
  
  cor_matrix = matrix(rcor(fit), ncol=ncol(data) * ncol(data), byrow=T)
  output <- paste('../correlations/cor', substr(file1, 1, 6), substr(file2, 1, 6), sep = '_')
  write.table(cor_matrix[,2], file = output, row.names = F, col.names = F, quote = F)
  
  return(fit)
}

compute_job <- function(i, size) {
  for (j in (i+1):size) {
    print(paste(i, j))
    dcc_compute(files[i], files[j])
  }
}

main <- function() {
  files <- dir()
  files_size <- length(files)
  
  cl <- makeCluster(detectCores(), outfile = "../log.txt")
  clusterEvalQ(cl, library(xts))
  clusterEvalQ(cl, library(rmgarch))
  registerDoParallel(cl)
  
  # foreach(i = 1:(files_size - 1), .export = c("compute_job", "dcc_compute", "dcc_rmgarch", "files")) %dopar%
  # compute_job(i, files_size)
  foreach(i = 1:65, .export = c("compute_job", "dcc_compute", "dcc_rmgarch", "files")) %dopar%
    compute_job(i, files_size)
  
  stopCluster(cl)
}

main2 <- function() {
  files <- dir()
  files_size <- length(files)
  
  cl <- makeCluster(detectCores(), outfile = "../log2.txt")
  clusterEvalQ(cl, library(xts))
  clusterEvalQ(cl, library(rmgarch))
  registerDoParallel(cl)
  
  for (i in 1:2) {

    print(paste0("processing i=", i, " stock number: ", files[i]))

    data1 <- read.csv(files[i])
    data1 <- xts(data1[,-1], as.Date.factor(data1[,1]))
    close1 <- data1[, 'close']
    series1 <- diff(log(close1))
    
    foreach(j = (i + 1):files_size, .export = c("dcc_compute2", "dcc_rmgarch")) %dopar% {
      tryCatch({
        dcc_compute2(series1, files[i], files[j])
      }, error = function(e) { 
        print(paste0("index: i=", i, " j=", j, " error: ", e))
      })
    }
  }
  
  stopCluster(cl)
}

system.time(main2())