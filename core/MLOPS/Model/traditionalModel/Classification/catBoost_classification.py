import datetime
import catboost
import mlflow
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class CatBoostTabularClassification:
    def __init__(self, ip="http://localhost", port=5000, experiment_name='catboost_classification_experiment'):
        self.x_train, self.y_train, self.x_test, self.y_test = self.load_and_preprocess_data()

        # Start MLflow experiment
        self.name = "CatBoost_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.url = f'{ip}:{port}'
        self.config_mlflow(experiment_name, self.url)

        self.model = self.build_model()

    def config_mlflow(self, experiment_name, url):
        try:
            mlflow.set_tracking_uri(url)
            mlflow.set_experiment(experiment_name)
        except Exception as e:
            print(f"Error configuring MLflow: {e}")

    def build_model(self):
        # Build a CatBoost classification model
        model = catboost.CatBoostClassifier(random_state=42)
        return model

    def load_and_preprocess_data(self):
        # Load the California housing dataset
        data = fetch_california_housing()

        # Access the feature data
        X = data.data

        # Convert regression target to a binary classification problem (example)
        y = (data.target > data.target.mean()).astype(int)

        # Split data into training and testing sets
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        return x_train, y_train, x_test, y_test

    def train_model(self):
        try:
            mlflow.start_run(run_name=f'{self.name}_CatBoost')
            mlflow.autolog()

            # Train the model and log metrics using MLflow
            self.model.fit(self.x_train, self.y_train)

            # Evaluate the model on the test set
            test_predictions = self.model.predict(self.x_test)

            # Calculate classification metrics
            accuracy = accuracy_score(self.y_test, test_predictions)
            precision = precision_score(self.y_test, test_predictions)
            recall = recall_score(self.y_test, test_predictions)
            f1 = f1_score(self.y_test, test_predictions)

            # # Log metrics
            # mlflow.log_metric("accuracy", accuracy)
            # mlflow.log_metric("precision", precision)
            # mlflow.log_metric("recall", recall)
            # mlflow.log_metric("f1", f1)

            return accuracy, precision, recall, f1

        except Exception as e:
            print(f"Error training the model: {e}")

    def save_model(self, model_filename):
        try:
            # Save the model to a file and log as an artifact
            model_path = f"mlruns/models/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}/{model_filename}"
            self.model.save_model(model_path)
            mlflow.log_artifact(model_path)
            mlflow.end_run()

            print(f"Model saved as artifact: {model_filename}")
        except Exception as e:
            print(f"Error saving the model: {e}")

if __name__ == '__main__':
    # Example usage:
    catboost_classification_model = CatBoostTabularClassification()
    catboost_classification_model.train_model()
    catboost_classification_model.save_model("catboost_model.json")
    print("Completed training")
