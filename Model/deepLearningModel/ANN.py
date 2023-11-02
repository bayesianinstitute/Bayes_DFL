import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import subprocess
from sklearn.model_selection import train_test_split

class ANNTabularClassification:
    def __init__(self, optimizer='adam',log=' "custom_ANN_log"'):
        self.optimizer = optimizer
        self.x_train, self.y_train, self.x_test, self.y_test = self.load_and_preprocess_data()

        self.model = self.build_model()
        self.dir_log = log # Set the log directory

    def build_model(self):
        # Build a simple ANN model for tabular data
        model = Sequential()
        model.add(Dense(64, activation='relu', input_shape=(self.x_train.shape[1],)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(optimizer=self.optimizer, loss='binary_crossentropy', metrics=['accuracy'])

        return model

    def load_and_preprocess_data(self):
        # Load and preprocess the Titanic dataset (you should replace 'titanic.csv' with your dataset)
        dataset = pd.read_csv('titanic.csv')

        # Preprocess data (replace this with your own data preprocessing)
        x = dataset.drop(columns=['Survived'])
        y = dataset['Survived']

        # Split data into training and testing sets
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        return x_train, y_train, x_test, y_test

    def train_model(self, epochs=10, batch_size=32):
        # Create a TensorBoard callback to log the training process
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=self.dir_log)

        # Train the model and use the TensorBoard callback
        self.model.fit(self.x_train, self.y_train, epochs=epochs, batch_size=batch_size, callbacks=[tensorboard_callback])

    def evaluate_model(self):
        # Evaluate the model on the test data
        test_loss, test_accuracy = self.model.evaluate(self.x_test, self.y_test)
        return test_loss, test_accuracy

    def run_tensorboard(self):
        try:
            subprocess.run(["tensorboard", "--logdir", self.dir_log])
        except Exception as e:
            print(f"Error running TensorBoard: {e}")

# Usage example:
if __name__ == '__main__':
    tabular_model = ANNTabularClassification('adam')
    tabular_model.train_model(epochs=10, batch_size=32)
    test_loss, test_accuracy = tabular_model.evaluate_model()
    print(f'Test loss: {test_loss:.4f}, Test accuracy: {test_accuracy:.4f}')

    tabular_model.run_tensorboard()