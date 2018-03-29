####R code to fit titrating delay discounting task using Mazur (1987), Myerson and Green (1999) and Rachlin (2001) hyperbolic and hyperboloid models####


#Mazur: V = A/(1+kD)

#Myerson & Green: V = A/((1+kD)^s)

#Rachlin: V = A/(1+kD^s)

###Non-linear Least Squares is the fit method####

#Call in data-set
discounting <- read.table("/Users/williamdehart/Google Drive/JOVE/Data.txt", header=TRUE, sep="\t", na.strings="NA", dec=".", strip.white=TRUE)
#This data-set contains six indifference points from a money delay discounting task and can be separated by group (non-smoker = 0, smoker = 1). 


#Call in necessary libraries
library(psych) #For descriptive statistics

library(nlmrt) #Non-linear regression, especially good for models with residuals that are close to 0. Normal nls command may not work when residuals are close to 0.

library (plyr) #Includes function to run loop for individual fits



####Group analysis####

#Create time variable for 1 week, 2 weeks, 1 month, 6 months, 5 years & 25 years. Units will be in months
time <- c(.25, .5, 1, 6, 60, 300) #Creates time variable


#Create "V" values for each commodity
describeBy(discounting) #Obtain median values for indifference points.

money_indiff <- c(0.95, 0.90, 0.84, 0.69, 0.25, 0.06)


money_df <- data.frame(time, money_indiff) # Creates data frame for analysis


###Mazur group model fit###
Mazur_mod <- money_indiff ~ 1/(1+(k*time))
Mazur_fit <- wrapnls(Mazur_mod, start=list(k=0), data = money_df)

print(Mazur_fit)

#Calculate r-squared value
RSS <- sum(residuals(Mazur_fit)^2) #Residual sum of squares

TSS <- sum((money_indiff - mean(money_indiff))^2) #Total sum of squares

1 - (RSS/TSS) #R-squared

#AIC for model fit
AIC(Mazur_fit, k = 2)


#Plot of model fit
predict(Mazur_fit) #Gives model predicted values

plot(money_df) #Plots indifference points
time_range <- seq(0, 300, length = 1000) #Sets time range for best fit line.
lines(time_range, predict(Mazur_fit, data.frame(time = time_range))) #Adds best fit line




###Rachlin###

Rach_mod <- money_indiff ~ 1/(1+k*(time^s)) #Model
start_values <- c(k = 0, s = 1) #Parameter start values

Rach_fit <- wrapnls(Rach_mod, start = start_values, data = money_df, upper = c(s=1), lower = c(k=0, s=0)) #wrapnls is 

print(Rach_fit)


#AIC
AIC(Rach_fit, k=2)



#Calculate r-squared values
RSS <- sum(residuals(Rach_fit)^2) #Residual sum of squares

TSS <- sum((money_indiff - mean(money_indiff))^2) #Total sum of squares

1 - (RSS/TSS) #R-squared

#Plot of model fit
predict(Rach_fit) #Gives model predicted values

plot(money_df) #Plots indifference points
time_range <- seq(0, 300, length = 1000) #Sets time range for best fit line.
lines(time_range, predict(Rach_fit, data.frame(time = time_range))) #Adds best fit line




###Myerson & Green###

MG_mod <- money_indiff ~ 1/(1+k*time)^s #Model
start_values <- c(k = 0, s = 1) #Parameter start values

MG_fit <- wrapnls(Rach_mod, start = start_values, data = money_df, lower = c(k=0, s=0)) #wrapnls is 

print(MG_fit)


#AIC
AIC(MG_fit, k=2)



#Calculate r-squared values
RSS <- sum(residuals(MG_fit)^2) #Residual sum of squares

TSS <- sum((money_indiff - mean(money_indiff))^2) #Total sum of squares

1 - (RSS/TSS) #R-squared

#Plot of model fit
predict(MG_fit) #Gives model predicted values

plot(money_df) #Plots indifference points
time_range <- seq(0, 300, length = 1000) #Sets time range for best fit line.
lines(time_range, predict(MG_fit, data.frame(time = time_range))) #Adds best fit line



###Compare model fits###
anova(Mazur_fit, Rach_fit)

anova(Mazur_fit, MG_fit)


