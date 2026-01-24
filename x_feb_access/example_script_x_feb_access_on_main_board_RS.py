# Version 0.3 - R. Gornea on August 31, 2025 - added more complex testing loop fading gradually the intensity
# Version 0.2 - R. Gornea on July 17, 2025 - added a few simple updates to make the script clearer hopefully
# Version 0.1 - R. Gornea on June 30, 2025 - simple test with xFEB-Modbus access class on the main board

import time
from x_feb import xFEB_Modbus

my_device = xFEB_Modbus()

my_n_led_febs = my_device.get_n_led_febs()
print(f"Number of devices found is {my_n_led_febs}")
for my_led_feb_id in range(my_n_led_febs):
    print(f" *** Starting test of board with id {my_led_feb_id} *** ")
    my_status = my_device.power_on(my_led_feb_id)
    print(f"Successfully set LED-FEB power on: {my_status}")

    time.sleep(0.25)
    time.sleep(5.25)
    my_status = 0
    while my_status == 0:
        my_status = my_device.power_status(my_led_feb_id)
        print(f"Power Status is now : {my_status}")
    
    # my_status = my_device.u_controller_trig(my_led_feb_id)
    # print(f"Successfully selected LED-FEB trigger source: {my_status}")
    my_status = my_device.ext_crystal_trig(my_led_feb_id)
    print(f"Successfully selected LED-FEB trigger source: {my_status}")
    
    my_status = my_device.trig_enable(my_led_feb_id)
    print(f"Successfully LED-FEB trigger enabled: {my_status}")
    
    my_status = my_device.led_bias_enable(my_led_feb_id)
    print(f"Successfully LED-FEB bias enabled: {my_status}")

    my_status = my_device.max_led_bias(my_led_feb_id)
    print(f"Successfully set intensity to maximum: {my_status}")
    my_status = my_device.enable_channel_0(my_led_feb_id)
    print(f"Successfully channel 0 enabled: {my_status}")
    
    my_status = my_device.enable_all_channels(my_led_feb_id)
    print(f"Successfully all channels enabled: {my_status}")
    
    time.sleep(3)
    for my_index in range(6):
        my_bias_voltage = 13.1 - 2.0 * my_index
        my_status = my_device.set_led_bias(my_led_feb_id, my_bias_voltage)
        print(f"Successfully set the bias at {my_bias_voltage}: {my_status}")
        time.sleep(3)
    my_status = my_device.min_led_bias(my_led_feb_id)
    print(f"Successfully set intensity to minimum: {my_status}")
    time.sleep(3)
    my_status = my_device.disable_channel_0(my_led_feb_id)
    print(f"Successfully channel 0 disabled: {my_status}")
    my_status = my_device.min_led_bias(my_led_feb_id)
    print(f"Successfully set intensity to minimum: {my_status}")
    my_status = my_device.enable_channel_0(my_led_feb_id)
    print(f"Successfully channel 0 enabled: {my_status}")
    time.sleep(3)
    my_status = my_device.disable_all_channels(my_led_feb_id)
    print(f"Successfully channel 0 disabled: {my_status}")
    my_status = my_device.trig_disable(my_led_feb_id)
    print(f"Successfully LED-FEB trigger disabled: {my_status}")
    
    my_status = my_device.led_bias_disable(my_led_feb_id)
    print(f"Successfully LED-FEB Bias disabled: {my_status}")
    
    my_status = my_device.power_off(my_led_feb_id)
    print(f"Successfully set LED-FEB power off: {my_status}")

del my_device
