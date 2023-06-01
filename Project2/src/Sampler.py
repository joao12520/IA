import pandas as pd
import numpy as np
class Sampler:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.data = pd.read_csv(data_file_path)

    def sample(self, n, fraud_ratio):
        fraud = self.data[self.data['fraud_bool'] == 1]
        non_fraud = self.data[self.data['fraud_bool'] == 0]

        fraud_sample = fraud.sample(int(n * fraud_ratio))
        non_fraud_sample = non_fraud.sample(int(n * (1 - fraud_ratio)))

        sample = pd.concat([fraud_sample, non_fraud_sample]).sample(frac=1).reset_index(drop=True)

        return pd.concat([fraud_sample, non_fraud_sample])
