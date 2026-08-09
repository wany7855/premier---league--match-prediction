# Premier League Match Result Prediction

## Project Overview

This project uses the 2024/2025 Premier League dataset to predict football match results using machine learning.

First, the project loads and processes the required match data and creates features such as win percentage,
average goals scored and conceded, home and away performance, goal difference, and recent form.

These features are then used to train three machine learning models:
Logistic Regression, Random Forest, and XGBoost.

The models are evaluated and compared using performance metrics such as accuracy,
confusion matrices, and classification reports.

Finally, the trained models are used to predict whether a selected match will result in
a home win, a draw, or an away win, together with the predicted probabilities.


## Demo
The Streamlit web application allows users to select a home team and an away team.

The Streamlit application includes:

- The selected match
- Match result predictions from Logistic Regression, Random Forest, and XGBoost
- Home Win, Draw, and Away Win probabilities for each model
- A combined final prediction based on the three model outputs
- A model comparison table
- Bar charts showing the prediction probabilities for each model

## Technologies Used
- Python
- Pandas
- Scikit-learn
- XGBoost
- Streamlit
- Matplotlib

## Project Structure

| file | Description |
|---|---|
| data.py | Loads the Premier League csv dataset and stores team data. |
| team_compare.py | Compares statistics between two selected teams. |
| team_metrics.py | Calculates statistics for individual teams. |
| league_table.py | Creates and sorts the league table based on points, goal difference, and goals scored. |
| feature_engineering.py | Creates the features used by the machine learning models. |
| match_prediction.py | Uses the trained models to predict a selected match. |
| model_evaluation.py | Evaluates and compares model performance. |
| model_training.py | Creates and trains the logistic regression, random forest, and xgboost models. |
| pipeline.py | Connects the data, feature creation, and model training steps. |
| main.py | Runs the main project workflow and displays the results. |
| website.py | Runs the Streamlit web application. |

## Feature Engineering

I created simple statistics from past matches to measure each team's performance before a match.

The features include:

- Overall performance:
  - Win percentage
  - Draw percentage
  - Loss percentage
  - Average goals scored per match
  - Average goals conceded per match
  - Goal difference

- Home and away performance:
  - Home win percentage
  - Away win percentage
  - Home average goals scored
  - Home average goals conceded
  - Away average goals scored
  - Away average goals conceded

- Recent form:
  - Recent win percentage
  - Recent draw percentage
  - Recent average goals scored
  - Recent average goals conceded

To predict each match, I used the past match records of the home and away teams. To show which team was stronger, I added the difference between their win percentages. Moreover, I only used records available before each match to prevent data leakage.

## Model Training
Three machine learning models were trained to predict the Premier League match results.
- Logistic Regression
- Random Forest
- XGBoost

Each model was trained using features based on each team's past data before the match. These features include the team's overall records, home and away results, recent form, goals statistics, and the win percentage difference between two teams.


`train_x` contains numerical features used to train the models, while `train_y` contains the actual match results.
For XGBoost, the match result labels  were converted from strings into numerical labels.
For logistic regression and random forest, class weighting was used to reduce the effect of class imbalance among Home Wins, Draws, and Away Wins.

For Logistic Regression, I initially set `max_iter = 100`. However, the terminal displayed a `ConvergenceWarning`, indicating that the model had not fully converged within 100 iterations. Therefore, I increased `max_iter` to 500.

## Model Evaluation
As I mentioned before, I used accuracy, confusion matrix, and classification report for evaluating the model performance.
For accuracy, I measured the percentage of all test matches that the model predicted correctly. 

I compared the actual match results with the model's predictions using a confusion matrix. This showed which classes the model predicted correctly and which classes it confused with others, such as predicting a Draw as a Home Win. It helped to understand the model's mistakes, which cannot be seen by looking at accuracy alone.

I also checked the Precision, Recall, and F1-score for each class using the classification report. The numbers of Home Wins, Draws, Away Wins in the Premier League data were not equal. Therefore, I evaluated the performance of each class instead of looking only at the overall accuracy.

### Classification Metrics
- Precision : How often the model's prediction for each class was correct.
- Recall : How many of the actual results the model predicted correctly.
- F1-score : A score that shows the overall balance between Precision and Recall.

## Results
Logistic Regression: 38.16%
Random Forest: 40.79%
XGBoost: 46.05%

As shown above, XGBoost achieved the highest accuracy among the three models.
It was 5.26 percentage points higher than Random Forest and 7.89 percentage points higher than Logistic Regression.


However, accuracy alone does not show how well the model predicts each class.
Therefore, I also used a confusion matrix and classification report to evaluate the performance for home wins, draws, and away wins. The classification report was used to compare precision, recall, and F1-score for each match result(`H`,`D`,`A`).

## How to run 
To use it in the terminal:
Python src/main.py

To use it on the website:
streamlit run src/website.py

