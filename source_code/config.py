my_id = ''
server_id = ''

matt_server_address = 'ws://150.65.230.93:5580/ws'
el_mqtt_address = '150.65.231.106'
el_mqtt_port = 7883

dict_mdev_name_value = None

el_mqtt_topic_create = 'create'
el_mqtt_topic_delete = 'delete'
el_mqtt_topic_update = 'update'
el_mqtt_topic_operate = 'operate'
el_mqtt_topic_result = 'result'

mqtt_pub_client_name = 'matter-conver-pub'
mqtt_sub_client_name = 'matter-conver-sub'


# cluster_id: {attribute_id: el_name}
# m2e_cluster_name_pair = {
#     # 3 : Identify ,
#     # 4 : Groups ,
#     6: {#OnOff
#         0: 'operationStatus', 
#     },
#     # 7: OnOffSwitchConfiguration ,
#     8: {#LevelControl
#         0: 'lightLevel',
#         3: 'lightLevelStep',
#     },
#     # 15: BinaryInputBasic ,
#     # 28: PulseWidthModulation ,
#     # 29 : Descriptor ,
#     # 30 : Binding ,
#     # 31 : AccessControl ,
#     # 37 : Actions ,
#     # 40 : BasicInformation ,
#     # 41 : OtaSoftwareUpdateProvider ,
#     # 42 : OtaSoftwareUpdateRequestor ,
#     # 43 : LocalizationConfiguration ,
#     # 44 : TimeFormatLocalization ,
#     # 45 : UnitLocalization ,
#     # 46 : PowerSourceConfiguration ,
#     # 47 : PowerSource ,
#     # 48 : GeneralCommissioning ,
#     # 49 : NetworkCommissioning ,
#     # 50 : DiagnosticLogs ,
#     # 51 : GeneralDiagnostics ,
#     # 52 : SoftwareDiagnostics ,
#     # 53 : ThreadNetworkDiagnostics ,
#     # 54 : WiFiNetworkDiagnostics ,
#     # 55 : EthernetNetworkDiagnostics ,
#     # 56 : TimeSynchronization ,
#     # 57 : BridgedDeviceBasicInformation ,
#     # 59 : Switch ,
#     # 60 : AdministratorCommissioning ,
#     # 62 : OperationalCredentials ,
#     # 63 : GroupKeyManagement ,
#     # 64 : FixedLabel ,
#     # 65 : UserLabel ,
#     # 66 : ProxyConfiguration ,
#     # 67 : ProxyDiscovery ,
#     # 68 : ProxyValid ,
#     69 : {#BooleanState
#         0: 'openingDetectionStatus2', 
#     },
#     # 70 : IcdManagement ,
#     # 71 : Timer ,
#     # 72 : OvenCavityOperationalState ,
#     # 73 : OvenMode ,
#     # 74 : LaundryDryerControls ,
#     # 80 : ModeSelect ,
#     # 81 : LaundryWasherMode ,
#     # 82 : RefrigeratorAndTemperatureControlledCabinetMode ,
#     # 83 : LaundryWasherControls ,
#     # 84 : RvcRunMode ,
#     # 85 : RvcCleanMode ,
#     # 86 : TemperatureControl ,
#     # 87 : RefrigeratorAlarm ,
#     # 89 : DishwasherMode ,
#     # 91 : AirQuality ,
#     # 92 : SmokeCoAlarm ,
#     # 93 : DishwasherAlarm ,
#     # 94 : MicrowaveOvenMode ,
#     # 95 : MicrowaveOvenControl ,
#     # 96 : OperationalState ,
#     # 97 : RvcOperationalState ,
#     # 98 : ScenesManagement ,
#     # 113 : HepaFilterMonitoring ,
#     # 114 : ActivatedCarbonFilterMonitoring ,
#     # 128 : BooleanStateConfiguration ,
#     # 129 : ValveConfigurationAndControl ,
#     # 144 : ElectricalPowerMeasurement ,
#     # 145 : ElectricalEnergyMeasurement ,
#     # 150 : DemandResponseLoadControl ,
#     # 151 : Messages ,
#     # 152 : DeviceEnergyManagement ,
#     # 153 : EnergyEvse ,
#     # 155 : EnergyPreference ,
#     # 156 : PowerTopology ,
#     # 157 : EnergyEvseMode ,
#     # 159 : DeviceEnergyManagementMode ,
#     257: {#DoorLock
        