###Graph all three models on one graph###
plot(money_df) #Plots indifference points
time_range <- seq(0, 300, length = 50) #Sets time range for best fit line.
lines(time_range, predict(Mazur_fit, data.frame(time = time_range)), col = "Green") #Adds Mazur best fit line
lines(time_range, predict(Rach_fit, data.frame(time = time_range)), col = "Red") #Adds Rachlin best fit line
lines(time_range, predict(MG_fit, data.frame(time = time_range)), col = "Black") #Adds Mazur best fit line










####Non-linear fit using nls (non-linear least squares) command for Individual data####


###Mazur###

#Create long-formated data-set
discounting_long <- reshape(discounting, idvar = "Participant", varying = c("Money_1", "Money_2", "Money_3", "Money_4", "Money_5", "Money_6"),timevar = "time",   direction = "long", v.names = ( "indiff"))

#Order Data
osub <- order(as.integer(discounting_long$Participant))
discounting_long <- discounting_long[osub, ]

#Convert time variable to units of months
discounting_long$time <- c("1" = ".25", "2" = ".5", "3" = "1", "4" = "6", "5" = "60", "6" = "300")

discounting_long$time <- as.numeric (discounting_long$time)

#Model Fit
demo_maz <- dlply(discounting_long, .(Participant), function(discounting_long) {nlxb(indiff ~ 1/(1+(k*time)), data = discounting_long, start = c(k=0))})

print(demo_maz)

#Obtain parameter values
coef_Maz <- llply(demo_maz, function(discounting_long) coef(discounting_long))




#Create new dataset with model parameters
discounting_vars <- c("Participant", "Smoker", "Money_1", "Money_2", "Money_3", "Money_4", "Money_5", "Money_6")

osub <- order(as.integer(discounting$Participant))
discounting <- discounting[osub,]

discounting_clean <- discounting[discounting_vars]

discounting_clean$k <- coef_Maz

discounting_long_Maz <- reshape(discounting_clean, idvar = "Participant", varying = c("Money_1", "Money_2", "Money_3", "Money_4", "Money_5", "Money_6"),timevar = "time",   direction = "long", v.names = ( "indiff"))


#Order Data
osub <- order(as.integer(discounting_long_Maz$Participant))
discounting_long <- discounting_long_Maz[osub, ]

discounting_long_Maz$time <- c("1" = ".25", "2" = ".5", "3" = "1", "4" = "6", "5" = "60", "6" = "300")

discounting_long_Maz$time <- as.numeric (discounting_long_Maz$time)

discounting_long_Maz$k <- as.numeric (discounting_long_Maz$k)


#Create variables needed for r-squared and AIC calulcations
discounting_long_Maz$predict <- 1/(1+discounting_long_Maz$time*discounting_long_Maz$k)

discounting_long_Maz$resid <- discounting_long_Maz$indiff - discounting_long_Maz$predict

#Create final wide data-set
discounting_wide_Maz <- reshape(discounting_long_Maz, idvar = c("Participant", "Smoker"), timevar = "time", direction = "wide") #Change data-set into wide formate

#R-squared calculation
#Mean Indifference Point
discounting_wide_Maz$mean_indiff <- (discounting_wide_Maz$indiff.0.25 + discounting_wide_Maz$indiff.0.5 + discounting_wide_Maz$indiff.1 + discounting_wide_Maz$indiff.6 + discounting_wide_Maz$indiff.60 + discounting_wide_Maz$indiff.300)/6


#Residual sum of squares
#Total sum of squares
discounting_wide_Maz$TSS <-((discounting_wide_Maz$indiff.0.25 - discounting_wide_Maz$mean_indiff)^2 + (discounting_wide_Maz$indiff.0.5 - discounting_wide_Maz$mean_indiff)^2 + (discounting_wide_Maz$indiff.1 - discounting_wide_Maz$mean_indiff)^2 + (discounting_wide_Maz$indiff.6 - discounting_wide_Maz$mean_indiff)^2 + (discounting_wide_Maz$indiff.60 - discounting_wide_Maz$mean_indiff)^2 + (discounting_wide_Maz$indiff.300 - discounting_wide_Maz$mean_indiff)^2) 

