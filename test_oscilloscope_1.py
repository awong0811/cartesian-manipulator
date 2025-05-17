from src.agilent54624A import Agilent54624A
from src.utils import *


# Set up oscilloscope
oscilloscope = Agilent54624A(port='COM1')
oscilloscope.connect()
oscilloscope.checkOperational()
datapoints_tx = oscilloscope.collect_datapoints('tx')
datapoints_rx = oscilloscope.collect_datapoints('rx')

output_file = 'data/20250517_experiment_1.xlsx'
datapoints = np.vstack([np.array(datapoints_tx), np.array(datapoints_rx)]).T
columns = [f"{'TX' if i % 2 == 0 else 'RX'}{i // 2 + 1}" for i in range(datapoints.shape[1])]
save_data(output_file, columns=columns, datapoints=datapoints)
oscilloscope.disconnect()