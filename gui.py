import sys
import random
import tempfile
from time import sleep
from datetime import datetime, timedelta

from pymeasure.experiment import Procedure, IntegerParameter, Parameter, FloatParameter
from pymeasure.experiment import Results
from pymeasure.display.Qt import QtWidgets, fromUi
from pymeasure.display.windows import ManagedWindow
from agilent54624A import Agilent54624A

import logging
log = logging.getLogger('')
log.addHandler(logging.NullHandler())

#=============================== Tasks ================================= 
# 1. Connect to oscilloscope. User needs to be able to select channel, set the mode of the received data, and retrieve the data.
# 2. (Future) Incorporate a python script that uses PySerial to send serial commands to the Arduino so user does everything in the GUI.
#=======================================================================

class ExperimentProcedure(Procedure):
    collectionRows = IntegerParameter('Number of rows in collection grid', default=10)
    collectionCols = IntegerParameter('Number of columns in collection grid', default=10)
    collectionRowSep = FloatParameter('Distance between rows in grid (cm)', default=1.0)
    collectionColSep = FloatParameter('Distance between columns in grid (cm)', default=1.0)

    startX = FloatParameter('Starting point of the grid rows (cm)', default=0.0)
    startY = FloatParameter('Starting point of the grid columns (cm)', default=0.0)

    datapoints = IntegerParameter('Number of Datapoints', default=1999) #number of datapoints received from oscope, currently not modifiable by user
    channel = IntegerParameter('Oscilloscope Channel', default=1)
    mode = Parameter('Mode', default="WORD")
    instrument = None

    DATA_COLUMNS = ['Datapoints', 'Voltage', 'X', 'Y']

    def startup(self):
        log.info("Checking connection to oscilloscope")
        self.instrument.checkOperational()
    
    #===========================Collect data from oscilloscope======================#
    def execute(self):
        collectionRowRange = range(self.collectionRows)
        collectionColRange = range(self.collectionCols)

        totalPoints = self.collectionRows * self.collectionCols

        currentPoints = 0

        for col in collectionColRange:
            for row in collectionRowRange:
                log.info("Moving to datapoint location")
                x = row * self.collectionColSep + self.startX
                y = col * self.collectionRowSep + self.startY

                self.moveTo(x, y)
        
                log.info("Starting to collect data from oscilloscope")
                response = self.instrument.retrieve_data()

                for i in range(self.datapoints):
                    data = {
                        'X': x,
                        'Y': y,
                        'Datapoints': i,
                        'Voltage': response[i]
                    }
                    self.emit('results', data)
                    
                currentPoints = currentPoints + 1
                self.emit('progress', 100 * currentPoints / totalPoints)

                if self.should_stop():
                    log.warning("Caught the stop flag in the procedure")
                    break

            if self.should_stop():
                break
    #===============================================================================#

    #===============================Arduino=========================================#
    def moveTo(self, x, y):
        log.info(f"MOVING TO ({x}, {y})")
        pass
    #===============================================================================#
        
    def shutdown(self):
        log.info("Finished")

    
    def get_estimates(self, sequence_length=None, sequence=None):

        points = int(self.collectionCols * self.collectionRows)
        duration = timedelta(seconds=points * 9)

        durStr = str(duration).split('.', 2)[0]
        if durStr[:2] == '0:':
            durStr = durStr[2:]

        estimates = [
            ("Duration", durStr),
            ("Number of points", "%d" % points),
            ('Measurement finished at', (datetime.now() + duration).strftime('%I:%M %p')),
        ]

        return estimates


class MainWindow(ManagedWindow):

    def __init__(self):
        super().__init__(
            procedure_class=ExperimentProcedure,
            inputs=['datapoints', 'channel', 'mode', 'collectionRows', 'collectionCols', 'collectionRowSep', 'collectionColSep', 'startX', 'startY'],
            displays=['datapoints', 'channel', 'mode', 'collectionRows', 'collectionCols', 'collectionRowSep', 'collectionColSep', 'startX', 'startY'],
            x_axis='Datapoints',
            y_axis='Voltage'
        )
        self.setWindowTitle('NDE GUI slay')
        self.instrument = Agilent54624A(port='COM1')
        self.instrument.connect()
        # self.instrument.checkOperational()

    def _setup_ui(self):
        super()._setup_ui()
        # self.inputs.hide()
        # self.inputs = fromUi('gui.ui')

    def queue(self):
        filename = tempfile.mktemp()

        procedure = ExperimentProcedure()
        procedure.datapoints = self.inputs.datapoints.value()
        
        channel = self.inputs.channel.value()
        self.instrument.select_channel(channel)
        log.info(f"Connected to Channel {channel}")
        
        mode = self.inputs.mode.text()
        self.instrument.set_waveform_type(mode)
        logstring = "Waveform type set to " + mode
        log.info(logstring)

        procedure.instrument = self.instrument

        results = Results(procedure, filename)

        experiment = self.new_experiment(results)

        self.manager.queue(experiment)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())