#Residual sum of squares
discounting_wide_Maz$RSS <- (discounting_wide_Maz$resid.0.25^2 + discounting_wide_Maz$resid.0.5^2 + discounting_wide_Maz$resid.1^2 + discounting_wide_Maz$resid.6^2 + discounting_wide_Maz$resid.60^2 + discounting_wide_Maz$resid.300^2)

discounting_wide_Maz$r_squared <- (1 - (discounting_wide_Maz$RSS/discounting_wide_Maz$TSS))

median(discounting_wide_Maz$r_squared, na.rm = FALSE)
describeBy(discounting_wide_Maz$r_squared, group = discounting_wide_Maz$Smoker)


#AIC for model fit. For individual model fits, it must be calculated by hand. Use AICc because of the low n (six indifference points).

discounting_wide_Maz$AICc <- -2*log(discounting_wide_Maz$RSS) + 2*1 + (2*1*(1+1))/(6-1-1)

median(discounting_wide_Maz$AICc, na.rm = FALSE)
describeBy(discounting_wide_Maz$AICc, group = discounting_wide_Maz$Smoker)

#Calculate AUC
time_AUC <- c(.25/300, .5/300, 1/300, 6/300, 60/300, 300/300) #Use these values for the time values in AUC calculation


attach(discounting_wide_Maz)
discounting_wide_Maz$AUC <- (((0.00083333-0)*((1 + indiff.0.25)/2)) + ((0.00166667-0.00083333)*((indiff.0.25+indiff.0.5)/2)) + ((0.00333333-0.00166667)*((indiff.0.5 + indiff.1)/2)) + ((0.02000000-0.00333333)*((indiff.1 + indiff.6)/2)) + ((0.20000000-0.02000000)*((indiff.6 + indiff.60)/2)) + ((1-0.20000000)*((indiff.60 + indiff.300)/2)))















###Rachlin###


#Create long-formated data-set
discounting_long <- reshape(discounting, idvar = "Participant", varying = c("Money_1", "Money_2", "Money_3", "Money_4", "Money_5", "Money_6"),timevar = "time",   direction = "long", v.names = ( "indiff"))



#Order Data
osub <- order(as.integer(discounting_long$Participant))
discounting_long <- discounting_long[osub, ]


discounting_long$time <- c("1" = ".25", "2" = ".5", "3" = "1", "4" = "6", "5" = "60", "6" = "300")

discounting_long$time <- as.numeric (discounting_long$time)



#Model fit
demo_Rach <- dlply(discounting_long, .(Participant), function(discounting_long) {nlxb(indiff ~ 1/(1+(k*time^s)), data = discounting_long, start = c(k=0, s=1), lower = c(s=0), upper = c(s=1))})

print(demo_Rach)

coef_Rach <- ldply(demo_Rach, function(discounting_long) coef(discounting_long))


coef_Rach$k <- as.numeric(coef_Rach$k)
coef_Rach$s <- as.numeric(coef_Rach$s)


osub <- order(as.integer(discounting$Participant))
discounting <- discounting[osub,]


discounting_vars <- c("Participant", "Smoker", "Money_1", "Money_2", "Money_3", "Money_4", "Money_5", "Money_6")


discounting_clean <- discounting[discounting_vars]

discounting_clean$k <- coef_Rach$k

discounting_clean$s <- coef_Rach$s




discounting_long_Rach <- reshape(discounting_clean, idvar = "Participant", varying = c("Money_1", "Money_2", "Money_3", "Money_4", "Money_5", "Money_6"),timevar = "time",   direction = "long", v.names = ( "indiff"))



#Order Data
osub <- order(as.integer(discounting_long_Rach$Participant))
discounting_long_Rach <- discounting_long_Rach[osub, ]

discounting_long_Rach$time <- c("1" = ".25", "2" = ".5", "3" = "1", "4" = "6", "5" = "60", "6" = "300")

discounting_long_Rach$time <- as.numeric (discounting_long_Rach$time)



discounting_long_Rach$predict <- 1/(1+discounting_long_Rach$k*(discounting_long_Rach$time^discounting_long_Rach$s))

discounting_long_Rach$resid <- discounting_long_Rach$indiff - discounting_long_Rach$predict


