import tensorflow as tf
import MySQLdb

flags = tf.flags
flags.DEFINE_string("filename", None,
                    "TFRecord output path")
FLAGS = flags.FLAGS




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
    # input_data = [get_change_rate_period_index(change_rate[0]) for change_rate in result[:-1]]
    # labels = [get_change_rate_period_index(change_rate[0]) for change_rate in result[1:]]
    input_data = [change_rate[0] for change_rate in result[:-1]]
    labels = [change_rate[0] for change_rate in result[1:]]
    return input_data, labels

def make_example(company_id, from_, size):
    input_data, labels = get_train_data(company_id, from_, size)
    if input_data is None or labels is None: return None

    ex = tf.train.SequenceExample()
    fl_input_data = ex.feature_lists.feature_list["input_data"]
    fl_labels = ex.feature_lists.feature_list["labels"]
    for input_data, label in zip(input_data, labels):
        fl_input_data.feature.add().float_list.value.append(input_data)
        fl_labels.feature.add().float_list.value.append(label)
    return ex


with MySQLdb.connect(db='kabudb', user='root', passwd='root') as cursor:
    cursor.execute("SELECT count(*) FROM tblcompanies")
    company_num = cursor.fetchall()[0][0]
    with tf.python_io.TFRecordWriter('/home/tatsuya/workspace/resaerch/kabu/python/traindata/normal/train') as writer:
        for init_from in range(1, 100, 25):
            print str(init_from)
            for company_id in range(1, company_num + 1):
                if company_id % 10 == 0: continue
                from_ = init_from
                while True:
                    example = make_example(company_id, from_, 100)
                    if example is None:break
                    writer.write(example.SerializeToString())
                    from_ += 100

    with tf.python_io.TFRecordWriter('/home/tatsuya/workspace/resaerch/kabu/python/traindata/normal/test') as writer:
        for init_from in range(1, 100, 25):
            for company_id in range(10, company_num + 1, 10):
                print str(company_id)
                from_ = init_from
                while True:
                    example = make_example(company_id, from_, 100)
                    if example is None: break
                    writer.write(example.SerializeToString())
                    from_ += 100

