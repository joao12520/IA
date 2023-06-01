import Sampler
from src.KNNFraudDetector import KNNFraudDetector
from src.DecisionTreeFraudDetector import DecisionTreeFraudDetector
from src.RandomForest import RandomForest


def main():
    sampler = Sampler.Sampler('../datasets/Base.csv')
    data = sampler.sample(10000, 0.1)

    fraudKNN = KNNFraudDetector(data)
    fraudKNN.train()
    fraudKNN.evaluate()
    fraudKNN.confusion_matrix()
    fraudKNN.plot_learning_curve()

    #dt = DecisionTreeFraudDetector(data)
    #dt.train()
    #dt.evaluate()
    # resultado = 0.94

    #rf = RandomForest(data)
    #rf.train()
    #rf.evaluate()
    # resultado = 0.99


if __name__ == '__main__':
    main()
