import numpy as np

from KabuModel import KabuModel

model = KabuModel()
model.load("weights.hdf5")
input_data = np.array([[[i] for i in range(100)]])
print (model.predict(input_data))


