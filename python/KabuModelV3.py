import tensorflow as tf

def data_type():
    return tf.float32


class KabuModelV3:
    def __init__(self, input_, mode, config):
        self.batch_size = batch_size = config.batch_size
        self.sequence_length = sequence_length = config.sequence_length
        #todo: available hiddne_size list
        size = config.hidden_size
        summaries = []

        lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(size, forget_bias=0.0)
        if mode == "train":
            lstm_cell = tf.nn.rnn_cell.DropoutWrapper(lstm_cell, output_keep_prob=1.0 - config.dropout_rate)
        cell = tf.nn.rnn_cell.MultiRNNCell([lstm_cell] * config.num_layers, state_is_tuple=True)

        self._initial_state = cell.zero_state(batch_size, dtype=data_type())

        input_data, labels = input_
        input_data = tf.to_float(input_data)
        input_data = tf.reshape(input_data, [config.batch_size, config.sequence_length, 1])
        outputs, state = tf.nn.dynamic_rnn(cell, input_data, [sequence_length] * batch_size, self._initial_state,
                                           parallel_iterations=1, swap_memory=True)
        outputs_flat = tf.reshape(outputs, [-1, size])
        softmax_w = tf.get_variable(
            "softmax_w", [size, 1], dtype=data_type())
        softmax_b = tf.get_variable("softmax_b", [1], dtype=data_type())
        logits = tf.matmul(outputs_flat, softmax_w) + softmax_b

        if mode == "train" or mode == "eval":
            labels_flat = tf.reshape(labels, [-1, 1])
            # cross_entropy = tf.reduce_mean(-tf.reduce_sum(labels_flat * tf.log(logits), reduction_indices=[1]))
            self._loss = loss =  tf.reduce_mean(tf.square(labels_flat - logits))
            summaries.append(tf.scalar_summary('loss', loss))

            if mode == "train":
                self._step = global_step = tf.Variable(0, trainable=False, name='global_step')

                self._learning_rate = learning_rate = tf.train.exponential_decay(
                    config.initial_learning_rate, global_step, config.decay_steps,
                    config.decay_rate, staircase=True, name='learning_rate')
                opt = tf.train.AdamOptimizer(learning_rate)
                params = tf.trainable_variables()
                gradients = tf.gradients(loss, params)
                clipped_gradients, _ = tf.clip_by_global_norm(gradients, config.clip_norm)
                self._train_optimizer = opt.apply_gradients(zip(clipped_gradients, params), global_step)
                summaries.append(tf.scalar_summary('learning_rate', learning_rate))
        self._summaries = tf.merge_summary(summaries)

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