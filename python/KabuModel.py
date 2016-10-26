from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.optimizers import Adam, SGD, RMSprop


class Config:
    hidden_size = 1000
    num_layers = 3
    batch_size = 50
    input_size = 1
    output_size = 1
    dropout_rate = 0.1


class KabuModel:
    def __init__(self, config=Config, training=True):
        self._model = model = Sequential()
        if training:
            if config.num_layers == 1:
                model.add(LSTM(config.hidden_size, batch_input_shape=(None, config.batch_size, config.input_size),
                               dropout_U=config.dropout_rate, unroll=True, stateful=True))
            else:
                model.add(LSTM(config.hidden_size, batch_input_shape=(None, config.batch_size, config.input_size),
                               return_sequences=True, activation="relu", unroll=True))
                for i in range(config.num_layers - 2):
                    model.add(LSTM(config.hidden_size, activation="relu", return_sequences=True, unroll=True))
                model.add(LSTM(config.hidden_size, activation="relu", unroll=True))
        else:
            if config.num_layers == 1:
                model.add(LSTM(config.hidden_size, batch_input_shape=(None, config.batch_size, config.input_size)))
            else:
                model.add(LSTM(config.hidden_size, batch_input_shape=(None, config.batch_size, config.input_size),
                               return_sequences=True))
                for i in range(config.num_layers - 2):
                    model.add(LSTM(config.hidden_size, return_sequences=True))
                model.add(LSTM(config.hidden_size))
        model.add(Dense(1))
        model.add(Activation("relu"))
        model.compile(Adam(), loss="mean_squared_error")

    @property
    def model(self):
        return self._model

    def learn(self, input_data, targets, epoch_size, batch_size):
        self._model.fit(input_data, targets, batch_size=batch_size, nb_epoch=epoch_size)

    def save(self, file_name):
        self._model.save_weights(file_name)

    def load(self, file_name):
        self._model.load_weights(file_name)

    def predict(self, input_data):
        return self._model.predict(input_data)
