## :soccer: guesstimator MVP

### Project Goal:
Gain the ability to predict Premier League  match scores simply based on home and away team names :soccer: :trophy:  

### Project Summary:
Using Premier League match dataset containing results from 2006/2007 to 2017/2018 seasons, train a model (guesstimator) that would predict whether the upcoming match will result in a loss, draw or a win for selected team and provide a probability of that outcome  

### Project Approach:  
1. Split the dataset into train - test
2. Explore the dataset, evaluate data quality
3. Cross-check test cases online
4. Analyze the dataset
5. Identify independent variables
6. Dummify categorical variables *(if needed)*
7. Train multiple models (using techniques to pick the optimal parameters):
      * Random Forest
      * XGBoost
      * Other *(if needed)*
8. Assess performance of each model through cross-validation
9. Choose the optimal model and run it on the test set
10. Build a simple interface
11. A/B test with the remaining games of the 2018/2019 season
