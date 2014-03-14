Predicting parking availability
================================

If we were able to continuously update the database with the latest cashless transactions,
we could use linear regression to predict the number of cars parked at a given bay at time (measured in hours):
Parameters could be fitted from the past month’s data.

However, we weren’t given a live feed of parking transactions, so a practical alternative is to use the historical data
to predict the most likely parking availability given the day and time. We do this with a generalized linear model 
(see the script “R_glm_script.R”). This method provides parameters for estimating the future occupancy at a given parking
bay, time, and day of the week.
