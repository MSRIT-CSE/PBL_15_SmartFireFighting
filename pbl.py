from ubidots import ApiClient
import os
import glob
import time
import RPi.GPIO as GPIO
import time
api = ApiClient("181bfdacd408f5d2dcff6ebdb655b2a68387606e")
test_variable1 = api.get_variable("5669a22d7625422c9c7345aa")
test_variable = api.get_variable("56699131762542086a2f3480")
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(11,GPIO.IN)
os.system('moderate w1-therm')
base_dir='/sys/bus/w1/devices/'
device_folder=glob.glob(base_dir + '28-0314566612ff')[0]
#g from 28*
device_file = device_folder + '/w1_slave'
def read_temp_raw():
        f=open(device_file,'r')
        lines=f.readlines()
        f.close()
        return lines 
def read_temp():
        lines=read_temp_raw()
        while lines[0].strip()[-3:]!='YES':
                time.sleep(0.2)
                lines=read_temp_raw()
equals_pos=lines[1].find('t=')
        if equals_pos!=-1:
                temp_string = lines[1][equals_pos+2:]
                temp_c=float(temp_string)/1000.0
                temp=GPIO.input(11)
                if (temp_c <50) and (temp==1):
                        GPIO.output(13,0)
                else :
                        GPIO.output(13,1)
                test_variable.save_value({'value':temp_c})
                test_variable1.save_value({'value':temp})
                if GPIO.input(11):
                        print "Smoke not sensed"
                else:
                        print "Smoke sensed"
                temp_f=temp_c*9.0/5.0 + 32.0
                return temp_c,temp_f
while True:
        print(read_temp())
        time.sleep(1)