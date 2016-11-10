import tensorflow as tf

def data_type():
    return tf.float32


class KabuModelV2:
    def __init__(self, training, config):
        self.batch_size = batch_size = config.batch_size
        self.sequence_length = sequence_length = config.sequence_length
        #todo: available hiddne_size list
        size = config.hidden_size

        self._input_data = inputs = tf.placeholder(data_type(), [batch_size, sequence_length, config.input_output_size], name="input_data")
        self._labels = labels = tf.placeholder(tf.int32, [batch_size, sequence_length], name="labels")

        lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(size, forget_bias=0.0)
        if training:
            lstm_cell = tf.nn.rnn_cell.DropoutWrapper(lstm_cell, output_keep_prob=1.0 - config.dropout_rate)
        cell = tf.nn.rnn_cell.MultiRNNCell([lstm_cell] * config.num_layers, state_is_tuple=True)

        self._initial_state = cell.zero_state(batch_size, dtype=data_type())

        # inputs = [tf.squeeze(input_, [1])
        #           for input_ in tf.split(1, config.sequence_length, inputs)]
        outputs, state = tf.nn.dynamic_rnn(cell, inputs, [sequence_length] * batch_size, self._initial_state,
                                           parallel_iterations=1, swap_memory=True)
        outputs_flat = tf.reshape(outputs, [-1, size])
        logits_flat = tf.contrib.layers.linear(outputs_flat, config.input_output_size)

        if training:
            labels_flat = tf.reshape(labels, [-1])
            softmax_cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits_flat, labels_flat)
            self._loss = loss = tf.reduce_mean(softmax_cross_entropy)

            self._step = global_step = tf.Variable(0, trainable=False, name='global_step')

            self._learning_rate = learning_rate = tf.train.exponential_decay(
                config.initial_learning_rate, global_step, config.decay_steps,
                config.decay_rate, staircase=True, name='learning_rate')
            opt = tf.train.AdamOptimizer(learning_rate)
            params = tf.trainable_variables()
            gradients = tf.gradients(loss, params)
            clipped_gradients, _ = tf.clip_by_global_norm(gradients, config.clip_norm)
            self._train_optimizer = opt.apply_gradients(zip(clipped_gradients, params), global_step)
            self._summaries = tf.merge_summary([
                tf.scalar_summary('loss', loss),
                tf.scalar_summary('learning_rate', learning_rate)
            ])

    @property
    def input_data(self):
        return self._input_data

    @property
    def labels(self):
        return self._labels

    @property
    def initial_state(self):
        return self._initial_state

    @property
    def loss(self):
        return self._loss

    @property
    def step(self):
        return self._step

    @property
    def learning_rate(self):
        return self._learning_rate

    @property
    def train_optimizer(self):
        return self._train_optimizer

    @property
    def summaries(self):
        return self._summaries
