import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, auc, precision_recall_curve

from src.corpus_performance_evaluator.classification_model import ClassificationModel


class CustomMetrics:

    def __init__(self, actual, predicted):
        self.actual = actual
        self.predicted = predicted
        self.true_positive = None
        self.false_positive = None
        self.false_negative = None
        self.true_negative = None
        self.confusion_matrix()

    def confusion_matrix(self, print_matrix=False):
        """
        Confusion Matrix as the name suggests gives us a matrix as output and describes the complete performance of the
        model. It gives you 4 important metrics of the model: True Positives, True Negatives, False Positives and
        False Negatives.
        :return: Array of unique classes and matrix of confusion
        """
        unique = set(self.actual)
        matrix = [list() for x in range(len(unique))]
        for i in range(len(unique)):
            matrix[i] = [0 for x in range(len(unique))]
        lookup = dict()
        for i, value in enumerate(unique):
            lookup[value] = i
        for i in range(len(self.actual)):
            x = lookup[self.actual[i]]
            y = lookup[self.predicted[i]]
            matrix[y][x] += 1

        self.true_positive = matrix[0][0]
        self.false_positive = matrix[0][1]
        self.false_negative = matrix[1][0]
        self.true_negative = matrix[1][1]

        if print_matrix:
            self.print_confusion_matrix(matrix, unique)

        return unique, matrix

    @staticmethod
    def print_confusion_matrix(matrix, unique):
        print('(A)' + ' '.join(str(x) for x in unique))
        print('(P)---')
        for i, x in enumerate(unique):
            print("%s| %s" % (x, ' '.join(str(x) for x in matrix[i])))

    def accuracy_metric(self):
        """
        Measures the proportion of correct predictions out of the total number of predictions.
        Accuracy = (True positive + True negative) / Total number of predictions
        :return: float
        """
        return (self.true_positive + self.true_negative) / len(self.actual)

    def precision_metric(self):
        """
        Measures the proportion of true positives over the addition between true and false positives. Useful when we
        want to minimize false positive.
        Precision = True positive / (True positive + False positive)
        :return: float
        """
        return self.true_positive / (self.true_positive + self.false_positive)

    def recall_metric(self):
        """
        It is the number of correct positive results divided by the number of all relevant samples (all samples that
        should have been identified as positive).
        Recall = True positive / (True positive + False negative)
        :return: float
        """
        return self.true_positive / (self.true_positive + self.false_negative)

    def f1_metric(self):
        """
        F1 Score is the Harmonic Mean between precision and recall. The range for F1 Score is [0, 1]. It tells you how
        precise your classifier is, as well as how robust it is. As closer to 1 this metric is the better the model is.
        F1 = 2 / ((1 / Precision) + (1 / Recall))
        :return: float
        """
        return 2 / ((1 / self.precision_metric()) + (1 / self.recall_metric()))

    def auc_metric(self):
        """
        Represents the relation between true positives and false positives. The area under the curve measures the
        discriminative capacity of the model.
        :return: float
        """
        return roc_auc_score(self.actual, self.predicted)

    def auc_pr_metric(self):
        """
        Represents the relation between precision and recall
        :return: float
        """
        # calculate precision-recall curve
        precision, recall, thresholds = precision_recall_curve(self.actual, self.predicted)

        # calculate precision-recall AUC
        return auc(recall, precision)

    def calculate_metrics_report(self, save=False, path=None):
        metrics = {"Metric": ["Accuracy", "Precision", "Recall", "F1-score", "auc_roc", "auc_pr"],
                   "Value": []}

        # Confusion matrix
        self.confusion_matrix(print_matrix=True)

        # Accuracy
        accuracy = self.accuracy_metric()
        metrics["Value"].append(accuracy)
        print("Accuracy: ", accuracy)

        # Precision
        precision = self.precision_metric()
        metrics["Value"].append(precision)
        print("Precision: ", precision)

        # Recall
        recall = self.recall_metric()
        metrics["Value"].append(recall)
        print("Recall: ", recall)

        # F1-Score
        f1_score = self.f1_metric()
        metrics["Value"].append(f1_score)
        print("F1-score: ", f1_score)

        # Area under ROC curve
        auc_roc = self.auc_metric()
        metrics["Value"].append(auc_roc)
        print("Area under ROC curve: ", auc_roc)

        # Area under precision recall curve
        auc_pr = self.auc_pr_metric()
        metrics["Value"].append(auc_pr)
        print("Area under precision & recall curve: ", auc_pr)

        if save:
            pd.DataFrame.from_dict(metrics).to_csv(path, index=False, sep=";")


if __name__ == '__main__':
    path = ("C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus "
            "Lectura Fácil (2023) - Documentos/data/corpus_performance_evaluator/")
    RF_obj = ClassificationModel(RandomForestClassifier, path)
    RF_obj.save_split_data()
    RF_obj.load_model()
    RF_obj.load_split_data()
    predicted = RF_obj.predict(RF_obj.X_test)

    cm_obj = CustomMetrics(RF_obj.y_test["class"].array, predicted)
    cm_obj.calculate_metrics_report(path=(path + "classification_model/metrics.csv"), save=False)