#     },
#     # 258 : WindowCovering ,
#     # 259 : BarrierControl ,
#     # 512 : PumpConfigurationAndControl ,
#     # 513: {#Thermostat
        
#     # },
#     # 514 : FanControl ,
#     # 516 : ThermostatUserInterfaceConfiguration ,
#     768: {#ColorControl ,
#         0: 'rgb',
#         1: 'rgb',
#     },
#     # 769 : BallastConfiguration ,
#     1024: {#IlluminanceMeasurement
#         0: 'valueInLux',
#     },
#     1026: {#TemperatureMeasurement
#         0: 'value',
#     },
#     # 1027 : PressureMeasurement ,
#     # 1028 : FlowMeasurement ,
#     1029: {#RelativeHumidityMeasurement
#         0: 'value',
#     },
#     1030: {#OccupancySensing
#         0: 'detection',
#     },
#     # 1036 : CarbonMonoxideConcentrationMeasurement ,
#     # 1037 : CarbonDioxideConcentrationMeasurement ,
#     # 1043 : NitrogenDioxideConcentrationMeasurement ,
#     # 1045 : OzoneConcentrationMeasurement ,
#     # 1066 : Pm25ConcentrationMeasurement ,
#     # 1067 : FormaldehydeConcentrationMeasurement ,
#     # 1068 : Pm1ConcentrationMeasurement ,
#     # 1069 : Pm10ConcentrationMeasurement ,
#     # 1070 : TotalVolatileOrganicCompoundsConcentrationMeasurement ,
#     # 1071 : RadonConcentrationMeasurement ,
#     # 1283 : WakeOnLan ,
#     # 1284 : Channel ,
#     # 1285 : TargetNavigator ,
#     # 1286 : MediaPlayback ,
#     # 1287 : MediaInput ,
#     # 1288 : LowPower ,
#     # 1289 : KeypadInput ,
#     # 1290 : ContentLauncher ,
#     # 1291 : AudioOutput ,
#     # 1292 : ApplicationLauncher ,
#     # 1293 : ApplicationBasic ,
#     # 1294 : AccountLogin ,
#     # 1295 : ContentControl ,
#     # 1296 : ContentAppObserver ,
#     # 2820 : ElectricalMeasurement ,
#     # 4294048773 : UnitTesting ,
#     # 4294048774 : FaultInjection ,
#     # 4294048800 : SampleMei ,
# }


cluster_skip_list = [
    3, # identify
    4, # groups
    5, # unknow in tapo
    29, # desctiptor
    57, # bridge device basic information
]


device_type_skip_list = [
    14, # 0x000e -> MA-aggregator
    17, # 0x0011 -> MA-powersource
    18, # 0x0012 -> MA-otarequestor
    19, # 0x0013 -> MA-bridgeddebice
    20, # 0x0014 -> MA-otaprovider
]


