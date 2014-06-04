import pebblelibs.pebble as libpebble
import time

#test
def get_pc_from_queue():
    return '10s'
def get_queue_lenght():
    return 5

def set_metadata():
    # init
    artist = "  Andy  "
    title = "Press NEXT to receive"
    album = "a new pc to visit"
    
    pebble.set_nowplaying_metadata(title, album, artist)
    
def send_pc_to_visit():

    pc_code = get_pc_from_queue()
    
    if pc_code == None: 
        #queue is empy
        t_track = 'No pc in queue'
        t_album = ''
    else : 
        t_track = pc_code
        #get the number of pc in queue
        n_pc_in_queue = get_queue_lenght()
        t_album = n_pc_in_queue + 'pc in queue'
    
    artist = '  Andy  '
    track = t_track
    album = t_album
    
    pebble.set_nowplaying_metadata(track, album, artist)

def andy_handler(endpoint, response):
    control_events = {
                      "NEXT"
                      #you can add a function with "PREVIOUS" that send old pc codes
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
