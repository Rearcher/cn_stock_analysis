library("ccgarch", lib.loc="~/R/x86_64-pc-linux-gnu-library/3.3")

nobs <- 1000
a <- c(0.01, 0.5)
A <- diag(c(0.05, 0.2))
B <- diag(c(0.94, 0.5))
uncR <- matrix(c(1.0, 0.5, 0.5, 1.0), 2, 2)
dcc.para <- c(0.03, 0.96)

dcc.data <- dcc.sim(nobs, a, A, B, uncR, dcc.para, model="diagonal")
dcc.result <- dcc.estimation(inia=a, iniA=A, iniB=B, ini.dcc=dcc.para, 
                             dvar=dcc.data$eps, model="diagonal")

plot(x=seq(1,1000), dcc.result$DCC[,2], "l", col="red", ylim=c(0.1, 0.9))
t = seq(1, 1000)
rho = 0.5 + 0.4*cos(2 * pi * t / 200)
lines(t, rho, "l")

ans = dcc.result$DCC[, 2]
ans = abs(ans - rho)
sum(ans) / 1000
