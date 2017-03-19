setwd('/Users/Katherine/Desktop/data/aligned_data')

library(rmgarch)
library(rugarch)
library(xts)
library(foreach)


sig_compute <- function(file) {
  data <- read.csv(file)
  data <- xts(data[,-1], as.Date.factor(data[,1]))
  close <- data[, 'close']
  series <- diff(log(close))
  xspec = ugarchspec(mean.model = list(armaOrder = c(1, 1)), variance.model = list(garchOrder = c(1,1), model = 'sGARCH'), distribution.model = 'norm')
  fit = ugarchfit(spec=xspec,data=series[-1,],out.sample=0,solver="solnp")
  sig <- sigma(fit)
#  plot(sig)
  sig_matrix = matrix(sig, byrow=T)
  output <- paste('../cor/sig/sig', substr(file, 1, 6), sep = '_')
  write.table(sig_matrix, file = output, row.names = F, col.names = F, quote = F)
  
#  output2 <- paste('../cor/sig/sigPlot', substr(file, 1, 6), sep = '_')
#  savePlot(filename = output2, type=c("png"),device=dev.cur())
  return(sig)
}

main <- function() {
  files <- dir()
  files_size <- length(files)
  for (i in 1:files_size) {
    sig_compute(files[i])
  }
}


