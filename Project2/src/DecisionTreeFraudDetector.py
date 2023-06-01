import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

class DecisionTreeFraudDetector:
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
        self.clf = DecisionTreeClassifier(max_depth=5, min_samples_split=5)
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
