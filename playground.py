from time import sleep
from liquidctl import find_liquidctl_devices
devs = find_liquidctl_devices()
d = list(devs)[0]



def init():
    d.connect()
    #print(d.get_status())
    print(d.initialize())
    #d._read()
    #sleep(0.2)
    #d.device.clear_enqueued_reports()

    #d._write([0x10, 0x01])
    #d._read()

    # init ??
    d._write([0x36, 0x03])
    d._read()

# not sure why, what for ?
def get_display_info():
    # generic info about display ???
    d._write([0x30, 0x01])
    return d._read()

# get info about slot
def get_slot_info():
    d._write([0x30, 0x04, slot])
    return d._read()

def get_fw_info():
    d._write([0x20, 0x03])
    d._read()

    d._write([0x70, 0x01])
    d._read()

def set_rotation():
    # rotate (last byte 0x00 .. 0x03 - clock-wise 90° steps)
    # * rotation is only applied on a newly saved slot
    d._write([0x30, 0x02, 0x01, 0x3d, 0x00, 0x00, 0x01, 0x03])
    return d._read()


def write_slot(slot, content=None):

    # init write
    d._write([0x32, 0x02, slot])
    d._read()
    #d._write([0x32, 0x02, slot])
    #d._read()
    #d._write([0x32, 0x02, slot])
    #d._read()

    # init write is mostly called twice by CAM, why?

    # write "data" to slot
    # * slot is here twice, really?
    # * the next two bytes seem to be the data to be set (or moreover identifying)
    # * the final 3 bytes are always the same ?

    d._write([0x32, 0x01, slot, slot, 0b11000000 , 0b00000110, 0x90, 0x01, 0x01])
    d._read()

    # write buffer to slot [slot]
    # * CAM has ~2sec after this call, guess this will be based on the gif transfer duration?
    d._write([0x36, 0x01, slot])
    d._read()
    sleep(2)

def view_slot(slot):

    # set proper mode to view slot
    d._write([0x36, 0x02])
    d._read()

    # now view slot
    d._write([0x38, 0x01, 0x04, slot])
    d._read()

def set_brightness(percent):
    # last byte 0x00 .. 0x64
    d._write([0x30, 0x02, 0x01, percent])
    return d._read()



if __name__ == "__main__":
    from sys import argv
    slot = int(argv[1])


    init()

    set_brightness(1)
    sleep(2)
    set_brightness(100)


    write_slot(slot)
    view_slot(slot)



