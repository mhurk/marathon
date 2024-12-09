library(fitdistrplus)
library(lubridate)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

results <- readxl::read_excel("Results-marathon-eindhoven-2017.xlsx")

ChipTime <- parse_date_time(results$Chiptime, orders = "%Y-%m-%d %H:%M:%S")
ChipMinute <- hour(ChipTime)*60 + minute(ChipTime) + second(ChipTime)/60

descdist(ChipMinute, discrete = FALSE)

hist(ChipMinute, breaks=100)

# Comparison of various fits 
fitW <- fitdist(ChipMinute, "weibull")
fitg <- fitdist(ChipMinute, "gamma")
fitln <- fitdist(ChipMinute, "lnorm")
fitnorm <- fitdist(ChipMinute, "norm")
summary(fitW)
summary(fitg)
summary(fitln)
summary(fitnorm)
cdfcomp(list(fitW, fitg, fitln, fitnorm), legendtext=c("Weibull", "gamma", "lognormal", "normal"))
denscomp(list(fitW, fitg, fitln, fitnorm), legendtext=c("Weibull", "gamma", "lognormal", "normal"))
qqcomp(list(fitW, fitg, fitln, fitnorm), legendtext=c("Weibull", "gamma", "lognormal", "normal"))
ppcomp(list(fitW, fitg, fitln, fitnorm), legendtext=c("Weibull", "gamma", "lognormal", "normal"))
gofstat(list(fitW, fitg, fitln, fitnorm), fitnames=c("Weibull", "gamma", "lognormal", "normal"))

# The gamma distribution has the lowest values across all goodness-of-fit statistics (KS, CvM, AD) 
# and criteria (AIC, BIC), suggesting it is the best fit for your data compared to the Weibull and lognormal distributions.

meanTime <- mean(ChipMinute)
sdTime <- sd(ChipMinute)

paste("mean time:", sprintf("%.02d:%.02d:%.02d", meanTime %/% 60, round(meanTime %% 60), round(meanTime%%1*60)), sep = " ")
paste("standard deviation:", sprintf("%.02d:%.02d:%.02d", sdTime %/% 60, round(sdTime %% 60), round(sdTime%%1*60)), sep = " ")


meanPace <- meanTime/42.195 #input for simulation
sdPace <- sdTime/42.195 #input for simulation
paste("mean pace :", sprintf("%.02d:%.02d", round(meanPace %% 60), round(meanPace%%1*60)), sep = " ")
paste("standard deviation:", sprintf("%.02d:%.02d", round(sdPace %% 60), round(sdPace%%1*60)), sep = " ")
