# Read in the output file from the python function and add titles to the columns to make it more readable

data <- read.csv("output.csv", header = T)
names(data) <- c("BayID", "DateTime", "Occupancy")

# Order the file by bay location key

data <- data[order(data$BayID),]

# There are 1428 unique location bays in the file given by the following code:

nrow(table(data$BayID))

# Look at bay number 344 for this model but could equally repeat this steps for every bay in the 1428 cases

dataBay344 <- data[data$BayID == 344,]

# Add a column to the dateframe corresponding the day of the week

dataBay344$Day <- weekdays(as.Date(dataBay344$Date))

# Strip the time from the Date column

dataBay344$DateTime <- as.character(dataBay344$DateTime)
dataBay344$Time <- substring(dataBay344$DateTime, 12, 13)

# Change the start, end times and day of week as factors to ensure that they are in the right format for the generalised linear model

dataBay344$Day <- as.factor(dataBay344$Day)
dataBay344$Time <- as.factor(dataBay344$Time)

# Set up the glm

model <- glm(Occupancy ~ Day + Time, data = dataBay344)
 
# Model summary shows the high significance of the positive correlation of occupancy with the 9-5 time bracket as well as the high significance of the negative correlation with parking occupancy with Saturday and Sunday, which is more marked on Sunday than Saturday.
 
summary(model)
