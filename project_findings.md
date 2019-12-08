## Questions and Tasks
### (1) Data Usage.


(a) What outside data have you appended to the original data set? Why did you choose this data?

- We added crime data, school data, and parks data. We used NYC Open data to retrieve these data. The reason why we chose this data is because we believe that these are some of the major factors that may affect rent prices in the area. 

(b) Does the inclusion of this additional data raise any ethical considerations?

- The inclusion of the additional datas may raise ethical considerations such as choosing neighborhoods, since we added crime data, it will show that certain neighoborhoods have higher crime rates which may raise a ethical consideration. 

### (2) Data Exploration.
(a) What outliers present issues for your analysis? How have you chosen to handle them? Why?


(b) To what extent do missing values pose a challenge for your analysis? How have you chosen to
handle them? Why?


(c) Are there any other aspects of the data your exploration shows might be problematic?


(d) Create at least one visualization that demonstrates the predictive power of your data.


### (3) Transformation and Modeling.
(a) Describe 5 features you think play the biggest role in your model.

- Five features that play the biggest role in our model are size_sqft, number_of_privileges, floor_count, bedrooms, and park_level. We can see that when the size_sqft, bedrooms, number_of_privileges, increases/ decreases, it affects the rent prices as well. 

• How did you create these features?
- These features were created by importing the training data set as well as appending new data sets for park_level

• How do you know these features are playing key roles?
- We know these features are playing a key roles in our model because it affects the rent price. By looking at the size_sqft or bedrooms, the rent price changes along with it. 

If your modeling process uses less than five features, explain why you think other features didn’t
add value.


(b) Describe how you are implementing your model. Why do you think this works well?


(c) Describe your methodology for selecting your model. Why do you think this type of model works
well?


### (4) Metrics, Validation, and Evaluation.
(a) How well do you think you model will perform on the hold out test set? How do you know?


(b) Is your model useful? Why or why not?


(c) Are there any special cases in which your model works particularly well or particularly poorly?


(d) Create at least one visualization that demonstrates the predictive power of your model.


### (5) Conclusion
(a) How would you use this model?


(b) If you could have additional modeling features, what would they be?


(c) Would you rather have more data, or more features?

