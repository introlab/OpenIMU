from .BaseAlgorithm import BaseAlgorithmFactory
from .BaseAlgorithm import BaseAlgorithm
from libopenimu.models.sensor_types import SensorType
from libopenimu.db.DBManager import DBManager

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFormLayout, QSpinBox, QComboBox, QFrame, QSizePolicy

from libopenimu.qt.Charts import OpenIMUBarGraphView

# actual algorithm is here
from .freedson_adult_1998 import freedson_adult_1998


class FreedsonAdult1998(BaseAlgorithm):
    def __init__(self, params: dict):
        super().__init__(params)

    def configure(self, params: dict):
        print('FreedsonAdult1998.configure')
        super().configure(params)

    def calculate(self, manager: DBManager, recordsets: list):
        # print('FreedsonAdult1998.calculate')
        # print('Using recordsets', recordsets)

        results = []

        for record in recordsets:
            # Get all sensors in record
            sensors = manager.get_all_sensors(id_sensor_type=SensorType.ACCELEROMETER)

            for sensor in sensors:
                # print('Found Accelerometer')
                channels = manager.get_all_channels(sensor=sensor)
                # print('Found channels: ', channels)
                for channel in channels:
                    if channel.label == 'Accelerometer_Y':
                        # print('Processing Channel :', channel)
                        # Will get all data (converted to floats)
                        channel_data = manager.get_all_sensor_data(recordset=record, convert=True, sensor=sensor,
                                                                   channel=channel)
                        if len(channel_data) > 0:
                            # Process all sensor data
                            result = {'id_recordset': record.id_recordset,
                                      'result_name': record.name + ' (' + sensor.location + '/' + sensor.name + ')',
                                      'id_sensor': sensor.id_sensor, 'result':
                                          freedson_adult_1998(self.params, channel_data, sensor.sampling_rate)}
                            results.append(result)

        # Return an array with results for each recordset
        return results


class FreedsonAdult1998Factory(BaseAlgorithmFactory):
    config_preset_input = QComboBox
    config_sedentary_input = QSpinBox
    config_light_input = QSpinBox
    config_moderate_input = QSpinBox
    config_vigorous_input = QSpinBox

    def __init__(self):
        super().__init__()

    def create(self, params: dict):
        # Create instance of algorithm
        return FreedsonAdult1998(params)

    def params(self):
        return {'sedentary_cutoff': self.config_sedentary_input.value(),
                'light_cutoff': self.config_light_input.value(),
                'moderate_cutoff': self.config_moderate_input.value(),
                'vigorous_cutoff': self.config_vigorous_input.value()}

    def name(self):
        return 'Freedson Adult 1998'

    def unique_id(self):
        return 1

    def info(self):
        my_info = {'description': """ \
        It is a uniaxial accelerometer that assesses accelerations ranging from 0.05-2.0 G and is band limited with a 
        frequency response from 0.25-2.5 Hz.
                
        The acceleration signal is filtered by an analog bandpass filter and digitized by an 8 bit A/D converter at a 
        sampling rate of 10 samples per second.
        
        Each digitized signal is summed over a user specified time interval (epoch), and at the end of each epoch 
        the activity count is stored internally and the accumulator is reset to zero. In the current study, a 60-s
         epoch was used and activity counts were expressed as the average counts per minute over the 6 min of exercise. 
        
        
        Cut points (intensity buckets): 
        * https://actigraph.desk.com/customer/portal/articles/2515802
        
        Counts (accelerator sum over 60 s)
        * https://actigraph.desk.com/customer/portal/articles/2515580-What-are-counts-
        
        Notes:
        --> Only Y axis used on Actigraph devices.
        8 bits = 256 = 2g
        
        epoch = 60 seconds
                        
        """, 'name': self.name(), 'author': 'Dominic Létourneau', 'version': '0.1',
                   'reference': ("Freedson PS1, Melanson E, Sirard J., Calibration of the Computer Science and "
                                 "Applications, Inc. accelerometer., Med Sci Sports Exerc. 1998 May;30(5):777-81"),
                   'unique_id': self.unique_id()}

        return my_info

    def required_sensors(self):
        return [SensorType.ACCELEROMETER]

    def build_config_widget(self, parent_widget: QWidget, default_params: dict = None):
        # Initialize inputs
        self.config_preset_input = QComboBox()
        # self.config_preset_input.addItem('')
        self.config_preset_input.addItem('Values from paper', [99, 1951, 5724, 9498])
        # self.config_preset_input.addItem('Child', [99, 573, 1002, 0])
        self.config_preset_input.currentIndexChanged.connect(self.config_preset_changed)

        base_layout = QVBoxLayout()
        preset_frame = QFrame()
        preset_frame.setStyleSheet('QFrame{background-color: rgba(200,200,200,50%);}'
                                   'QLabel{background-color: rgba(0,0,0,0%);}')
        preset_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        frame_layout = QFormLayout()
        frame_layout.addRow('Preset', self.config_preset_input)
        preset_frame.setLayout(frame_layout)
        base_layout.addWidget(preset_frame)

        layout = QFormLayout()
        self.config_sedentary_input = QSpinBox()
        self.config_sedentary_input.setRange(0, 15000)
        layout.addRow("Cut-off Sedentary", self.config_sedentary_input)
        self.config_light_input = QSpinBox()
        self.config_light_input.setRange(0, 15000)
        layout.addRow("Cut-off Light", self.config_light_input)
        self.config_moderate_input = QSpinBox()
        self.config_moderate_input.setRange(0, 15000)
        layout.addRow("Cut-off Moderate", self.config_moderate_input)
        self.config_vigorous_input = QSpinBox()
        self.config_vigorous_input.setRange(0, 15000)
        layout.addRow("Cut-off Vigorous", self.config_vigorous_input)
        base_layout.addLayout(layout)

        base_widget = QWidget(parent_widget)
        base_widget.setLayout(base_layout)

        # Set default values
        if default_params is None:
            self.config_preset_changed()
        else:
            self.config_sedentary_input = default_params['sedentary_cutoff']
            self.config_light_input = default_params['light_cutoff']
            self.config_moderate_input = default_params['moderate_cutoff']
            self.config_vigorous_input = default_params['vigorous_cutoff']

        return base_widget

    def config_preset_changed(self):
        params = self.config_preset_input.currentData()
        if params is not None and len(params) == 4:
            self.config_sedentary_input.setValue(params[0])
            self.config_light_input.setValue(params[1])
            self.config_moderate_input.setValue(params[2])
            self.config_vigorous_input.setValue(params[3])

    def build_display_widget(self, parent_widget: QWidget, results, recordsets):

        layout = QVBoxLayout()
        # Add Scroll area
        scroll = QScrollArea(parent=parent_widget)

        scroll.setLayout(layout)
        view = OpenIMUBarGraphView(scroll)
        view.set_title('Active minutes')
        layout.addWidget(view)

        for result in results:
            data = result['result']
            view.set_category_axis(data.keys())
            values = []

            for key in data:
                values.append(data[key])

            label = result['result_name']
            view.add_set(label, values)

        # if len(results) == len(recordsets):
        #     for i, _ in enumerate(results):
        #         view.set_category_axis(results[i].keys())
        #         values = []
        #
        #         for key in results[i]:
        #             values.append(results[i][key])
        #
        #         label = recordsets[i].name
        #         view.add_set(label, values)

        # Update view
        view.update()

        return scroll


# Factory init
def init():
    return BaseAlgorithmFactory.register_factory(FreedsonAdult1998Factory())



