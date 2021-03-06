setwd('/Users/rahul/tmp/data/aligned_data')
library(xts)

plot_sample <- function(sample_file_name) {
  data = read.csv(paste(sample_file_name, ".txt", sep = ""))
  data <- xts(data[,-1], as.Date(data[,1]))
  plot(data[, c(4,5)], multi.panel = TRUE, yaxis.same = FALSE, main = sample_file_name, observation.based = TRUE)
}

plot_all <- function(dir_name) {
  files <- dir()
  for (file in files[1:10]) {
    data <- read.csv(file)
    data <- xts(data[, -1], as.Date.factor(data[, 1]))
    plot(data[,5])
  }
}

plot_one <- function(filename) {
  data <- read.csv(filename)
  data <- xts(data[, -1], as.Date.factor(data[, 1]))
  plot(data[, 'trading_volume'], main = filename)
}

plot_sample('601988')
plot_sample('601318')
plot_sample('601398')
plot_sample('601766')
plot_sample('601668')
plot_sample('601390')
plot_sample('600325')
plot_sample('600868')
plot_sample('300059')
plot_sample('002594')
plot_sample('300033')
plot_sample('300104')
plot_sample('300024')
plot_sample('300120')

plot_sample('000046')
plot_sample('000898')
plot_sample('000539')
plot_sample('000793')
plot_sample('002292')
plot_sample('000156')
