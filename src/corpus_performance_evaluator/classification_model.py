import pandas as pd
import warnings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle


warnings.filterwarnings('ignore')

if __name__ == '__main__':
    # Get the data
    base_path = ("C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus "
                 "Lectura Fácil (2023) - Documentos/data/corpus_performance_evaluator/")
    final_corpus_path = base_path + "encoding/encoded_text.csv"
    df = pd.read_csv(final_corpus_path, sep="|", encoding="utf-8")

    # Split the data
    X = df.loc[:, df.columns != 'class']
    y = df["class"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    # define the model
    model = RandomForestClassifier(verbose=1, n_estimators=100)

    # fit the model on the whole dataset
    print("Training model...")
    model.fit(X_train, y_train)

    # Save the model
    print("Saving model...")
    model_path = base_path + "classification_model/random_forest.pkl"
    pickle.dump(model, open(model_path, 'wb'))

    # load the model from disk
    print("Testing model...")
    loaded_model = pickle.load(open(model_path, 'rb'))
    result = loaded_model.score(X_test, y_test)
    print(result)
