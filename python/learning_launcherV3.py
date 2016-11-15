import tensorflow as tf
from KabuModelV3 import KabuModelV3

flags = tf.flags
flags.DEFINE_string("datadir", None,
                    "input file name")

flags.DEFINE_string("logdir", None,
                    "logging directory")

FLAGS = flags.FLAGS


class Config:
    hidden_size = 100
    sequence_length = 100
    num_layers = 3
    batch_size = 128
    dropout_rate = 0.1
    initial_learning_rate = 0.1
    decay_steps = 1000
    decay_rate = 0.97
    clip_norm = 3
    init_scale = 0.1


def train(model):
    saver = tf.train.Saver()
    sv = tf.train.Supervisor(logdir=FLAGS.logdir, summary_op=model.summaries, saver=saver, global_step=model.step,
                             save_summaries_secs=3)
    with sv.managed_session() as session:
        fetches = [
            model.step,
            model.train_optimizer,
            model.summaries,
            model.learning_rate,
            model.loss
        ]
        for epoch in range(100000):
            if sv.should_stop():
                return
            (global_step, _, summaries, learning_rate, loss) = session.run(fetches)
            if global_step % 100 == 0:
                print 'Global Step: %d - Learning Rate: %.5f - Loss: %.3f - ' % (global_step, learning_rate, loss)


def eval(model):
    with tf.Session() as session:
        loss = session.run(model.loss)
        print str(loss)


def get_padded_batch(file_name, batch_size,
                     num_enqueuing_threads=4):
    file_queue = tf.train.string_input_producer([file_name])
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(file_queue)

    sequence_features = {
        'input_data': tf.FixedLenSequenceFeature(shape=[],
                                                 dtype=tf.float32),
        'labels': tf.FixedLenSequenceFeature(shape=[],
                                             dtype=tf.float32)}

    _, sequence = tf.parse_single_sequence_example(
        serialized_example, sequence_features=sequence_features)

    queue = tf.PaddingFIFOQueue(
        capacity=1000,
        dtypes=[tf.float32, tf.float32],
        shapes=[(config.sequence_length,), (config.sequence_length,)])

    enqueue_ops = [queue.enqueue([sequence['input_data'],
                                  sequence['labels']])] * num_enqueuing_threads
    tf.train.add_queue_runner(tf.train.QueueRunner(queue, enqueue_ops))
    return queue.dequeue_many(batch_size)


with tf.Graph().as_default():
    config = Config
    initializer = tf.random_uniform_initializer(-config.init_scale,
                                                config.init_scale)
    input = get_padded_batch(FLAGS.datadir + "/train", config.batch_size)
    eval_input = get_padded_batch(FLAGS.datadir + "/test", config.batch_size)
    with tf.name_scope("Train"):
        with tf.variable_scope("Model", initializer=initializer):
            model = KabuModelV3(input, "train", config)
    with tf.name_scope("Eval"):
        with tf.variable_scope("Model", reuse=True):
            eval_model = KabuModelV3(eval_input, "eval", config)
    train(model)