from match_prediction import predict_match
from pipeline import prepare_prediction_pipeline
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_resource
def load_prediction_system():
    return prepare_prediction_pipeline()


(
    team_records,
    logistic_model,
    random_forest_model,
    xgboost_model
) = load_prediction_system()

csv_path_file = "data/E0.csv"
df = pd.read_csv(csv_path_file)

st.title("Premier League AI predictor")
st.write("Welcome to my AI football prediction website")

team_list = pd.concat([df["HomeTeam"], df["AwayTeam"]]).unique()

home = st.selectbox(label="Home Team", options=team_list)
away = st.selectbox(label="Away Team", options=team_list)
predict_button = st.button("Predict")

if predict_button:
    if home == away:
        st.warning("Do not select the same team!!")

    else:
        result = predict_match(
            home,
            away,
            team_records,
            logistic_model,
            random_forest_model,
            xgboost_model
        )

        st.header(f"{home} vs {away}")

        logistic = result["logistic_regression"]
        random_forest = result["random_forest"]
        xgboost = result["xgboost"]

        # Logistic Regression
        st.subheader("Logistic Regression")
        st.write("Prediction:", logistic["prediction"])
        st.write("Home Win Probability:", f"{logistic['home_win_probability'] * 100:.2f}%")
        st.write("Draw Probability:", f"{logistic['draw_probability'] * 100:.2f}%")
        st.write("Away Win Probability:", f"{logistic['away_win_probability'] * 100:.2f}%")

        # Random Forest
        st.subheader("Random Forest")
        st.write("Prediction:", random_forest["prediction"])
        st.write("Home Win Probability:", f"{random_forest['home_win_probability'] * 100:.2f}%")
        st.write("Draw Probability:", f"{random_forest['draw_probability'] * 100:.2f}%")
        st.write("Away Win Probability:", f"{random_forest['away_win_probability'] * 100:.2f}%")

        # XGBoost
        st.subheader("XGBoost")
        st.write("Prediction:", xgboost["prediction"])
        st.write("Home Win Probability:", f"{xgboost['home_win_probability'] * 100:.2f}%")
        st.write("Draw Probability:", f"{xgboost['draw_probability'] * 100:.2f}%")
        st.write("Away Win Probability:", f"{xgboost['away_win_probability'] * 100:.2f}%")

        # Final Prediction
        predictions = [
            logistic["prediction"],
            random_forest["prediction"],
            xgboost["prediction"]
        ]

        number_of_home_wins = predictions.count("Home Win")
        number_of_draws = predictions.count("Draw")
        number_of_away_wins = predictions.count("Away Win")

        if (
            number_of_home_wins > number_of_draws
            and number_of_home_wins > number_of_away_wins
        ):
            final_prediction = "Home Win"

        elif (
            number_of_draws > number_of_home_wins
            and number_of_draws > number_of_away_wins
        ):
            final_prediction = "Draw"

        elif (
            number_of_away_wins > number_of_home_wins
            and number_of_away_wins > number_of_draws
        ):
            final_prediction = "Away Win"

        else:
            final_prediction = "No Consensus"
        st.subheader("Final Prediction")

        st.write(final_prediction)
        if final_prediction == "No Consensus":
            max_logistic = max(logistic["home_win_probability"],logistic["draw_probability"],logistic["away_win_probability"])
            max_random_forest = max(random_forest["home_win_probability"],random_forest["draw_probability"],random_forest["away_win_probability"])
            max_xgboost = max(xgboost["home_win_probability"], xgboost["draw_probability"], xgboost["away_win_probability"])
            highest_probability = max(max_logistic,max_random_forest,max_xgboost)

            if highest_probability == max_logistic:
                recommended_model = "Logistic Regression"
                recommended_prediction = logistic["prediction"] 
            elif highest_probability == max_random_forest:
                recommended_model = "Random Forest"
                recommended_prediction = random_forest["prediction"]
            else:
                recommended_model = "XGBoost"
                recommended_prediction = xgboost["prediction"]
            
            st.subheader("Recommendation")
            st.write("Recommended Model:", recommended_model)
            st.write("Recommended Prediction:", recommended_prediction)
            st.write("Confidence:", f"{highest_probability * 100:.2f}%")

        # Model Comparison Table
        table_data = {
            "Model": [
                "Logistic Regression",
                "Random Forest",
                "XGBoost"
            ],

            "Prediction": [
                logistic["prediction"],
                random_forest["prediction"],
                xgboost["prediction"]
            ],

            "Home Win": [
                f"{logistic['home_win_probability'] * 100:.2f}%",
                f"{random_forest['home_win_probability'] * 100:.2f}%",
                f"{xgboost['home_win_probability'] * 100:.2f}%"
            ],

            "Draw": [
                f"{logistic['draw_probability'] * 100:.2f}%",
                f"{random_forest['draw_probability'] * 100:.2f}%",
                f"{xgboost['draw_probability'] * 100:.2f}%"
            ],

            "Away Win": [
                f"{logistic['away_win_probability'] * 100:.2f}%",
                f"{random_forest['away_win_probability'] * 100:.2f}%",
                f"{xgboost['away_win_probability'] * 100:.2f}%"
            ]
        }

        result_dataframe = pd.DataFrame(table_data)
        st.subheader("Model Comparison")
        st.dataframe(result_dataframe, hide_index=True)

        # Probabilities
        logistic_probabilities = [
            logistic["home_win_probability"],
            logistic["draw_probability"],
            logistic["away_win_probability"]
        ]

        random_forest_probabilities = [
            random_forest["home_win_probability"],
            random_forest["draw_probability"],
            random_forest["away_win_probability"]
        ]

        xgboost_probabilities = [
            xgboost["home_win_probability"],
            xgboost["draw_probability"],
            xgboost["away_win_probability"]
        ]

        labels = [home, "Draw", away]

        # Logistic Regression Chart
        fig1, ax1 = plt.subplots()
        first_bar = ax1.bar(labels, logistic_probabilities)
        ax1.bar_label(first_bar, labels=[f"{probability * 100:.2f}%" for probability in logistic_probabilities])
        ax1.set_title("Logistic Regression Probabilities")
        ax1.set_ylim(0, 1)
        ax1.set_ylabel("Probability")
        st.pyplot(fig1)

        # Random Forest Chart
        fig2, ax2 = plt.subplots()
        second_bar = ax2.bar(labels, random_forest_probabilities)
        ax2.bar_label(second_bar, labels=[f"{probability * 100:.2f}%" for probability in random_forest_probabilities])
        ax2.set_title("Random Forest Probabilities")
        ax2.set_ylim(0, 1)
        ax2.set_ylabel("Probability")
        st.pyplot(fig2)

        # XGBoost Chart
        fig3, ax3 = plt.subplots()
        third_bar = ax3.bar(labels, xgboost_probabilities)
        ax3.bar_label(third_bar, labels=[f"{probability * 100:.2f}%" for probability in xgboost_probabilities])
        ax3.set_title("XGBoost Probabilities")
        ax3.set_ylim(0, 1)
        ax3.set_ylabel("Probability")
        st.pyplot(fig3)