# matter_device_type_value: echonet_dd_file_name
matter_el_pair = {
    10: 'electricLock',# 0x000A -> Door Lock
    11: 'controller',# 0x000B -> Door Lock Controller
    15: 'controller',# 0x000F -> eneric Switch
    
    21: 'openCloseSensor',# 0x0015 -> Contact Sensor
    
    # ? # 0x002B -> Fan
    # ?# 0x002C -> Air Quality Sensor
    45: 'airCleaner',# 0x002D -> Air Purifier    
    
    112: 'refrigerator',# 0x0070 -> Refrigerator
    113: 'refrigerator',# 0x0071 -> Temperature Controlled Cabinet
    114: 'homeAirConditioner',# 0x0072 -> Room Air Conditioner
    115: 'washerDryer',# 0x0073 -> Laundry Washer
    # ? # 0x0074 -> Robotic Vacuum Cleaner
    # ? # 0x0075 -> deviceDishWasher
    # ? # 0x0076 -> Smoke CO Alarm
    
    256: 'generalLighting', # 0x0100 -> On/Off Light
    257: 'generalLighting', # 0x0101 -> Dimmable Light
    
    259: 'controller',# 0x0103 -> On/Off Light Switch
    260: 'controller',# 0x0104 -> Dimmer Switch
    261: 'controller',# 0x0105 -> Color Dimmer Switch
    262: 'illuminanceSensor',# 0x0106 -> Light Sensor
    263: 'humanDetectionSensor',# 0x0107 -> Occupancy Sensor
    
    266: 'switch',# 0x010A -> On/Off Plug-in Unit
    267: 'switch',# 0x010B -> Dimmable Plug-In Unit
    268: 'generalLighting', # 0x010C -> Color Temperature Light
    269: 'generalLighting', # 0x010D -> Extended Color Light
    
    # ? # 0x0202 -> Window Covering
    515: 'controller',# 0x0203 -> Window Covering Controller
    
    # temperatureSensor ? # 768: 'temperatureSensor',# 0x0300 -> Heating/Cooling Unit 
    769: 'homeAirConditioner',# 0x0301 -> Thermostat
    770: 'temperatureSensor', # 0x0302 -> Temperature sensor
    
    772: 'controller',# 0x0304 -> Pump Controller
    # ? # 0x0305 -> Pressure Sensor
    774: 'waterFlowMeter',# 0x0306 -> Flow Sensor
    775: 'humiditySensor',# 0x0307 -> Humidity Sensor
    
    # ? # 19000 -> Switch bot's special device type
    2112: 'controller',# 0x0840 -> Control Bridge
    
}


# matter_cluster_type_name_pair = {
#     0: 'UNKNOWN',
    
#     6: 'ONOFF',
    
#     8: 'LEVEL_CONTROL',
    
#     69: 'BOOLEAN_STATE',
    
#     80: 'MODE_SELECT',
#     81: 'LAUNDRY_WASHER_MODE',
#     82: 'REFRIGERATOR_AND_TEMPERATURE_CONTROLLER_CABINET_MODE',
#     83: 'LAUNDRY_WASHER_CONTROLS',
#     84: 'RVC_RUN_MODE',
#     85: 'RVC_CLEAN_MODE',
#     86: 'TEMPERATURE_CONTROL',
#     87: 'REFRIGERATOR_ALARM',
    
#     89: 'DISH_WASHER_MODE',
    
#     91: 'AIR_QUALITY',
#     92: 'SMOKE_CO_ALARM',
#     93: 'DISHWASHER_ALARM',
    
#     96: 'OPERATIONAL_STATE',
#     97: 'RVC_OPERATIONAL_STATE',
    
#     114: 'ACTIVATED_CARBON_FILTER_MONITORING',
    
#     257: 'DOORLOCK',
#     258: 'WINDOW_COVERING',
    
#     513: 'THERMOSTAT',
#     514: 'FAN_CONTROL',
    
#     768: 'COLOR_CONTROL',
    
#     1024: 'ILLUMINANCE_SENSOR',
    
#     1026: 'TEMPERATURE_SENSOR',
#     1027: 'PRESSURE_MEASUREMENT',
#     1028: 'FLOW_MEASUREMENT',
#     1029: 'RELATIVE_HUMIDITY_SENSOR',
#     1030: 'OCCUPANCY_SENSING',
    
#     1036: 'CARBON_MONOXIDE_CONCENTRATION_MEASUREMENT',
#     1037: 'CARBON_DIOXIDE_CONCENTRATION_MEASUREMENT',
    
#     1043: 'NITROGEN_DIOXIDE_CONCENTRATION_MEASUREMENT',
    
#     1045: 'OZONE_CONCENTRATION_MEASUREMENT',
    
#     1066: 'PM25_CONCENTRATION_MEASUREMENT',
#     1067: 'FORMALDEHYDE_DIOXIDE_CONCENTRATION_MEASUREMENT',
#     1068: 'PM1_CONCENTRATION_MEASUREMENT',
#     1069: 'PM10_CONCENTRATION_MEASUREMENT',
#     1070: 'TOTAL_VOLATILE_ORGANIC_COMPOUNDS_CONCENTRATION_MEASUREMENT',
# }