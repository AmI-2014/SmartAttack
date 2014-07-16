import pebblelibs as libpebble
import time, REST_client




def wait_new_pc():
    url="http://localhost/api/v1/queuemanager/?check_is_empty=1"
    while(REST_client.send('GET',url, {}, { 'Content-Type':'application/json' })==1): 
        sender = 'New help request'
        body = 'Press NEXT to receive it'
        pebble.notification_sms(sender, body)
    

def set_metadata():
    # init
    artist = " Andy "
    title = "Press NEXT to receive"
    album = "a new pc to visit"
    
    pebble.set_nowplaying_metadata(title, album, artist)
    
def send_pc_to_visit():

    artist = ' Andy '

         
        #get pc code and save it as track
    url="HTTP://localhost/api/v1/queuemanager"    
    track = REST_client.send('GET',url, {}, { 'Content-Type':'application/json' })
        #get the number of pc in queue
    url="http://localhost/api/v1/queuemanager/?check_length=1"
    n_pc_in_queue = REST_client.send('GET',url, {}, { 'Content-Type':'application/json' })
    album = n_pc_in_queue + 'pc in queue'
        
    pebble.set_nowplaying_metadata(track, album, artist)
    

def andy_handler(endpoint, response):
    control_events = {
                      "NEXT"
                      #you can add a function with "PREVIOUS" that send old pc code
                      # to avoid the problem that if a tutor click NEXT twice you loose a reservation
                      }
    if response in control_events:
        if response == 'NEXT' :
            send_pc_to_visit()

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
    pebble.register_endpoint("MUSIC_CONTROL", andy_handler)
    
    #First message with instruction
    set_metadata()
    
    # wait for data...
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        # close the connection with the Pebble
        pebble.disconnect()
