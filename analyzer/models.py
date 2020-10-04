from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model

class MonopolyModel(Model):
    def __init__(self, layer1_node: int, layer2_node: int, output_node: int):
        super(MonopolyModel, self).__init__()
        self.conv1 = Conv2D(16, 1, activation='elu')
        self.flatten = Flatten()
        self.d1 = Dense(layer1_node, activation='elu')
        self.d2 = Dense(layer2_node, activation='elu')
        self.d3 = Dense(output_node)

    def call(self, x):
        x = self.conv1(x)
        x = self.flatten(x)
        x = self.d1(x)
        x = self.d2(x)
        return self.d3(x)
