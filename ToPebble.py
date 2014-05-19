import pebblelibs.pebble as libpebble
import time

def music_handler(endpoint, response):
    control_events = {
                      "NEXT"
                      }
    if response in control_events:
        uuid = pebble.current_running_uuid() # false??????
        pebble.app_message_send_string(uuid, 1 , "prova")#key ???????
        

if __name__ == '__main__':
    # create a new Pebble object
    pebble = libpebble.Pebble()
    
    # pebble MAC address
    pebble.id = '00:17:E9:6D:31:04'
    
    # init PBL log
    pebble.print_pbl_logs = False
    
    # connect via Bluetooth
    pebble.connect_via_lightblue()
    
    # register as music handler
    uuid = pebble.current_running_uuid()
    pebble.register_endpoint(uuid, music_handler)
    
    # wait for data...
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        # close the connection with the Pebble
        pebble.disconnect()
