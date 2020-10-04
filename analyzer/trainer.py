import tensorflow as tf
from analyzer.datageneration import generate_data
from analyzer.models import MonopolyModel
from monopoly.board import MonopolyBoard

PLAYER_COUNT = 4
GAMMA = 0.99
ASSETS_SCALE = 0.001

@tf.function
def train_step(model: MonopolyModel, loss_object, optimizer, train_loss, images, labels):
    with tf.GradientTape() as tape:
        predictions = model(images, training=True)
        loss = loss_object(labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    train_loss(loss)
    return predictions

@tf.function
def test_step(model: MonopolyModel, loss_object, test_loss, images, labels):
    predictions = model(images, training=False)
    t_loss = loss_object(labels, predictions)
    test_loss(t_loss)
    return predictions

@tf.function
def get_data(model: MonopolyModel, actuals, inputs, gamma):
    predictions = model(inputs, training=False)
    answers = tf.add(actuals, tf.multiply(predictions, gamma))
    return answers

class MonopolyAITrainer:
    def __init__(self, model, loss_object, optimizer, train_loss, test_loss):
        self.model = model
        self.loss_object = loss_object
        self.optimizer = optimizer
        self.train_loss = train_loss
        self.test_loss = test_loss
        self.gamma = tf.constant(GAMMA, dtype="float32")

        self.board_data = MonopolyBoard(PLAYER_COUNT)
        return

    def reset(self):
        self.train_loss.reset_states()
        self.test_loss.reset_states()

    def train(self, datasize: int):
        asset_matrix, board_before_matrix, board_after_matrix = generate_data(self.board_data, datasize, ASSETS_SCALE)
        actuals = tf.constant(asset_matrix, dtype="float32")
        inputs1 = tf.constant(board_before_matrix, dtype="float32")
        inputs2 = tf.constant(board_after_matrix, dtype="float32")
        train_step(self.model, self.loss_object, self.optimizer, self.train_loss, inputs1, get_data(self.model, actuals, inputs2, self.gamma))

    def test(self, datasize: int):
        asset_matrix, board_before_matrix, board_after_matrix = generate_data(self.board_data, datasize, ASSETS_SCALE)
        actuals = tf.constant(asset_matrix, dtype="float32")
        inputs1 = tf.constant(board_before_matrix, dtype="float32")
        inputs2 = tf.constant(board_after_matrix, dtype="float32")
        test_step(self.model, self.loss_object, self.test_loss, inputs1, get_data(self.model, actuals, inputs2, self.gamma))
