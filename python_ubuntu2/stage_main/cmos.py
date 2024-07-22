# CMOS カメラのプログラム
# TIS.py，profile.py および property.py を同じディレクトリに配置すること
# CMOS カメラとは シリアル番号で通信を行う
# シリアル番号は tcam-ctrl -l で確認できる

# import sys
# import time
import cv2  # カメラ
# import PIL.Image
# import PIL.ImageTk  # カメラ
# import numpy as np
import os
# gui 関係 #
import tkinter as tk
# import tkinter.ttk as ttk
# from tkinter import filedialog  # save に用いる

# TIS #
import TIS
# from collections import namedtuple

# original #
from python_ubuntu2.stage_main.property import Property


class CustomData:
    ''' Example class for user data passed to
 the on new image callback function '''

    def __init__(self, newImageReceived, image):
        self.newImageReceived = newImageReceived
        self.image = image
        self.busy = False


class Cmos(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master  # root
        self.width = 960
        self.height = 720
        self.count = 0  # FPS 用
        self.max_count = 10
        self.judge = False
        self.ave_judge = False
        self.t = cv2.TickMeter()  # FPS 用
        self.t.start()

        self.path = "./capture/"
        self.name = "test"
        if not os.path.exists(self.path):  # property.txt が存在しないなら
            os.makedirs(self.path, exist_ok=True)  # cash
            print("property.txt は存在しません．初期値を設定します．")
            # 適当に定めた初期値を適用する
        else:  # property.txt が存在するなら
            print("pathは存在します")
        self.CD = CustomData(False, None)  # CustomData をインスタンス化
        self.Tis = TIS.TIS()  # TIS.py をインスタンス化
        self.Tis.openDevice("27810554", self.width, self.height,
                            "30/1", TIS.SinkFormats.GRAY8, False)  # カメラに接続
        self.Tis.Set_Image_Callback(self.on_new_image, self.CD)  # 必須．よくわからない
        self.CD.busy = True  # CMOS カメラが ready
        self.Tis.Start_pipeline()  # パイプラインの構築
        self.Tis.Set_Property("Trigger Mode", "OFF")  # 設定
        print(self.Tis.Get_Property("Trigger Source").value)  # 設定確認
        cv2.waitKey(1000)  # 1 秒待機．よくわからない．
        self.CD.busy = False  # CMOS カメラが busy

        # property.py #
        self.property = Property(self.Tis)  # インスタンス化

    def on_new_image(self, tis, userdata):  # イメージを取得する関数
        '''
        Callback function, which will be called by the TIS class
        :param tis: the camera TIS class, that calls this callback
        :param userdata: This is a class with user data, filled by this call.
        :return:
        '''
        self.userdata = userdata
        # Avoid being called, while the callback is busy
        if self.userdata.busy is True:
            return

        self.userdata.busy = True
        self.userdata.newImageReceived = True
        self.userdata.image = tis.Get_image()
        self.userdata.busy = False

    def define(self):  # self.loop_capture_A を定義する関数
        pass
    # main.py の処理 #

    def capture(self):
        if self.CD.newImageReceived is False:
            # CD.newImageReceived が True になるまでx待機する loop
            # print("no image received")
            self.loop_capture = self.master.after(
                10, self.capture)  # 1 ms capture_A を繰り返す．
        else:  # loop から抜け出したら
            self.CD.newImageReceived = False
            self.img = cv2.resize(self.CD.image[:, :, 0], dsize=(1000, 800))
            cv2.imshow("capture", self.CD.image[:, :, 0])
            self.count += 1  # FPS カウンター
            if self.count == self.max_count:  # FPS 用．1 秒経過したら
                self.t.stop()
                # print("fps")
                self.t.reset()
                self.t.start()
                self.count = 0  # self.count のリセット
            if (self.ave_judge is True):
                self.ave = self.ave + self.CD.image[:, :, 0].astype("uint16")
                print(self.ave[100, 100], self.CD.image[100, 100, 0])
                self.ave_count += 1
                if self.ave_count == 100:
                    self.ave = self.ave/100
                    print(self.ave[100, 100])
                    self.ave_judge = False
                    self.save(self.path, self.name)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                self.master.after_cancel(
                    self.loop_capture)  # loop_capture_A を停止
                print("終了")
        # self.loop_capture = self.master.after(1,self.capture)
        # # 1 ms capture_A を繰り返す

    def average(self, path, name):
        print("average")
        self.ave_judge = True
        self.ave = 0
        self.ave_count = 0
        self.path = path
        self.name = name+"_average"

    def property_function(self):
        self.property.gui()  # property の gui 表示
        self.fps_box = self.property.return_box()  # fps_box の取得
        # fps_box と property_get 関数の結びつけ
        self.fps_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.property_get(), "+"
        )

    def property_get(self):
        self.width, self.height, self.fps = self.property.return_property()
        # resolution,fps の取得
        print(self.width, self.height, self.fps)
        self.device(self.width, self.height, self.fps)  # device 関数

    def device(self, width, height, fps):  # resolution,fps を設定する関数．
        self.Tis.Stop_pipeline()  # パイプラインの停止
        self.Tis.openDevice("27810554", width, height, "{}".format(
            # resolution(width,height),fps の設定．再び接続する．
            fps), TIS.SinkFormats.GRAY8, False)
        self.Tis.Set_Image_Callback(self.on_new_image, self.CD)  # 必須．よくわからない
        self.CD.busy = True  # CMOS カメラが ready
        self.Tis.Start_pipeline()  # パイプラインの構築
        self.Tis.Set_Property("Trigger Mode", "OFF")  # 設定
        print(self.Tis.Get_Property("Trigger Source").value)  # 設定確認
        cv2.waitKey(1000)  # 1 秒待機．よくわからない．
        self.CD.busy = False  # CMOS カメラが busy
        # カメラの設定 ここまで #
        # property.py end #

    def save(self, path, name):  # 映像のスナップショット用の関数．修正箇所
        if not os.path.exists(path):  # property.txt が存在しないなら
            os.makedirs(path, exist_ok=True)  # cash
            print("pathを作成しました")
            # 適当に定めた初期値を適用する
        else:  # property.txt が存在するなら
            print("pathは存在します")

        print(path, name)
        cv2.imwrite(path+name+".png", self.CD.image[:, :, 0])  # image を保存
        print("saveしました")

    def property_text(self):
        return self.property.p, self.property.p_name

    def on_closing(self):  # 左上のバツを押したら動く関数．
        if self.judge is True:
            self.master.after_cancel(self.loop_capture)  # loop_capture_A を停止
            self.master.after_cancel(self.loop_capture_A)
        self.Tis.Stop_pipeline()  # CMOS カメラとの通信終了
        cv2.destroyAllWindows()
        # self.master.destroy() # gui を閉じる
        print("program ends")
        # sys.exit() # プログラム終了


def main():  # はじめに動く関数
    root = tk.Tk()  # root を定義
    app = Application(master=root)  # Applicationをインスタンス化．
    # 左上のバツを押したら，on_closing関数を行う．
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()  # 処理がない時，受付待機状態となりプログラムが終了するまで loop する．


# app =Application()
if __name__ == "__main__":  # python3 main.py でこのプログラムを動かしたら
    main()
