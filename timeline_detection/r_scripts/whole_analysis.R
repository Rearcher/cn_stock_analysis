setwd('/home/rahul/Documents/Gits/cn_stock_analysis/data')
library(xts)

shanghai <- read.csv('000001.txt')
shenzhen <- read.csv('399106.txt')
hushen300 <- read.csv('000300.txt')

shanghai <- shanghai[, c(1, 2)]
shenzhen <- shenzhen[, 2]
hushen300 <- hushen300[, 2]

data <- cbind(shanghai, shenzhen, hushen300)
data <- xts(data[, -1], as.Date(data[,1]))

names(data) <- c("shang_zheng", "shen_zhen", "hu_shen_300")
plot(data[, 1:3], main = 'whole analysis', observation.based = TRUE, legend.loc = 'topleft')