discounting_wide_Rach <- reshape(discounting_long_Rach, idvar = c("Participant", "Smoker"), timevar = "time", direction = "wide") #Change data-set into wide formate


#Mean Indifference Point
discounting_wide_Rach$mean_indiff <- (discounting_wide_Rach$indiff.0.25 + discounting_wide_Rach$indiff.0.5 + discounting_wide_Rach$indiff.1 + discounting_wide_Rach$indiff.6 + discounting_wide_Rach$indiff.60 + discounting_wide_Rach$indiff.300)/6


#Residual sum of squares
#Total sum of squares
discounting_wide_Rach$TSS <-((discounting_wide_Rach$indiff.0.25 - discounting_wide_Rach$mean_indiff)^2 + (discounting_wide_Rach$indiff.0.5 - discounting_wide_Rach$mean_indiff)^2 + (discounting_wide_Rach$indiff.1 - discounting_wide_Rach$mean_indiff)^2 + (discounting_wide_Rach$indiff.6 - discounting_wide_Rach$mean_indiff)^2 + (discounting_wide_Rach$indiff.60 - discounting_wide_Rach$mean_indiff)^2 + (discounting_wide_Rach$indiff.300 - discounting_wide_Rach$mean_indiff)^2) 

#Residual sum of squares
discounting_wide_Rach$RSS <- (discounting_wide_Rach$resid.0.25^2 + discounting_wide_Rach$resid.0.5^2 + discounting_wide_Rach$resid.1^2 + discounting_wide_Rach$resid.6^2 + discounting_wide_Rach$resid.60^2 + discounting_wide_Rach$resid.300^2)

discounting_wide_Rach$r_squared <- (1 - (discounting_wide_Rach$RSS/discounting_wide_Rach$TSS))

median(discounting_wide_Rach$r_squared, na.rm = FALSE)
describeBy(discounting_wide_Rach$r_squared, group = discounting_wide_Rach$Smoker)


#AIC for model fit
discounting_wide_Rach$AICc <- -2*log(discounting_wide_Rach$RSS) + 2*2 + (2*2*(2+1))/(6-2-1) # n = number of observations or data points


median(discounting_wide_Rach$AICc, na.rm = FALSE)
describeBy(discounting_wide_Rach$AICc, group = discounting_wide_Rach$Smoker)

#AUC
time_AUC <- c(.25/300, .5/300, 1/300, 6/300, 60/300, 300/300) #Use these values for the time values in AUC calculation


attach(discounting_wide_Rach)
discounting_wide_Rach$AUC <- (((0.00083333-0)*((1 + indiff.0.25)/2)) + ((0.00166667-0.00083333)*((indiff.0.25+indiff.0.5)/2)) + ((0.00333333-0.00166667)*((indiff.0.5 + indiff.1)/2)) + ((0.02000000-0.00333333)*((indiff.1 + indiff.6)/2)) + ((0.20000000-0.02000000)*((indiff.6 + indiff.60)/2)) + ((1-0.20000000)*((indiff.60 + indiff.300)/2)))







###Myerson & Green###

discounting_long <- reshape(discounting, idvar = "Participant", varying = c("Money_1", "Money_2", "Money_3", "Money_4", "Money_5", "Money_6"),timevar = "time",   direction = "long", v.names = ( "indiff"))



#Order Data
osub <- order(as.integer(discounting_long$Participant))
discounting_long <- discounting_long[osub, ]



discounting_long$time <- c("1" = ".25", "2" = ".5", "3" = "1", "4" = "6", "5" = "60", "6" = "300")

discounting_long$time <- as.numeric (discounting_long$time)

#Model fit
demo_MG <- dlply(discounting_long, .(Participant), function(discounting_long) {nlxb(indiff ~ 1/((1+k*time)^s), data = discounting_long, start = c(k=0, s=1), lower = c(s=0))})


print(demo_MG)

coef_MG <- ldply(demo_MG, function(discounting_long) coef(discounting_long))

coef$Participant <- NULL

coef_MG$k <- as.numeric(coef_MG$k)
coef_MG$s <- as.numeric(coef_MG$s)


osub <- order(as.integer(discounting$Participant))
discounting <- discounting[osub,]


