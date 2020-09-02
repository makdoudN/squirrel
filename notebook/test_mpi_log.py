import numpy as np
import pandas as pd
import ml_record
import random
import time

from ml_record.utils import proc_id
rec = ml_record.MPI_Recorder(f'mpi-outputs-{proc_id()}')

for t in range(100):
    score = random.random()
    rec.store({'score': score})
    rec.summary()
    time.sleep(0.05)


