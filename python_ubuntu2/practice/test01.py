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
#stegenozyoutaikakuninn

#move
move_dis_1 = 400  #パルス(1deg=400)
ser.write(("M:1+P%d\r\n"%abs(move_dis_1)).encode("ascii"))
ser.write("G\r\n".encode("ascii")) # 動かせ
#move

#stegenozyoutaikakuninn-kaitengo
time.sleep(1) #mawatteirutotyuuniyorutohasuugaderu
ser.write("Q:\r\n".encode("ascii")) # 状態確認
print(ser.readline()) # 状態をよみとる
#stegenozyoutaikakuninn

#move
move_dis_1 = 800  #パルス(1deg=400)
ser.write(("M:1-P%d\r\n"%abs(move_dis_1)).encode("ascii"))
ser.write("G\r\n".encode("ascii")) # 動かせ
#move

time.sleep(1) #mawatteirutotyuuniyorutohasuugaderu

# 原点回帰
ser.write("H:1-\r\n".encode("ascii")) # 1軸機械原点復帰
#ser.write("H:2-\r\n".encode("ascii")) # 2軸機械原点復帰
#0deg&R tonatterukakakunin  timesleepwotukattekakuzituni
# 原点回帰

#stegenozyoutaikakuninn-gentenkaikigo
time.sleep(1) #mawatteirutotyuuniyorutohasuugaderu
ser.write("Q:\r\n".encode("ascii")) # 状態確認
print(ser.readline()) # 状態をよみとる
#stegenozyoutaikakuninn
