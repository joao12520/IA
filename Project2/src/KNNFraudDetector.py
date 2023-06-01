import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.model_selection import learning_curve


class KNNFraudDetector:
    def __init__(self, data):
        self.data = data
        self.xtrain, self.xtest, self.ytrain, self.ytest = self._split_data()

    def _split_data(self):
        x = self.data.drop('fraud_bool', axis=1)
        y = self.data['fraud_bool']
        X_encoded = pd.get_dummies(x, columns=['payment_type', 'employment_status', 'housing_status', 'source',
                                               'device_os'])

        oversampler = SMOTE(random_state=42)
        X_resampled, y_resampled = oversampler.fit_resample(X_encoded, y)

        xtrain, xtest, ytrain, ytest = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)
        return xtrain, xtest, ytrain, ytest

    def train(self):
        self.clf = KNeighborsClassifier(n_neighbors=5)
        self.clf.fit(self.xtrain, self.ytrain)

    def predict(self, input_data):
        return self.clf.predict(input_data)

    def evaluate(self):
        y_pred_proba = self.clf.predict_proba(self.xtest)[:, 1]
        fpr, tpr, thresholds = roc_curve(self.ytest, y_pred_proba)
        auc_roc = roc_auc_score(self.ytest, y_pred_proba)

        # Print AUC-ROC score
        print("AUC-ROC Score:", auc_roc)
        for i, threshold in enumerate(thresholds):
            if fpr[i] <= 0.05:
                print("Threshold: {:.2f}, FPR: {:.2f}, TPR: {:.2f}".format(threshold, fpr[i], tpr[i]))

        # Plot ROC curve
        plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc_roc)
        plt.plot([0, 1], [0, 1], 'k--')  # Random guessing line
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC)')
        plt.legend(loc='lower right')
        plt.show()

    def confusion_matrix(self):
        # Assuming you have already trained your model and obtained predictions
        y_pred = self.clf.predict(self.xtest)

        # Create a confusion matrix
        cm = confusion_matrix(self.ytest, y_pred)

        cm_df = pd.DataFrame(cm, index=['Actual Negative', 'Actual Positive'],
                             columns=['Predicted Negative', 'Predicted Positive'])

        # Create a heatmap of the confusion matrix
        sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues")

        # Add labels, title, and axis ticks
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.title("Confusion Matrix for KNN")

        plt.show()

    def plot_learning_curve(self):
        print("Trying to build plot")
        train_sizes, train_scores, test_scores = learning_curve(self.clf, self.xtrain, self.ytrain, cv=5, scoring='accuracy',
                                                                train_sizes=np.linspace(0.1, 1.0, 10))

        train_mean = np.mean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)
        test_mean = np.mean(test_scores, axis=1)
        test_std = np.std(test_scores, axis=1)

        plt.figure(figsize=(8, 6))
        plt.plot(train_sizes, train_mean, 'o-', color='r', label='Training Accuracy')
        plt.plot(train_sizes, test_mean, 'o-', color='g', label='Validation Accuracy')
        plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='r')
        plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1, color='g')
        plt.xlabel('Training Set Size')
        plt.ylabel('Accuracy')
        plt.title('Learning Curve')
        plt.legend(loc='best')
        plt.grid(True)
        plt.show()