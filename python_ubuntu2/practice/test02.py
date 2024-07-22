
#import
import PythonDSO #Oshiro#zikkoufairutoonazidelirekutoriniireru
#mataha Pathwotoosu

#Oshiro Setuzoku
obj=PythonDSO.LecroyVICP("192.168.2.20") # オシロスコープと接続する
#obj ni insutansuka sita

#zikan denatu wokaesu obj.get_scaled_waveform_withtim
data =  obj.get_scaled_waveform_withtime("C2") # オシロスコープから波形を転送する．scwltは時間と電圧の配列
#get_scaled_waveform_withtim ha sokuteiti novtwo kaesu kaeritwoireruhensuugahituyou
#%s ni oshiro no CH1-4 ga hairu

print(data) #kekka syuturyoku
#data[0]-t ,data[1]-v

##
print("レンジを50mv/divに変更")
obj.writestring("C2:VDIV 0.05") # レンジ変更
data2=obj.get_scaled_waveform_withtime("C2") # 計測
print(data2)
##


