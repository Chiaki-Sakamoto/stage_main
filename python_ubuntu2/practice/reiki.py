#import
import time     #time.sleep(seconds)
import serial   #serial
#import

#serial
ser = serial.Serial("/dev/ttyUSB0",baudrate=9600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE, xonxoff=True,timeout=1)
#serial

#stegenozyoutaikakuninn
ser.write("Q:\r\n".encode("ascii")) # 状態確認
print(ser.readline()) # 状態をよみとる
ser.write("D:2S100F1000R200s100F1000R200\r\n".encode("ascii")) # 状態確認
print("speed_change")

ser.write("C:11\r\n".encode("ascii")) # 状態確認
print("free")
ser.write("Q:\r\n".encode("ascii")) # 状態確認
print(ser.readline()) # 状態をよみとる

#stegenozyoutaikakuninn
time.sleep(1)
#move
ser.write("Q:\r\n".encode("ascii")) # 状態確認
print(ser.readline()) # 状態をよみとる

angle = 10
move_dis_1 = angle*400
ser.write(("M:1+P%d\r\n"%abs(move_dis_1)).encode("ascii"))
ser.write("G\r\n".encode("ascii")) # 動かせ
#move
