import MySQLdb
import tensorflow as tf
from KabuModelV2 import KabuModelV2

# +---------------------+-----------------------+
# | stddev(change_rate) | avg(change_rate)      |
# +---------------------+-----------------------+
# | 0.06494733817591199 | 0.0005248532996038034 |
# +---------------------+-----------------------+
#


flags = tf.flags
flags.DEFINE_string("save_path", None,
                    "Model output directory.")

flags.DEFINE_string("log_dir", None,
                    "logging directory")

FLAGS = flags.FLAGS


class Config:
    hidden_size = 100
    sequence_length = 100
    num_layers = 3
    batch_size = 128
    input_output_size = 100
    dropout_rate = 0.1
    initial_learning_rate = 0.01
    decay_steps = 1000
    decay_rate = 0.97
    clip_norm = 3
    init_scale = 0.1


change_rate_period = [-0.32421183758,
                      -0.151451918032,
                      -0.133266663343,
                      -0.122225615853,
                      -0.11378246189,
                      -0.106638254691,
                      -0.100792994255,
                      -0.0962466805825,
                      -0.0917003669102,
                      -0.0871540532379,
                      -0.0832572129473,
                      -0.0800098460385,
                      -0.0767624791297,
                      -0.0735151122209,
                      -0.0702677453121,
                      -0.0676698517851,
                      -0.0644224848763,
                      -0.0618245913493,
                      -0.059876171204,
                      -0.057278277677,
                      -0.0546803841499,
                      -0.0527319640046,
                      -0.0501340704776,
                      -0.0481856503323,
                      -0.0462372301871,
                      -0.04363933666,
                      -0.0416909165147,
                      -0.0397424963695,
                      -0.0377940762242,
                      -0.0358456560789,
                      -0.0338972359336,
                      -0.0325982891701,
                      -0.0306498690248,
                      -0.0287014488796,
                      -0.0267530287343,
                      -0.0254540819708,
                      -0.0235056618255,
                      -0.0215572416802,
                      -0.0202582949167,
                      -0.0183098747714,
                      -0.0163614546261,
                      -0.0150625078626,
                      -0.0131140877173,
                      -0.0118151409538,
                      -0.00986672080854,
                      -0.00856777404502,
                      -0.00661935389975,
                      -0.00532040713623,
                      -0.00337198699095,
                      -0.00207304022743,
                      0.00312274682664,
                      0.00442169359016,
                      0.00637011373544,
                      0.00766906049895,
                      0.00961748064423,
                      0.0109164274077,
                      0.012864847553,
                      0.0141637943165,
                      0.0161122144618,
                      0.0174111612253,
                      0.0193595813706,
                      0.0213080015159,
                      0.0226069482794,
                      0.0245553684247,
                      0.02650378857,
                      0.0278027353335,
                      0.0297511554788,
                      0.031699575624,
                      0.0336479957693,
                      0.0349469425328,
                      0.0368953626781,
                      0.0388437828234,
                      0.0407922029687,
                      0.0427406231139,
                      0.0446890432592,
                      0.0472869367863,
                      0.0492353569315,
                      0.0511837770768,
                      0.0537816706039,
                      0.0557300907491,
                      0.0583279842762,
                      0.0609258778032,
                      0.0628742979485,
                      0.0654721914755,
                      0.0687195583843,
                      0.0713174519113,
                      0.0745648188201,
                      0.0778121857289,
                      0.0810595526377,
                      0.0843069195465,
                      0.0882037598371,
                      0.0927500735094,
                      0.0972963871817,
                      0.101842700854,
                      0.10768796129,
                      0.114832168489,
                      0.123275322452,
                      0.134316369942,
                      0.152501624631,
                      100]


def get_change_rate_period_index(change_rate):
    for i, period in enumerate(change_rate_period):
        if period > change_rate:
            return i
    return len(change_rate_period) - 1


def create_one_hot(index, size):
    return [int(i == index) for i in range(size)]


def create_one_hot_data(change_rate):
    return create_one_hot(get_change_rate_period_index(change_rate), len(change_rate_period))


def get_train_data(company_id, from_, size):
    row = cursor.execute("SELECT change_rate FROM tblvalues WHERE company_id = %d ORDER BY date LIMIT %d, %d" %
                         (company_id, from_, size + 1))
    if row != size + 1: return None, None
    result = cursor.fetchall()
    input_data = [create_one_hot_data(change_rate[0]) for change_rate in result[:-1]]
    labels = [get_change_rate_period_index(change_rate[0]) for change_rate in result[1:]]
    return input_data, labels


def train(model, company_num):
    company_id = 1
    from_ = 1
    saver = tf.train.Saver()
    with tf.Session() as session:
        session.run(tf.initialize_all_variables())
        summary_writer = tf.train.SummaryWriter(FLAGS.log_dir, session.graph)
        for epoch in range(3):
            while company_id < company_num:
                input_data = []
                labels = []
                while len(input_data) < config.batch_size:
                    (data, label) = get_train_data(company_id, from_, config.sequence_length)
                    if data is None:
                        # company_id % 10 == 0 is evaluation data.
                        from_ = 1
                        company_id += 1
                        if company_id % 10 == 0:
                            company_id += 1
                        if company_id >= company_num:
                            return
                        continue
                    input_data.append(data)
                    labels.append(label)
                    from_ += config.sequence_length
                fetches = [
                    model.step,
                    model.train_optimizer,
                    model.summaries,
                    model.learning_rate,
                    model.loss
                ]
                feed_dict = {model.input_data: input_data, model.labels: labels}
                (global_step, _, summaries, learning_rate, loss) = session.run(fetches, feed_dict)
                if global_step % 10 == 0:
                    saver.save(session, FLAGS.save_path)
                    summary_writer.add_summary(summaries, global_step=global_step)
                    tf.logging.info('Global Step: %d - '
                                    'Learning Rate: %.5f - '
                                    'Loss: %.3f - ',
                                    global_step, learning_rate, loss)


with MySQLdb.connect(db='kabudb', user='root', passwd='root') as cursor:
    cursor.execute("SELECT count(*) FROM tblcompanies")
    company_num = cursor.fetchall()[0][0]
    with tf.Graph().as_default():
        config = Config
        initializer = tf.random_uniform_initializer(-config.init_scale,
                                                    config.init_scale)
        with tf.name_scope("Train"):
            with tf.variable_scope("Model", initializer=initializer):
                model = KabuModelV2(True, config)
        train(model, company_num)
