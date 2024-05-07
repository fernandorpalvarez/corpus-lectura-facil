import os.path

import pandas as pd
import warnings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

warnings.filterwarnings('ignore')


class ClassificationModel:
    def __init__(self, model_class, base_path):
        # Instance the model
        self.model = model_class(verbose=1, n_estimators=100)

        # Get the data
        self.base_path = base_path
        self.df = self.load_data()

        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = self.split_df()

    def load_data(self):
        final_corpus_path = self.base_path + "encoding/encoded_text.csv"
        return pd.read_csv(final_corpus_path, sep="|", encoding="utf-8")

    def split_df(self):
        # Split the data
        x = self.df.loc[:, self.df.columns != 'class']
        y = self.df["class"]
        return train_test_split(x, y, test_size=0.33, random_state=42)

    def save_split_data(self):
        data_path = self.base_path + "classification_model/train_test_data/"

        # If the data folder for the splits does not exist, create one
        if not os.path.isdir(data_path):
            os.mkdir(data_path)

        # Save the splits
        self.X_train.to_csv(data_path + "x_train.csv", index=False, sep="|", encoding="utf-8")
        self.y_train.to_csv(data_path + "y_train.csv", index=False, sep="|", encoding="utf-8")
        self.X_test.to_csv(data_path + "x_test.csv", index=False, sep="|", encoding="utf-8")
        self.y_test.to_csv(data_path + "y_test.csv", index=False, sep="|", encoding="utf-8")

    def load_split_data(self):
        data_path = self.base_path + "classification_model/train_test_data/"

        # Load the splits
        self.X_train = pd.read_csv(data_path + "x_train.csv", sep="|")
        self.y_train = pd.read_csv(data_path + "y_train.csv", sep="|")
        self.X_test = pd.read_csv(data_path + "x_test.csv", sep="|")
        self.y_test = pd.read_csv(data_path + "y_test.csv", sep="|")

    def train_model(self):
        # fit the model on the whole dataset
        print("Training model...")
        self.model.fit(self.X_train, self.y_train)

    def save_model(self):
        # Save the model using the pickle library
        print("Saving model...")
        model_path = self.base_path + "classification_model/random_forest.pkl"
        pickle.dump(self.model, open(model_path, 'wb'))

    def load_model(self):
        # Load the model using the pickle library
        model_path = self.base_path + "classification_model/random_forest.pkl"
        self.model = pickle.load(open(model_path, 'rb'))

    def predict(self, data):
        return self.model.predict(data)


if __name__ == '__main__':
    path = ("C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus "
            "Lectura Fácil (2023) - Documentos/data/corpus_performance_evaluator/")
    RF_obj = ClassificationModel(RandomForestClassifier, path)
    RF_obj.save_split_data()
    RF_obj.load_model()
    RF_obj.load_split_data()
    RF_obj.predict(RF_obj.X_test)
