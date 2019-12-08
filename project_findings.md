# Questions and Tasks
## (1) Data Usage.


**(a) What outside data have you appended to the original data set? Why did you choose this data?**
1. Price per sqft of rentals
    * This data allowed us to get an idea for how much size square feet affects the rental property by an actual dollar amount. Doing so allows our model to get closer to the actual rental property using the size sqft.

2. Zip Code demographics 
    * The zip code demographics give us an idea of the kind of people that live in that neighborhood. For example, the IncomePerHousehold column tells us, on average, how much money people make in that zip code. The idea is that people with a higher income will live in more upscale neighborhoods with higher rent.

3. Number of nearby parks
   * The idea behind nearby parks is that people will pay higher money the more parks there are in the area. For example, people who live near battery park and central park have higher rent. Also, more parks usually mean it’s a better neighborhood for families.
4. School information
   * School information is oriented towards family neighborhoods as well. The idea is that neighborhoods with better schools will have higher rent. 

**(b) Does the inclusion of this additional data raise any ethical considerations?**

No all our data are taken from either NYC open data or API services from websites thus we did not raise any ethical considerations. As far as the actual data, the fact that we're using demographic information may raise ethical issues if we assume certain demographics cause higher rents. 

## (2) Data Exploration.

**(a) What outliers present issues for your analysis? How have you chosen to handle them? Why?**

There are many outliers that we noticed from our analysis. There were outliers in the size_sqft, bathrooms, minutes to subway, and bedrooms. We handled these values on a case by case basis. Certain ones that seemed both extreme and made little sense were dropped. However, there were others that made sense and we decided to keep them in mind as we developed our model. 

**(b) To what extent do missing values pose a challenge for your analysis? How have you chosen to
handle them? Why?**

There were many missing values in the data, not only null values, but values that were labeled as 0 that made no sense ( such as size_sqft == 0 ). We attempted to impute the values that we deemed necessary for our model. So, we used a linear regression to model size sqft and get an approximation for rows with a size sqft == 0. We chose to do it this way because size_sqft is an important value so we thought it might be important to try and get as close a value as possible to the real value. This could not be achieved by simply finding the mean and using it to impute. 

We also imputed mins_to_subway using the average minutes to subway for the corresponding zip code. We chose to impute rather than drop because we knew that we were going to have to deal with similar values in our test set, so we had to come up with a better way of dealing with them other than just dropping them. 


**(c) Are there any other aspects of the data your exploration shows might be problematic?**

Originally we thought that floor number and floor count would be powerful features in our model. However, data exploration showed that there were many invalid values for these columns to be of any use. There was no way of knowing if the floor count was invalid, or if the floor number was invalid, without looking up each value individually. 

During our data exploration, we also found that there were many neighborhoods with a much larger average rent than other neighborhoods, and it would be difficult to find a way to incorporate these in our model since they are such large outliers. So, we ended up making a feature which determined if that rent listing was located in a top neighborhood. This would hopefully account for the large rent differences between other neighborhoods and these so-called top neighborhoods.

**(d) Create at least one visualization that demonstrates the predictive power of your data.**


## (3) Transformation and Modeling.

**(a) Describe 5 features you think play the biggest role in your model.**

The 5 features that play the biggest role in our model are the size_sqft, avg_price_per_sqft, bedrooms, bathrooms, income_per_household. Size square feet, bedrooms, and bathrooms came with the data set, however we subjected them to outlier detection, and in the case of size sqft we also imputed missing values to make the feature more useful. Avg_price_per_sqft we retrieved from an external data set. However, there were some neighborhoods that didn’t have the average price per sqft, so we imputed these values using the average price per sqft for the entire borough. Lastly, we had income_per_household which we got from the zip code demographic information from our external data source. 


**How do you know these features are playing key roles?**

To determine the usefulness of these features we ran various tests that tested feature importance. Each feature importance test outputted the top 20 features that it deemed important. Afterwards, I compiled these results and found features that were deemed important by multiple tests. These top 5 features were among the top features after compiling the results. 