discounting_vars <- c("Participant", "Smoker", "Money_1", "Money_2", "Money_3", "Money_4", "Money_5", "Money_6")


discounting_clean <- discounting[discounting_vars]

discounting_clean$k <- coef_MG$k

discounting_clean$s <- coef_MG$s





discounting_long_MG <- reshape(discounting, idvar = "Participant", varying = c("Money_1", "Money_2", "Money_3", "Money_4", "Money_5", "Money_6"),timevar = "time",   direction = "long", v.names = ( "indiff"))





#Order Data
osub <- order(as.integer(discounting_long_MG$Participant))
discounting_long_MG <- discounting_long_MG[osub, ]

discounting_long_MG$time <- c("1" = ".25", "2" = ".5", "3" = "1", "4" = "6", "5" = "60", "6" = "300")

discounting_long_MG$time <- as.numeric (discounting_long_MG$time)



discounting_long_MG$predict <- 1/(1+discounting_long_MG$time*discounting_long_MG$k)^discounting_long_MG$s

discounting_long_MG$resid <- discounting_long_MG$indiff - discounting_long_MG$predict


discounting_wide_MG <- reshape(discounting_long_MG, idvar = c("Participant", "Smoker"), timevar = "time", direction = "wide") #Change data-set into wide formate


#Mean Indifference Point
discounting_wide_MG$mean_indiff <- (discounting_wide_MG$indiff.0.25 + discounting_wide_MG$indiff.0.5 + discounting_wide_MG$indiff.1 + discounting_wide_MG$indiff.6 + discounting_wide_MG$indiff.60 + discounting_wide_MG$indiff.300)/6


#Residual sum of squares
#Total sum of squares
discounting_wide_MG$TSS <-((discounting_wide_MG$indiff.0.25 - discounting_wide_MG$mean_indiff)^2 + (discounting_wide_MG$indiff.0.5 - discounting_wide_MG$mean_indiff)^2 + (discounting_wide_MG$indiff.1 - discounting_wide_MG$mean_indiff)^2 + (discounting_wide_MG$indiff.6 - discounting_wide_MG$mean_indiff)^2 + (discounting_wide_MG$indiff.60 - discounting_wide_MG$mean_indiff)^2 + (discounting_wide_MG$indiff.300 - discounting_wide_MG$mean_indiff)^2) 

#Residual sum of squares
discounting_wide_MG$RSS <- (discounting_wide_MG$resid.0.25^2 + discounting_wide_MG$resid.0.5^2 + discounting_wide_MG$resid.1^2 + discounting_wide_MG$resid.6^2 + discounting_wide_MG$resid.60^2 + discounting_wide_MG$resid.300^2)

discounting_wide_MG$r_squared <- (1 - (discounting_wide_MG$RSS/discounting_wide_MG$TSS))

median(discounting_wide_MG$r_squared, na.rm = FALSE)
describeBy(discounting_wide_MG$r_squared, group = discounting_wide_MG$Smoker)


#AIC for model fit
discounting_wide_MG$AIC <- -2*log(discounting_wide_MG$RSS) + 2*2 + (2*2*(2+1))/(6-2-1) # n = number of observations or data points

median(discounting_wide_MG$AIC, na.rm = FALSE)
describeBy(discounting_wide_MG$AIC, group = discounting_wide_MG$Smoker)


#AUC
time_AUC <- c(.25/300, .5/300, 1/300, 6/300, 60/300, 300/300) #Use these values for the time values in AUC calculation


attach(discounting_wide_MG)
discounting_wide_MG$AUC <- (((0.00083333-0)*((1 + indiff.0.25)/2)) + ((0.00166667-0.00083333)*((indiff.0.25+indiff.0.5)/2)) + ((0.00333333-0.00166667)*((indiff.0.5 + indiff.1)/2)) + ((0.02000000-0.00333333)*((indiff.1 + indiff.6)/2)) + ((0.20000000-0.02000000)*((indiff.6 + indiff.60)/2)) + ((1-0.20000000)*((indiff.60 + indiff.300)/2)))




####Notes####

#It is possible that despite using the nlxb function, the two-parameter models may fail because of a perfect fit. In this case, it would be reasonable to conclude that Mazur (1 parameter) would also fit well and would likely win in a AIC comparison.

