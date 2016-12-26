library("ccgarch", lib.loc="~/R/x86_64-pc-linux-gnu-library/3.3")

nobs <- 1000
a <- c(0.01, 0.5)
A <- diag(c(0.05, 0.2))
B <- diag(c(0.94, 0.5))
uncR <- matrix(c(1.0, 0.9, 0.9, 1.0), 2, 2)
dcc.para <- c(0.22, 0.75)

dcc.data <- dcc.sim(nobs, a, A, B, uncR, dcc.para, model="diagonal")

dcc.result <- dcc.estimation(inia=a, iniA=A, iniB=B, ini.dcc=dcc.para, 
                              dvar=dcc.data$eps, model="diagonal")
dcc.result$out


# sine
t = seq(1, 1000)
# rho = 0.5 + 0.4*cos(2 * pi * t / 200)

ans = dcc.result$DCC[, 2]
# ans = abs(ans - rho)
ans = abs(ans - 0.9)
sum(ans) / 1000

plot(seq(1, 1000), dcc.data$eps[,1], "l")
plot(seq(1, 1000), dcc.data$eps[,2], "l")
