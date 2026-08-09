from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

reverse_result_mapping = {
    0: "H",
    1: "D",
    2: "A"
}


def convert_xgboost_predictions(predictions):

    converted_predictions = []

    for prediction in predictions:
        converted_predictions.append(
            reverse_result_mapping[prediction]  
        )

    return converted_predictions

def evaluate_predictions(predictions,test_y,test_matches):
    correct_predictions = 0
    for index,prediction in enumerate(predictions):
        actual = test_y.iloc[index]
        match = test_matches.iloc[index]
        home_team = match["HomeTeam"]
        away_team = match["AwayTeam"]

        if prediction == actual:
                correct_predictions += 1
        else:
            print(f" {home_team} vs {away_team} | "
                      f"Actual: {actual} | prediction: {prediction}")
    accuracy = (correct_predictions / len(test_y) * 100)
    matrix = confusion_matrix(test_y, predictions,labels=["H", "D", "A"])     
    classification = classification_report(test_y, predictions, labels=["H", "D", "A"], zero_division=0)     
    return (accuracy , matrix, classification)
  

def print_evaluation(model_name,accuracy,matrix,classification):
    
    print("==============================")
    print(model_name)
    print("==============================")
    print(f"Accuracy: {accuracy:.2f}%")
    print("Confusion Matrix:")
    print(matrix)
    print("Classification Report:")
    print(classification)




