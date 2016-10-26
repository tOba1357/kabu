import sys
import glob
sys.path.append('gen-py')
from learning_service import LearningService

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import numpy as np

from KabuModel import KabuModel

class LearningHandler:
    def __init__(self):
        self.model = model = KabuModel()
        # model.load("weights.hdf5")

    def learn(self, input_data, targets, epoch_size, batch_size):
        input_data = np.array(input_data)
        targets = np.array(targets)
        self.model.learn(input_data, targets, epoch_size, batch_size)
        self.model.save("weights.hdf5")

    def predict(self, input_data):
        self.model.predict(input_data)


handler = LearningHandler()
processor = LearningService.Processor(handler)
transport = TSocket.TServerSocket(port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print "start server"
server.serve()
