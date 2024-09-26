import nidaqmx
from nidaqmx.constants import (AcquisitionType, CountDirection, Edge, READ_ALL_AVAILABLE, TaskMode, TriggerType)
import numpy as np
import time

system = nidaqmx.system.System.local()
DAQ_device = system.devices['Dev1']
print([ao.name for ao in DAQ_device.ao_physical_chans])


# with nidaqmx.Task() as samp_clk_task:
#     samp_clk_task.di_channels.add_di_chan('Dev1/SampleClock')
#     sampling_rate = 1000
#     samp_clk_task.timing.cfg_samp_clk_timing(sampling_rate, sample_mode=AcquisitionType.CONTINUOUS)
#     samp_clk_task.control(TaskMode.TASK_COMMIT)

with nidaqmx.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
    
    # Set the gain property to scale the output voltage
    task.ao_channels[0].ai_max = 0  # Set the maximum voltage range to 0.5 V
    task.start()
    task.ao_channels[0].ao_gain = 0
    sample_rate = 3e5
    num_samples = 1000
    # Configure timing using the onboard clock
    # task.timing.cfg_samp_clk_timing(
    #     rate=rate,  # Set the desired sampling rate (1 kHz in this example)
    #     sample_mode=AcquisitionType.CONTINUOUS,
    #     source='Dev1/OnboardReferenceClock'  # Use onboard clock
    # )

    
    
    # Generate a sine wave with frequency  kHz and amplitude  V
    for _ in range(num_samples):
        task.write([0.2])
        time.sleep(1 / sample_rate)  # Sleep to control the sample rate
    
    # Stop the task
    task.stop()