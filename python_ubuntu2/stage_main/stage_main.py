# gui 無駄なものがあるかも #
import tkinter as tk  # gui
# import tkinter.ttk as ttk
# from tkinter import font
# from tkinter import messagebox
import os
import sys
# from tkinter import *
# from tkinter import filedialog
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  \
# グラフをgui 上に表示

# 基本的なモジュール #
from math import *
import numpy as np
import time
# import subprocess as sp
import matplotlib.pyplot as plt

# 接続機器 #
import serial
# import TIS
import PythonDSO

# original #
import stage_gui
import ssh
from cmos import Cmos


class Application(stage_gui.Gui):  # stage_gui.Gui を継承
    def __init__(self, master=None):  # 最初によみこまれる関数
        super().__init__(master)  # Guiクラスのコンストラクタを呼び出す
        self.master = master
        self.sername = "/dev/ttyUSB0"  # ステージコントローラーの usb ポート指定
        self._oshiro_ip = "192.168.2.20"
        # self.sername = \
        # "/dev/serial/by-path/pci-0000:00:06.0-usb-0:1:1.0-port0"
        self.ser = serial.Serial(
            self.sername,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=True,
            timeout=1
        )  # serial 通信
        # endregion
        self.cmos = Cmos(self.master)  # カメラモジュールのインスタンス化
        self.ssh = ssh.Ssh()  # ssh モジュールのインスタンス化
        self.ssh.ssh_connect()  # ssh 接続
        v, p = self.pressure()  # v,p を定義するため
        # ボタン設定 #
        self.speed_B.bind("<Button-1>", lambda event: self.speedvariable())
        self.Run_B.bind("<Button-1>", lambda event: self.StageRun())
        self.restart.bind("<Button-1>", lambda event: self.axis1re())
        self.save_B.bind("<Button-1>", lambda event: self.save())
        self.hakei_B.bind("<Button-1>", lambda event: self.timewave())
        self.keisoku_B.bind("<Button-1>", lambda event: self.experiment())
        self.auto_save_B.bind("<Button-1>", lambda event: self.auto_save())
        self.stop_B.bind("<Button-1>", lambda event: self.stop())
        self.property_B.bind(
            "<Button-1>",
            lambda event: self.cmos.property_function()
        )
        self.image_B.bind("<Button-1>", lambda event: self.cmos.capture())
        self.image_save_B.bind(
            "<Button-1>",
            lambda event: self.cmos.save(
                self.image_savedirectory_box.get(),
                self.image_savename_box.get()
            )
        )
        self.ave_B.bind(
            "<Button-1>",
            lambda event: self.cmos.average(
                self.image_savedirectory_box.get(),
                self.image_savename_box.get()
            )
        )

    def experiment(self):  # 実験用プログラム
        print("experiment")
        self.ax.clear()  # グラフをリセット
        self.ax.tick_params(
            axis="both",
            width=1.0,
            size=5,
            labelsize=10,
            direction="in",
            top=True,
            right=True
        )  # 目盛り
        self.ax.grid()  # grid
        self.ax.set_xlabel("Angle (degree)", fontsize=15)  # 横軸
        self.ax.set_ylabel("Voltage (mV)", fontsize=15)  # 縦軸
        self.oshiro()  # oshiro 関数を使用する Time は time.sleep() を用いるため

    def oshiro(self):  # オシロスコープと接続し空の配列 data を作成
        self.obj = PythonDSO.LecroyVICP("192.168.2.20")  # オシロスコープと接続する
        self.sclwt_trace = self.obj.get_scaled_waveform_withtime(
            "%s" % self.ex_chanel.get()
        )  # オシロスコープから波形を転送する．scwltは時間と電圧の配列
        print("%s" % self.chanel.get())
        self.obj.disconnect()  # オシロスコープとの接続を解除する．
        self.t = self.sclwt_trace[0]  # 時間
        self.data = np.zeros(len(self.t))  # 配列の大きさ
        self.move()  # move関数を使用する

    def move(self):  # 計測するプログラム
        self.ex_Statuslabel.configure(bg="red")  # busy を表す赤色表示
        self.ex_Statuslabel.update()  # ここで update を挟まないとラベルが再描画されない
        self.start = float(self.ex_start_box.get())  # 計測開始角度
        self.end = float(self.ex_end_box.get())  # 計測終了角度
        self.width = float(self.ex_width_box.get())  # 角度幅
        self.number = int((self.end-self.start)/self.width+1)  # 計測回数0を含むため+1
        self.v_data = []  # 角度ごとの圧力計の電圧を入れる空の配列
        self.p_data = []  # 角度ごとのガス圧を入れる空の配列
        self.vmax = np.zeros(self.number)  # グラフに用いる配列
        self.txt.insert(tk.END, "計測を行います.\r\n")  # Gui に表示
        self.txt.see("end")  # 一番下に表示する
        for i in range(self.number):  # 計測回数でループ
            self.ex_exeframe.update()
            if (self.hantei.get() == "終了"):
                break
            self.obj = PythonDSO.LecroyVICP("192.168.2.20")  # オシロスコープと接続する.
            self.sclwt_trace = self.obj.get_scaled_waveform_withtime(
                "%s" % self.ex_chanel.get()
            )  # オシロスコープから波形を転送する．scwltは時間と電圧の配列
            if (min((self.sclwt_trace[1])) < -0.075):  # 50mV/div のレンジに変更
                # print(max(sclwt_trace[1])*1000)
                print("レンジを50mv/divに変更")
                self.obj.writestring(
                    "%s:VDIV 0.05" % self.ex_chanel.get()
                )  # レンジ変更
            elif (min((self.sclwt_trace[1])) < -0.035):  # 20mV/div のレンジに変更
                # print(max(sclwt_trace[1])*1000)
                # print("レンジを20mv/divに変更")
                self.obj.writestring(
                    "%s:VDIV 0.02" % self.ex_chanel.get()
                )  # レンジ変更
            elif (min((self.sclwt_trace[1])) < -0.0175):  # 10mV/div のレンジに変更
                # print(max(sclwt_trace[1])*1000)
                # print("レンジを10mv/divに変更")
                self.obj.writestring(
                    "%s:VDIV 0.01" % self.ex_chanel.get()
                )  # レンジ変更
            elif (min((self.sclwt_trace[1])) < -0.007):  # 5mV/div のレンジに変更
                # print(max(sclwt_trace[1])*1000)
                # print("レンジを5mv/divに変更")
                self.obj.writestring(
                    "%s:VDIV 0.005" % self.ex_chanel.get()
                )  # レンジ変更
                # print("再度計測しなおしました")
            time.sleep(2)
            self.sclwt_trace = self.obj.get_scaled_waveform_withtime(
                "%s" % self.ex_chanel.get()
            )  # 計測
            self.obj.disconnect()  # オシロスコープとの接続を解除する．
            self.cmos.save(self.ex_savedirectory_box.get()+"cap_{}/".format(
                self.ex_savename_box.get()),
                "degree={}".format(i))
            self.txt.insert(tk.END, "%s°の計測をしました\r\n" % i)  # Gui 上に表示
            self.txt.see("end")  # 一番下に表示
            self.t = self.sclwt_trace[0]  # 時間
            self.voltage = self.sclwt_trace[1]  # 信号値
            # print(t.shape)
            self.txt.insert(
                tk.END,
                "%s mV \r\n" % (min((self.voltage))*1000)
            )  # Gui 上に最大値を表示
            self.txt.see("end")  # 一番下に表示
            self.data = np.vstack((self.data, self.t))  # 時間 を列に加える
            self.data = np.vstack((self.data, self.voltage))  # 信号値を列に加える
            self.vmax[i] = min(
                self.voltage[
                    int(self.pixel_box_1.get()):int(self.pixel_box_2.get())
                ]
            )  # 最大値を vmax[i] に代入
            self.ax.plot(
                i * self.width,
                self.vmax[i] * 1000,
                marker="o",
                color="r"
            )  # グラフ
            self.canvas.draw()  # Gui上に表示
            v, p = self.pressure()
            self.v_data = np.append(self.v_data, v)  # 圧力計の電圧値を記録
            self.p_data = np.append(self.p_data, p)  # ガス圧を記録
            self.READY()  # ready 状態にする
            self.ser.write(
                ("M:2+P%d\r\n" % (self.width*400)).encode("ascii")
            )  # 指定した角度幅だけ回転させる．
            self.ser.write("G:\r\n".encode("ascii"))  # 動かせ.
            time.sleep(2)  # average
            self.READY()  # ready 状態にする
            self.STATUS()  # 現在の角度を GUI 上に表示
        if (self.hantei.get() == "終了"):  # 強制終了
            self.on_closing()
            # quit()
        self.cmos.on_closing()
        self.data = np.delete(self.data, 0, 0)  # 最初に作成した空の配列を削除
        self.maketxt()  # maketxt 関数を使用する
        self.ser.write(
            ("M:2-P%d\r\n" % ((self.end-self.start+1)*400)).encode("ascii")
        )  # 開始角度に移動
        self.ser.write("G:\r\n".encode("ascii"))  # 動かせ
        self.ex_Statuslabel.configure(bg="green")  # ready を表す緑色表示
        self.STATUS()  # 現在の角度を Gui 上に表示
        self.txt.insert(tk.END, "計測を終了します。\r\n")  # Gui 上に表示
        self.txt.see("end")  # 一番下に表示
        self.cmos = Cmos(self.master)

    def maketxt(self):  # txt データ作成のプログラム
        os.makedirs(
            "%s" % (self.ex_savedirectory_box.get()), exist_ok=True
        )  # savedirectoryを作成する
        self.txt.insert(tk.END, "txtデータを作成します。\r\n")  # Gui上に表示
        self.txt.see("end")  # 一番下に表示
        self.txt.insert(
            tk.END,
            "(%d,%d)\r\n" % (self.data.shape[0], self.data.shape[1])
        )  # Guiに表示
        self.txt.see("end")  # 一番下に表示
        property_number, property_name = self.cmos.property_text()  # カメラの設定を取得
        with open(
            "%s%s.txt" % (
                self.ex_savedirectory_box.get(),
                self.ex_savename_box.get()
            ),
            "w"
        ) as file:  # txt データの作成
            file.write(
                "#開始角度 %s,終了角度%s,角度間隔 %s deg\n #一列目は時間、2列目は信号値 エンコードはutf-8 !!"
                % (self.start, self.end, self.width)+"\r\n"
            )  # text を書き込み
            # file.write("volt_range ##,time_range ##"+"\r\n")
            file.write(
                "Cmos property\n%s\n%s" % (property_name, property_number) +
                "\r\n"
            )
            file.write(
                "圧力計の電圧(V)，ガス圧(MPa)\n %s,%s\n"
                % (self.v_data, self.p_data) + "\r\n"
            )
            for n in range(self.data.shape[1]):  # データの大きさ
                for a in range(2 * self.number):  # 計測回数
                    if (a < 2 * self.number - 1):  # 最終行の一つ手前まで
                        file.write(
                            "{},".format(self.data[a, n])
                        )  # 時間 信号値の順番で書き込み
                    else:  # 最終行
                        file.write(
                            "{}\r\n".format(self.data[a, n])
                        )  # 終了角度の信号値を書き込み、改行する
            file.close()  # ファイルを閉じる
        self.txt.insert(tk.END, "txt データを作成しました。\r\n")  # Gui 上に表示
        self.txt.see("end")  # 一番下に表示

    def stop(self):  # 強制終了の関数．
        print("stop")
        self.ser.write("L:E\r\n".encode("ascii"))  # 強制終了
        self.ser.close()  # serial 通信終了
        self.on_closing()  # on_closing 関数
        # elf.master.quit() # Gui を閉じる
        print("強制終了しました")
        self.hantei.set("終了")

    def StageRun(self):  # Run ボタン の関数
        print("stageRun")
        self.move_dis_1 = float(self.thetabox.get())  # Editbox に入った数値を得る
        self.move_dis_1 = self.move_dis_1 * 200 * 2  # パルス
        # move_dis_2 = move_dis_2 * 1000   #パルス
        self.degree = int(self.move_dis_1 / 400)  # パルスを角度に変換
        if (self.move_dis_1 > 0):  # 時計回りに
            self.ser.write(
                ("M:1+P%d\r\n" % abs(self.move_dis_1)).encode("ascii")
            )
        else:  # 反時計回りに
            self.ser.write(
                ("M:1-P%d\r\n" % abs(self.move_dis_1)).encode("ascii")
            )
        self.ser.write("G\r\n".encode("ascii"))  # 動かせ
        self.READY()  # ready 状態にする
        self.STATUS()  # 現在の角度を Gui 上に表示する。
        self.txt.insert(tk.END, "%s °回転しました\r\n" % self.degree)  # Gui 上に表示する
        self.txt.see("end")  # 一番下に表示

    def axis1re(self):  # 原点回帰
        print("axis1re")
        self.ser.write("H:2-\r\n".encode("ascii"))  # 1軸機械原点復帰
        # ser.write("H:2-\r\n".encode("ascii")) # 2軸機械原点復帰
        # 1 軸が0 になるまで待つコード．原点回帰中にredyになるため###
        while True:  # 1軸の座標が 原点になるまでループして待つ．
            self.ser.write("Q:\r\n".encode("ascii"))  # 状態の確認
            self.status = self.ser.readline()  # status に状態を代入
            self.degree = chr(self.status[5])
            + chr(self.status[6])
            + chr(self.status[7])
            + chr(self.status[8])
            + chr(self.status[9])  # 1 軸のパルス数を代入
            self.degree = int(self.degree)  # degree はstr(文字列)なのでint(数字)に直す．
            self.degree = (self.degree) / 400  # パルスを角度に変換．
            if (self.degree == 0):  # 0°にならループを抜ける
                break
            time.sleep(3.0)  # 時間を長くするほど正確になる．
        self.READY()  # ready 状態にする
        self.angle.set("%d" % self.degree)  # 現在の角度を Gui 上に表示
        self.txt.insert(tk.END, "原点回帰しました。\r\n")  # Gui 上に表示
        self.txt.see("end")  # 一番下に表示

    def speedvariable(self):  # 回転速度の変更
        print("speedvariable")
        self.ser.write(("D:2S%sF%sR%sS100F1000R200\r\n" % (
            self.speed_s_box.get(),
            self.speed_f_box.get(),
            self.speed_r_box.get()
        )).encode("ascii"))  # 2Sは 1 軸 S は 2 軸
        self.READY()  # ready 状態にする
        self.txt.insert(
            tk.END,
            "D:2S%sF%sR%sS100F1000R200\r\n" % (
                self.speed_s_box.get(),
                self.speed_f_box.get(),
                self.speed_r_box.get()
            )
        )  # Gui 上に表示
        self.txt.see("end")  # 一番下に表示
        self.txt.insert(tk.END, "速度を変更しました\r\n")  # Gui 上に表示
        self.txt.see("end")  # 一番下に表示

    def save(self):  # 波形の保存
        print("save")
        os.makedirs(
            "%s" % (self.savedirectory_box.get()),
            exist_ok=True
        )  # savedirectoryを作成する
        self.obj = PythonDSO.LecroyVICP("192.168.2.20")  # オシロスコープと接続する
        self.sclwt_trace = self.obj.get_scaled_waveform_withtime(
            "%s" % self.chanel.get()
        )  # オシロスコープからの波形を転送する．scwltは時間と電圧の配列
        self.obj.disconnect()  # オシロスコープとの接続を解除する．
        with open(
            "%s%s.txt" % (
                self.savedirectory_box.get(),
                self.savename_box.get()
            ), "w"
        ) as file:  # txt データの作成
            file.write(
                "保存した波形 %s\r\n 1 列目は時間,2 列目は信号値\r\n \r\n" % (self.chanel.get())
            )  # txt データの説明
            for i in range(len(self.sclwt_trace[1])):  # データの大きさ
                file.write(
                    "{},{}\r\n".format(
                        self.sclwt_trace[0][i],
                        self.sclwt_trace[1][i])
                )  # 時間、信号値の順で書き込み
            file.close()  # txt データを閉じる
        self.txt.insert(
            tk.END,
            "%s の波形を保存しました\r\n" % self.chanel.get()
        )  # Gui 上に作成
        self.txt.see("end")  # 一番下に表示

    def READY(self):  # ready 状態にする関数
        self.Statuslabel.configure(bg="red")  # ready を表す緑色表示
        self.Statuslabel.update()  # ここで update を挟まないとラベルが再描画されない
        while True:  # Busy か Ready を判定するためのループ
            self.ser.write("Q:\r\n".encode("ascii"))  # 状態の確認
            self.status = (self.ser.readline())  # 状態をよみとる
            self.loc = self.status.rfind(b",")  # 右から , の場所を探す
            if (self.status[self.loc+1] == 82):  # 82 = R
                break
            time.sleep(0.5)
        self.Statuslabel.configure(bg="green")  # ready を表す緑色表示
        self.Statuslabel.update()  # ここで update を挟まないとラベルが再描画されない
        self.txt.insert(tk.END, "%s\r\n" % self.status)
        self.txt.see("end")
        # time.sleep(1) # 長くするほど正確になる

    def STATUS(self):  # GUI 上に 現在の角度を表示
        self.ser.write("Q:\r\n".encode("ascii"))  # 状態確認
        self.status = self.ser.readline()  # 状態をよみとる．
        self.txt.insert(tk.END, "%s\r\n" % self.status)
        self.txt.see("end")
        self.degree = chr(self.status[5]) + chr(self.status[6]) + chr(self.status[7]) + chr(self.status[8]) + chr(self.status[9])  # asciiをstrに直す．パルスの 5 桁までを読み込む(角度は 250 まで)．
        self.degree = int(self.degree)  # degree はstr(文字列)なのでint(数字)に直す.
        self.degree = (self.degree) / 400  # パルスを角度に変換．-1 は止まる際に動く距離．修正する個所．
        self.angle.set("%d" % self.degree)  # 現在の角度を Gui 上に表示

    def timewave(self):
        print("timewave")
        plt.close()  # 放射角度分布のグラフが描写されるため．
        self.f, self.ax = plt.subplots(1)
        self.obj = PythonDSO.LecroyVICP("192.168.2.20")  # オシロスコープと接続する
        self.sclwt_trace = self.obj.get_scaled_waveform_withtime(
            "%s" % self.ex_chanel.get()
        )  # オシロスコープから波形を転送する．scwltは時間と電圧の配列
        self.obj.disconnect()  # オシロスコープとの接続を解除する．
        self.x_pixel = np.arange(0, len(self.sclwt_trace[0]), 1)
        self.txt.insert(
            tk.END,
            "data.shape = [%d,%d] \r\n" % (
                len(self.sclwt_trace[0]),
                len(self.sclwt_trace[1])
            )
        )  # Gui 上に作成
        self.txt.see("end")  # 一番下に表示
        self.ax.plot(self.x_pixel, self.sclwt_trace[1])
        plt.show()

    def pressure(self):
        ssh_voltage = self.ssh.get_volt()
        ssh_pressure = (ssh_voltage-0.590)/3.975
        self.now_pressure.set("%0.3f" % ssh_pressure)  # 現在の角度を Gui 上に表示
        return ssh_voltage, ssh_pressure

    def auto_save(self):
        print("\033[38;5;30mexe auto save\033[0m\n")
        start_angle = float(self.auto_save_start_box.get()) + 30.0
        end_angle = float(self.auto_save_end_box.get()) + 30.0
        width_angle = float(self.auto_save_width_box.get())
        mesure_number = int(abs(((end_angle - start_angle) / width_angle)))
        current_angle = self._get_current_angle()
        angle_move_to_init = current_angle - start_angle
        direction_rotate = '-' if start_angle >= end_angle else '+'

        print("start:%f, end:%f, mesure_number:%d\n" % (start_angle, end_angle, mesure_number))
        print("current angle: %f\n" % current_angle)
        print("init move angle: %f" % angle_move_to_init)
        self.ser.write(("D:2S%sF%sR%sS100F1000R200\r\n" % (
            400,
            400,
            400
        )).encode("ascii"))
        if (angle_move_to_init >= 0):
            self._rotate_stage("-", abs(angle_move_to_init))
        else:
            self._rotate_stage("+", abs(angle_move_to_init))
        self.ser.write("G\r\n".encode("ascii"))
        self.READY()
        self.ser.write("Q:\r\n".encode("ascii"))
        print("current angle: %f\n" % self._get_current_angle())
        time.sleep(3)
        self._save_wave(self.auto_save_savename_box.get() + str(int(start_angle - 30)))
        for i in range(mesure_number):
            self._rotate_stage(direction_rotate, width_angle)
            time.sleep(3)
            if (start_angle <= end_angle):
                self._save_wave(self.auto_save_savename_box.get() + str(int(start_angle + (i + 1) * width_angle - 30)))
            else:
                self._save_wave(self.auto_save_savename_box.get() + str(int(start_angle - (i + 1) * width_angle - 30)))
        print("current angle: %f\n" % self._get_current_angle())
        print("\033[38;5;30mEnd of measurement\033[0m\n")

    def on_closing(self):
        # if messagebox.askokcancel("Quit","Do you want to quit ?"):
        self.cmos.on_closing()  # cmos カメラの終了
        self.ssh.ssh_close()  # ssh 接続の終了
        self.ser.close()  # serial 通信の終了
        self.master.quit()  # gui の終了
        sys.exit()  # プログラムの終了

    def _get_current_angle(self):
        self.ser.write("Q:\r\n".encode("ascii"))
        current_status = self.ser.readline()
        current_angle = ''.join([chr(current_status[i]) for i in range(5, 10)])
        current_angle = float(int(current_angle) / 400)
        return current_angle

    def _rotate_stage(self, direction, angle):
        self.ser.write(
            ("M:1%sP%d\r\n" % (direction, angle * 400)).encode("ascii")
        )
        self.ser.write("G\r\n".encode("ascii"))
        self.READY()

    def _save_wave(self, file_name):
        os.makedirs(
            "%s" % self.auto_save_savedirectory_box.get(), exist_ok=True
        )
        obj = PythonDSO.LecroyVICP(self._oshiro_ip)
        sclwt_trace = obj.get_scaled_waveform_withtime(
            "%s" % self.auto_save_chanel.get()
        )
        obj.disconnect()
        with open(
            "%s%s.txt" %
            (
                self.auto_save_savedirectory_box.get(),
                file_name
            ), "w"
        ) as file:
            file.write(
                "保存した波形 %s\r\n 1 列目は時間,2 列目は信号値\r\n \r\n" % (self.auto_save_chanel.get())
            )
            for i in range(len(sclwt_trace[1])):
                file.write(
                    "{},{}\r\n".format(
                        sclwt_trace[0][i],
                        sclwt_trace[1][i]
                    )
                )
            file.close()
        self.txt.insert(
            tk.END,
            "%s の波形を保存しました\r\n" % self.auto_save_chanel.get()
        )


def main():
    root = tk.Tk()
    app = Application(master=root)  # Applicationをインスタンス化
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # 右上のバツボタンを押したら
    app.mainloop()  # gui のための無限ループ


if __name__ == "__main__":
    main()
