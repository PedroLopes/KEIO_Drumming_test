from time import sleep
import serial
import threading
import logging 
import time
import numpy as np
import simpleaudio as sa

def metronome():
    wave_obj = sa.WaveObject.from_wave_file("click.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

def getInput():
    global flag 
    global current_time
    while 1:
        input = ser.readline(ser.in_waiting)
        #if b'HIT' in input:
        #    if(getTime() - current_time  > 0.001):
        #        logging.info("HIT:\t" + str(getTime()))
        #        current_time = getTime()
        
        if b'HIT_LEFT' in input:
            if(getTime() - current_time  > 0.05):
                logging.info("HIT_LEFT:\t" + str(getTime()))
                current_time = getTime()
        elif b'HIT_RIGHT' in input:
            if(getTime() - current_time  > 0.05):
                logging.info("HIT_RIGHT:\t" + str(getTime()))
                current_time = getTime()
        
        if flag == True:
            break

def countdown(beats):
    for i in range(beats):
        print(str(i+1))
        thread_metronome = threading.Thread(target=metronome)
        thread_metronome.start() 
        if i+1==beats and mode == EMS:
            sleep(time_beats-extensor_preemption) 
            ser.write("2\n".encode()) 
            sleep(extensor_preemption)
            ser.write("2\n".encode()) 
        else:
            sleep(time_beats)  
        #thread_metronome.join()   

def PGMcontrol():
    global flag    
    countdown(4)
    Exercise(5)
    '''
    for i in range(5):
        #print("starting actuate...")
        ser.write("1\n".encode())
        sleep(0.1)
        ser.write("1\n".encode())
        ser.write("2\n".encode())
        sleep(0.2)
        ser.write("2\n".encode())
        sleep(0.7)
        logging.info("PGM:\t" + str(getTime()))
        sleep(1)
    '''
    flag = True

def WristControl(channel, time, num):
    thread_metronome = threading.Thread(target=metronome)
    thread_metronome.start()
    for repetation_number in np.arange(num): 
        if channel == 'left':
            ser.write("3\n".encode())
            sleep(time * 0.1)
            ser.write("3\n".encode())
            ser.write("4\n".encode())
            sleep(time * 0.2)
            ser.write("4\n".encode())
            sleep(time * 0.7)
            logging.info("PGM_LEFT:\t" + str(getTime()))
        elif channel == 'right':
            ser.write("1\n".encode())
            sleep(time * 0.1)
            ser.write("1\n".encode())
            ser.write("2\n".encode())
            sleep(time * 0.2)
            ser.write("2\n".encode())
            sleep(time * 0.7)
            logging.info("PGM_RIGHT:\t" + str(getTime()))

def Exercise(num):
    rhythm = {
        1 : lambda : ex1(),
        2 : lambda : ex2(),
        3 : lambda : ex3(),
        4 : lambda : ex4(),
        5 : lambda : ex5()
    }
    rhythm[num]()

def ex1():
    # repeat beat (quarter note)
    for i in range(64):
        #thread_metronome = threading.Thread(target=metronome)
        #thread_metronome.start()
        WristControl('right', 0.8, 1)
    #ser.write("5\n".encode())

def ex2():
    # Single stroke four
    for i in range(4):
        for j in range(2):
            WristControl('right', 0.8, 1)
            WristControl('left', 0.8, 1)

        for k in range(2):
            WristControl('left', 0.8, 1)
            WristControl('right', 0.8, 1)
    #ser.write("5\n".encode())


def ex3():
    # Single paradiddle
    for i in range(8):
        WristControl('right', 0.8, 1)
        WristControl('left', 0.8, 1)
        WristControl('right', 0.8, 1)
        WristControl('right', 0.8, 1)
        
        WristControl('left', 0.8, 1)
        WristControl('right', 0.8, 1)
        WristControl('left', 0.8, 1)
        WristControl('left', 0.8, 1)
    #ser.write("5\n".encode())


def ex4():
    # double paradiddle
    for i in range(5):
        WristControl('right', 0.8, 1)
        WristControl('left', 0.8, 1)
        WristControl('right', 0.8, 1)
        WristControl('left', 0.8, 1)
        
        WristControl('right', 0.8, 1)
        WristControl('right', 0.8, 1)
        WristControl('left', 0.8, 1)
        WristControl('right', 0.8, 1)

        WristControl('left', 0.8, 1)
        WristControl('right', 0.8, 1)
        WristControl('left', 0.8, 1)
        WristControl('left', 0.8, 1)
    #ser.write("5\n".encode())

def ex5():
    # double paradiddle
    for i in range(6):
        WristControl('right', 0.4, 2)
        WristControl('left', 0.8, 1)
        WristControl('right', 0.8, 1)
        WristControl('right', 0.8, 1)

        WristControl('left', 0.4, 2)
        WristControl('right', 0.8, 1)
        WristControl('left', 0.8, 1)
        WristControl('left', 0.8, 1)
    #ser.write("5\n".encode())

def getTime():
    global start_time
    return time.time() - start_time

#
COM_port = '/dev/tty.usbserial-A104WP9R'
baud_rate = 115200
time_beats = 0.8
extensor_preemption = 0.1
EMS = 1
NO_EMS = 2

#setup mode
mode = EMS

#open the connection
ser = serial.Serial(COM_port, baud_rate)#, write_timeout=0,timeout=0) 

#setup flag
flag = False

#setup logging 
FORMAT = '%(message)s'
file_handler = logging.FileHandler('Pedrotest_ex5_3 .log')
logging.basicConfig(format=FORMAT,level=logging.DEBUG)
file_handler.setFormatter(logging.Formatter(FORMAT))
logging.getLogger().addHandler(file_handler)

#make thread object
start_time = time.time()
current_time = getTime()
thread_input = threading.Thread(target=getInput)
thread_output = threading.Thread(target=PGMcontrol)

thread_input.start()
thread_output.start()


#thread_obj.join()