Also, domain knowledge told us that if a person is looking to rent an apartment, these would probably be things that would sway the price heavily. 

Lastly, during our experimentation, we tried removing some of these features, and found that our model performed significantly worse. Thus, we concluded that these features were high predictive. 

If your modeling process uses less than five features, explain why you think other features didn’t add value.


**(b) Describe how you are implementing your model. Why do you think this works well?**

To implement our model, the first thing we had to do is data engineering. Since there are a lot of missing values, un-meaningful values, and duplicate data, we had to clean our data. Additionally, we looked into the outliers of our data and made sure to fix and remove any “true” outliers. We then fed the features we selected into our model and checked with cross-validation to see if our model works well on unseen data. Our process works well because we are eliminating data that might negatively influence our model. By using feature engineering we are extracting meaningful features from our original features to further boost our models performance.

**(c) Describe your methodology for selecting your model. Why do you think this type of model works
well?**

Since we are dealing with continuous data, we needed to choose a regression model. By looking at the correlation between the features, utilizing data visualization, and calculating feature importance, we determined that linear regression model will not work with the street easy dataset. We also noticed a lot of feature dependencies which led us to choose a non-linear model. We then chose between random forest regression and boosting methods which are known as powerful non-linear models that tend to not overfit as much. Finally, we used a grid search to choose hyperparameters and also find which model performed the best. This led us to pick random forest. 


## (4) Metrics, Validation, and Evaluation.

**(a) How well do you think you model will perform on the hold out test set? How do you know?**

I believe that our model will have a mean squared error ranging from 1 million to 1.5 million. After running various tests on  the training data, we came up with a solid model, and ran it on a holdout set. On the holdout set we got an MSE of 1065373. 

Our performance on the final test set is highly dependent on how many outliers are contained in the data. We believe our model can handle normal cases pretty well, but we noticed highly variable outcomes on outlier data. 


**(b) Is your model useful? Why or why not?**

Our model is useful for predicting rent prices that are on the lower spectrum of prices. For instances when our model predict rent prices on the Upper East Side neighborhoods, our model had trouble predicting the rent prices. This might be due to the lack of high prices data we have. Thus our model is mostly uses for predicting low rent prices.


**(c) Are there any special cases in which your model works particularly well or particularly poorly?**

After training our model, we used our model to predict on our training set. Ideally, our model should be able to predict these perfectly. However, it did not, so we took advantage of this fact to see where our model had a high MSE. We found that our model had a high MSE on properties in high end neighborhoods, especially the Upper West and Upper East side. We believe there may be some features in these neighborhoods that we don’t have. Also, when imputing the size sqft, mistakes in Manhattan tended to create a larger MSE since the price per sqft for rentals is much higher in Manhattan.

**(d) Create at least one visualization that demonstrates the predictive power of your model.**


## (5) Conclusion

**(a) How would you use this model?**

We would use this model when trying to find an apartment to move to. Using this model would give us a ballpark estimate for the value of an apartment, thus we could see if the current rental price is a rip-off.

**(b) If you could have additional modeling features, what would they be?**

We originally planned to add the crime data to our current dataset but due to the complexity of the dataset from NYC open data and poor correlation we found, we proceed not to continue with the crime data. If we had more time to scrub the crime data we believe that it would affect our model. Additionally, the other feature that we wanted to add is a more accurate school data, the API service that we used to find the school data was not from a reliable source and having a reliable source would increase the predictive power of school data.

**(c) Would you rather have more data, or more features?**

Having more data allows us to follow the law of large numbers which means that we get close to the true distribution of the data. The dataset that we have does not have a lot of rentals with large price rent which makes our model more biased towards cheaper rents and makes large rental prices harder to predict. Having more data allows us to further train our model on data that consist of high rent prices. Adding more features would not help us with the lack of certain data. 
