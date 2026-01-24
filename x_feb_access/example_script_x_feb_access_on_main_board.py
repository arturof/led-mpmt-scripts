# Version 0.4 - R. Gornea on October 8, 2025 - added tests for the new functions including firmware ID
# Version 0.3 - R. Gornea on August 31, 2025 - added more complex testing loop fading gradually the intensity
# Version 0.2 - R. Gornea on July 17, 2025 - added a few simple updates to make the script clearer hopefully
# Version 0.1 - R. Gornea on June 30, 2025 - simple test with xFEB-Modbus access class on the main board

import time
from x_feb import xFEB_Modbus

my_device = xFEB_Modbus()

my_n_led_febs = my_device.get_n_led_febs()
print(f"Number of devices found is {my_n_led_febs}")

for my_led_feb_id in range(my_n_led_febs):
    print(f" *** Starting test of board with ID {my_led_feb_id} *** ")
    print(my_device.fetch_firmware_id(my_led_feb_id))
    my_status = my_device.power_on(my_led_feb_id)
    print(f"Successfully set LED-FEB power on: {my_status}")
    print("Waiting for the power on to complete ", end = '')
    while (my_device.power_status(my_led_feb_id) == False):
        print(".", end = '')
        time.sleep(1)
    print(" done!")
    my_status = my_device.set_u_controller_trig(my_led_feb_id)
    print(f"Successfully selected LED-FEB trigger source: {my_status}")
    my_status = my_device.trig_enable(my_led_feb_id)
    print(f"Successfully LED-FEB trigger enabled: {my_status}")
    my_status = my_device.led_bias_enable(my_led_feb_id)
    print(f"Successfully LED bias enabled: {my_status}")
    my_status = my_device.set_max_led_bias(my_led_feb_id)
    print(f"Successfully set intensity to maximum: {my_status}")
    print(my_device.fetch_led_bias(my_led_feb_id))
    print(my_device.fetch_i_mon(my_led_feb_id))
    #my_status = my_device.led_bias_enable(my_led_feb_id)
    #print(f"Successfully LED bias enabled: {my_status}")
    my_status = my_device.enable_channel_0(my_led_feb_id)
    print(f"Successfully channel 0 enabled: {my_status}")
    time.sleep(3)
    for my_index in range(6):
        my_bias_voltage = 13.1 - 2.0 * my_index
        my_status = my_device.set_led_bias(my_led_feb_id, my_bias_voltage)
        print(f"Successfully set the bias at {my_bias_voltage:.2f}: {my_status}")
        print(my_device.fetch_led_bias(my_led_feb_id))
        print(my_device.fetch_i_mon(my_led_feb_id))
        time.sleep(3)
    my_status = my_device.set_min_led_bias(my_led_feb_id)
    print(f"Successfully set intensity to minimum: {my_status}")
    time.sleep(3)
    my_status = my_device.disable_channel_0(my_led_feb_id)
    print(f"Successfully channel 0 disabled: {my_status}")
    my_status = my_device.set_min_led_bias(my_led_feb_id)
    print(f"Successfully set intensity to minimum: {my_status}")
    my_status = my_device.enable_channel_0(my_led_feb_id)
    print(f"Successfully channel 0 enabled: {my_status}")
    time.sleep(3)
    my_status = my_device.disable_all_channels(my_led_feb_id)
    print(f"Successfully channel 0 disabled: {my_status}")
    my_status = my_device.trig_disable(my_led_feb_id)
    print(f"Successfully LED-FEB trigger disabled: {my_status}")
    my_status = my_device.power_off(my_led_feb_id)
    print(f"Successfully set LED-FEB power off: {my_status}")

del my_device
