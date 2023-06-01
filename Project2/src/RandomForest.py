import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE


class RandomForest:
    def __init__(self, data):
        self.data = data
        self.X_train, self.X_test, self.y_train, self.y_test = self._split_data()

    def _split_data(self):
        X = self.data.drop('fraud_bool', axis=1)
        y = self.data['fraud_bool']

        # Label encoding
        label_encoder = LabelEncoder()
        X_encoded = X.copy()
        for col in ['payment_type', 'employment_status', 'housing_status', 'source', 'device_os']:
            X_encoded[col] = label_encoder.fit_transform(X[col])

        # Sparse one-hot encoding
        X_encoded = pd.get_dummies(X_encoded, columns=['payment_type', 'employment_status', 'housing_status', 'source', 'device_os'], sparse=True)

        # Perform oversampling using SMOTE
        oversampler = SMOTE(random_state=42)
        X_resampled, y_resampled = oversampler.fit_resample(X_encoded, y)

        X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def train(self):
        self.clf = RandomForestClassifier(n_jobs=-1)  # Enable parallel processing
        self.clf.fit(self.X_train, self.y_train)

    def predict(self, X_test):
        return self.clf.predict(X_test)

    def evaluate(self):
        y_pred_proba = self.clf.predict_proba(self.X_test)[:, 1]
        fpr, tpr, thresholds = roc_curve(self.y_test, y_pred_proba)
        auc_roc = roc_auc_score(self.y_test, y_pred_proba)

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