import tkinter as tk
import tkinter.ttk as ttk
import datetime
import os

import TIS


class Property():
    def __init__(self, Tis=None):  # Property のクラスをインスタンス化した際に実行される関数
        self.Tis = Tis
        self.resolution_list = [
            "640x480",
            "720x480",
            "960x720",
            "1280x720",
            "1280x1024"
        ]
        self.fps_list = [
            [
                "5/1",
                "10/1",
                "30/1",
                "50/1",
                "100/1",
                "200/1",
                "300/1"
            ],  # 640x480
            [
                "5/1",
                "10/1",
                "30/1",
                "50/1",
                "100/1",
                "200/1",
                "300/1"
            ],  # 720x480
            ["5/1", "10/1", "30/1", "50/1", "100/1", "150/1"],  # 960x720
            ["5/1", "10/1", "30/1", "50/1", "100/1"],  # 1280x720
            ["5/1", "10/1", "30/1", "50/1", "90/1"]  # 1280x1024
        ]
        self.path = "./cash/property.txt"
        if not os.path.exists(self.path):  # property.txt が存在しないなら
            os.makedirs("./cash/", exist_ok=True)  # cash
            print("property.txt は存在しません．初期値を設定します．")
            self.initial_value()  # 適当に定めた初期値を適用する
        else:  # property.txt が存在するなら
            print("property.txt は存在しました．読み込みます．")
            with open(self.path, "r", encoding=("UTF-8")) as f:
                # property.txt を変数 f で開く
                data = f.readlines()  # 配列で読み込む
                # 空の配列を宣言 #
                self.p = data[1:]  # 設定値．最初の行 (0行目) は最終更新日時が記述されているため 1行目から
                self.p_name = data[1:]  # 設定値の名前
                for a in range(len(data)-1):  # 設定値だけを取得する
                    # .index("=")+2:-1 で = と \n の間にある要素を取得する
                    # +2は半角スペース -1は\n を読み込まないため．
                    self.p[a] = data[a+1][data[a+1].index("=")+2:-1]
                    # "=" の前の文字列を代入.-1は半角スペースがあるため
                    self.p_name[a] = data[a+1][:data[a+1].index("=")-1]

        # 設定をカメラに読み込ませる #
        for a in range(len(self.p)):
            self.read(self.p_name[a], self.p[a], a)

    def initial_value(self):  # 初期値の設定．Property.txt が存在しない場合，実行
        # 初期値 #
        self.exposure = 500
        self.exposure_auto = "Off"
        self.gain = 0
        self.gain_auto = "Off"
        self.trigger_mode = "Off"
        self.trigger_source = "Any"
        self.trigger_delay = 9.5
        self.trigger_debouncer = 0
        self.trigger_mask = 0
        self.trigger_noise = 0
        self.trigger_burst_count = 1
        self.trigger_act = "RisingEdge"
        # 初期値 ここまで #
        self.p = [
            self.exposure,
            self.exposure_auto,
            self.gain,
            self.gain_auto,
            self.trigger_mode,
            self.trigger_source,
            self.trigger_delay,
            self.trigger_debouncer,
            self.trigger_mask,
            self.trigger_noise,
            self.trigger_burst_count,
            self.trigger_act
        ]  # 値
        self.p_name = [
            "Resolution",
            "FPS",
            "Exposure",
            "Exposure Auto",
            "Gain",
            "Gain Auto",
            "Trigger Mode",
            "Trigger Source",
            "Trigger Delay (us)",
            "Trigger Debouncer",
            "Trigger Mask",
            "Trigger Denoise",
            "Trigger Burst Count",
            "Trigger Activation"
        ]  # 名前
        # print(len(self.p)) # 確認

    def read(self, name, parameter, n):  # カメラに設定を読みこませる関数(名前，設定値，設定の番号)
        self.p_name[n] = name
        self.p[n] = parameter
        self.Tis.Set_Property("{}".format(name), parameter)  # 設定
        # print("{} : {} : {}\n".format(name,self.
        # Tis.Get_Property("{}".format(name)).value,parameter))

    def property(self, resolution, fps):  # reslusion,fps を取得する関数
        loc = resolution.find("x")
        self.width = int(resolution[0:loc])
        self.height = int(resolution[loc+1:])
        self.fps = fps

    def return_box(self):  # main.py に self.fps の情報を返す
        return self.fps_box

    def return_property(self):  # main.py に resplution(width,height),fps の情報を返す
        return self.width, self.height, self.fps

    def test(self):
        print("hi")

    def save(self):  # property.txt の作成．
        print("save 関数を実行します")
        with open(self.path, "w", encoding=("UTF-8")) as f:  # property.txt の編集
            f.write("最終履歴 %s\n" % datetime.datetime.now())  # 作成日時の書き込み
            for a in range(len(self.p)):  # プロパティの数だけ loop
                f.write("{0} = {1}\n".format(
                    self.p_name[a], self.p[a]))  # 設定名と設定値を書き込み
        print("保存しました")

    def on_closing(self):  # 左上のバツを押したら動く関数．
        self.save()
        self.property_root.destroy()
        print("property ends")

    def gui(self):
        color = "#D2ffD2"  # Light Green
        # property root #
        self.property_root = tk.Tk()
        self.property_root.title(u"PROPERTY")  # タイトル
        # 左上のバツを押したら，on_closing関数を行う．
        self.property_root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # property frame #
        self.exposure_frame = tk.LabelFrame(
            self.property_root,
            width=500,
            height=175,
            bg="white",
            relief="groove",
            bd=10,
            text="Exposure"
        )
        self.exposure_frame.grid(row=0, column=0)
        # self.exposure_frame.grid_propagate(False)
        # Trigger frame
        self.trigger_frame = tk.LabelFrame(
            self.property_root,
            width=500,
            height=500,
            bg="white",
            relief="groove",
            bd=10,
            text="Trigger"
        )
        self.trigger_frame.grid(row=1, column=0)

        # resolution #
        self.resolution_label = tk.Label(
            self.exposure_frame,
            text="Resolution",
            bg=color
        )
        self.resolution_label.grid(row=0, column=0, sticky=tk.E+tk.W)
        self.resolution_box = ttk.Combobox(
            self.exposure_frame,
            textvariable=self.resolution_list,
            # ttk.Combobox(場所,変数,変数の内容,幅)
            values=self.resolution_list, width=10
        )
        self.resolution_box.set(self.resolution_list[-1])
        self.resolution_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.fps_box.config(
                # Combobox を選択したら，self.fps_boxの中身を変更
                value=self.fps_list[
                    self.resolution_list.index(self.resolution_box.get())
                    ][:]
            )
        )
        self.resolution_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.fps_box.set("SELECT FPS"),
            "+"
        )  # Combobox を選択したら，self.fps_box にSELECT FPS を表示
        self.resolution_box.grid(row=0, column=2)  # Combobox の配置

        # fps #
        self.fps_label = tk.Label(self.exposure_frame, text="FPS", bg=color)
        self.fps_label.grid(row=1, column=0, sticky=tk.E+tk.W)
        self.fps_box = ttk.Combobox(
            self.exposure_frame,
            textvariable=self.fps_list,
            # ttk.Combobox(場所,変数,変数の内容,幅)
            values=self.fps_list[-1][:], width=10
        )
        self.fps_box.set(self.fps_list[-1][1])
        self.fps_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.property(
                # Combobox を選択したら，self.property 関数を実行
                self.resolution_box.get(), self.fps_box.get()
            )
        )
        self.fps_box.grid(row=1, column=2)  # Combobox の配置

        # exposure #
        # exposure value
        self.exposure = tk.IntVar()  # 変数(整数)
        self.exposure_label = tk.Label(
            # tk.Label(場所,ラベルの内容,背景色)
            self.exposure_frame,
            text="Exposure (us)",
            bg=color
        )
        self.exposure_label.grid(row=2, column=0, sticky=tk.E+tk.W)  # ラベルの配置
        self.exposure_scale = tk.Scale(
            self.exposure_frame,
            variable=self.exposure,
            from_=50,
            to=1e7,
            length=256,
            resolution=1,
            orient=tk.HORIZONTAL,
            showvalue=False,
            # tk.scale(場所,変数,最小値,最大値,幅,値幅,scaleの方向,値を非表示にする)
            )
        self.exposure_scale.bind(
            "<B1-Motion>",
            lambda event: self.read(
                "Exposure",
                self.exposure_scale.get(
                    # クリックしたら，self.read(設定名，設定値，設定番号) 関数を実行
                    ), self.p_name.index("Exposure")
            )
        )
        # scale の初期値設定．self.p の値を参照
        self.exposure_scale.set(self.p[self.p_name.index("Exposure")])
        self.exposure_scale.grid(row=2, column=1)  # scale の配置
        self.exposure_entry = tk.Entry(
            # tk.Entry(場所,変数,幅)
            self.exposure_frame, textvariable=self.exposure,
            width=10
        )
        self.exposure_entry.bind(
            "<Return>",
            lambda event: self.read(
                "Exposure",
                self.exposure_scale.get(),
                self.p_name.index("Exposure")
            )
        )
        self.exposure_entry.grid(row=2, column=2)  # Entry の配置

        # Exposure Auto
        self.exposure_auto = tk.StringVar(value="OFF")  # 変数(文字)
        self.exposure_auto_label = tk.Label(
            self.exposure_frame,
            text="Exposure Auto",
            bg=color
        )
        self.exposure_auto_label.grid(row=3, column=0)
        self.exposure_auto_box = ttk.Combobox(
            self.exposure_frame,
            textvariable=self.exposure_auto,
            values=[
                # ttk.Combobox(場所,変数,変数の内容,幅)
                "Continuous", "Off"
                ],
            width=10
        )
        self.exposure_auto_box.set(self.p[self.p_name.index("Exposure Auto")])
        self.exposure_auto_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.read(
                # Combobox を選択したら，self.read() 関数を実行
                "Exposure Auto",
                self.exposure_auto_box.get(),
                self.p_name.index("Exposure Auto")
            )
        )
        self.exposure_auto_box.grid(row=3, column=2)  # Combobox の配置

        # Gain #
        # gain value
        self.gain = tk.DoubleVar(value=5)
        self.gain_label = tk.Label(
            self.exposure_frame, text="Gain (dB)", bg=color)
        self.gain_label.grid(row=4, column=0, sticky=tk.E+tk.W)
        self.gain_scale = tk.Scale(
            self.exposure_frame,
            variable=self.gain,
            from_=0,
            to=9.2,
            length=256,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            showvalue=False,
        )
        self.gain_scale.bind(
            "<B1-Motion>",
            lambda event: self.read(
                "Gain",
                self.gain_scale.get(),
                self.p_name.index("Gain")
            )
        )
        self.gain_scale.set(self.p[self.p_name.index("Gain")])
        self.gain_scale.grid(row=4, column=1)
        self.gain_entry = tk.Entry(
            self.exposure_frame,
            textvariable=self.gain,
            width=10
        )
        self.gain_entry.bind(
            "<Return>",
            lambda event: self.read(
                "Gain",
                self.gain_scale.get(),
                self.p_name.index("Gain")
            )
        )
        self.gain_entry.grid(row=4, column=2)
        # gain auto
        self.gain_auto = tk.StringVar(value="False")
        self.gain_auto_label = tk.Label(
            self.exposure_frame,
            text="Gain Auto",
            bg=color
        )
        self.gain_auto_label.grid(row=5, column=0, sticky=tk.E+tk.W)
        self.gain_auto_box = ttk.Combobox(
            self.exposure_frame,
            textvariable=self.gain_auto,
            values=["Continuous", "Off"],
            width=10
        )
        self.gain_auto_box.set(self.p[self.p_name.index("Gain Auto")])
        self.gain_auto_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.read(
                "Gain Auto",
                self.gain_auto_box.get(),
                self.p_name.index("Gain Auto")
            )
        )
        self.gain_auto_box.grid(row=5, column=2)

        # save #
        # self.file_name = tk.StringVar(value = "save_property (拡張子不要)")
        # self.file_button = tk.Button(self.exposure_frame,text =
        # "SAVE",command = self.save) # tk.Button(場所,名前,対応する関数)
        # self.file_button.grid(row = 6,column = 0) # bottun の配置

        # trigger_frame #
        # trigger #
        # Triger Mode
        self.trigger_mode = tk.StringVar(value="On")
        self.trigger_label = tk.Label(
            self.trigger_frame,
            text="Mode",
            bg=color
        )
        self.trigger_label.grid(row=0, column=0, sticky=tk.E+tk.W)
        self.trigger_box = ttk.Combobox(
            self.trigger_frame,
            textvariable=self.trigger_mode,
            values=["On", "Off"],
            width=10
        )
        self.trigger_box.set(self.p[self.p_name.index("Trigger Mode")])
        self.trigger_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.read(
                "Trigger Mode",
                self.trigger_box.get(),
                self.p_name.index("Trigger Mode")
            )
        )
        self.trigger_box.grid(row=0, column=2)

        # Trigger Source
        self.trigger_source = tk.StringVar(value="Any")
        self.trigger_source_label = tk.Label(
            self.trigger_frame, text="Source", bg=color)
        self.trigger_source_label.grid(row=1, column=0, sticky=tk.E+tk.W)
        self.trigger_source_box = ttk.Combobox(
            self.trigger_frame,
            textvariable=self.trigger_source,
            values=["Any", "Line1", "Software"],
            width=10
        )
        self.trigger_source_box.set(
            self.p[self.p_name.index("Trigger Source")]
        )
        self.trigger_source_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.read(
                "Trigger Source",
                self.trigger_source_box.get(),
                self.p_name.index("Trigger Source")
            )
        )
        self.trigger_source_box.grid(row=1, column=2)
        # Trigger Activarion
        self.trigger_act = tk.StringVar(value="RisingEdge")
        self.trigger_act_label = tk.Label(
            self.trigger_frame, text="Activation", bg=color)
        self.trigger_act_label.grid(row=3, column=0, sticky=tk.E+tk.W)
        self.trigger_act_box = ttk.Combobox(
            self.trigger_frame,
            textvariable=self.trigger_act,
            values=["RisingEdge", "FallingEdge"],
            width=10
        )
        self.trigger_act_box.set(
            self.p[self.p_name.index("Trigger Activation")]
        )
        self.trigger_act_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.read(
                "Trigger Activation",
                self.trigger_act_box.get(),
                self.p_name.index("Trigger Activation")
            )
        )
        self.trigger_act_box.grid(row=3, column=2)
        # Trigger Delay
        self.trigger_delay = tk.DoubleVar(value=0)  # 変数(浮動小数点)
        self.trigger_delay_label = tk.Label(
            self.trigger_frame,
            text="Delay (us)",
            bg=color
        )
        self.trigger_delay_label.grid(row=4, column=0, sticky=tk.E+tk.W)
        self.trigger_delay_scale = tk.Scale(
            self.trigger_frame,
            variable=self.trigger_delay,
            from_=0,
            to=1e6,
            length=256,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            showvalue=False,
        )
        self.trigger_delay_scale.bind(
            "<B1-Motion>",
            lambda event: self.read(
                "Trigger Delay (us)",
                self.trigger_delay_scale.get(),
                self.p_name.index("Trigger Delay (us)")
            )
        )
        self.trigger_delay_scale.set(
            self.p[self.p_name.index("Trigger Delay (us)")]
        )
        self.trigger_delay_scale.grid(row=4, column=1)
        self.trigger_delay_entry = tk.Entry(
            self.trigger_frame,
            textvariable=self.trigger_delay,
            width=10
        )
        self.trigger_delay_entry.bind(
            "<Return>",
            lambda event: self.read(
                "Trigger Delay (us)",
                self.trigger_delay_scale.get(),
                self.p_name.index("Trigger Delay (us)")
            )
        )
        self.trigger_delay_entry.grid(row=4, column=2)
        # Trigger Debounce Time Min 0s / Max 1s
        self.trigger_debouncer = tk.DoubleVar(value=0)
        self.trigger_debouncer_label = tk.Label(
            self.trigger_frame, text="Debounce Time", bg=color)
        self.trigger_debouncer_label.grid(row=5, column=0, sticky=tk.E+tk.W)
        self.trigger_debouncer_scale = tk.Scale(
            self.trigger_frame,
            variable=self.trigger_debouncer,
            from_=0,
            to=1e6,
            length=256,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            showvalue=False,
        )
        self.trigger_debouncer_scale.bind(
            "<B1-Motion>",
            lambda event: self.read(
                "Trigger Debouncer",
                self.trigger_debouncer_scale.get(),
                self.p_name.index("Trigger Debouncer")
            )
        )
        self.trigger_debouncer_scale.set(
            self.p[self.p_name.index("Trigger Debouncer")]
        )
        self.trigger_debouncer_scale.grid(row=5, column=1)
        self.trigger_debouncer_entry = tk.Entry(
            self.trigger_frame,
            textvariable=self.trigger_debouncer,
            width=10
        )
        self.trigger_debouncer_entry.bind(
            "<Return>",
            lambda event: self.read(
                "Trigger Debouncer",
                self.trigger_debouncer_scale.get(),
                self.p_name.index("Trigger Debouncer")
            )
        )
        self.trigger_debouncer_entry.grid(row=5, column=2)
        # Trigger Mask Time Min 0s / Max 1s
        self.trigger_mask = tk.DoubleVar(value=0)
        self.trigger_mask_label = tk.Label(
            self.trigger_frame,
            text="Mask Time",
            bg=color
        )
        self.trigger_mask_label.grid(row=6, column=0, sticky=tk.E+tk.W)
        self.trigger_mask_scale = tk.Scale(
            self.trigger_frame,
            variable=self.trigger_mask,
            from_=0,
            to=1e6,
            length=256,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            showvalue=False,
        )
        self.trigger_mask_scale.bind(
            "<B1-Motion>",
            lambda event: self.read(
                "Trigger Mask",
                self.trigger_mask_scale.get(),
                self.p_name.index("Trigger Mask")
            )
        )
        self.trigger_mask_scale.set(self.p[self.p_name.index("Trigger Mask")])
        self.trigger_mask_scale.grid(row=6, column=1)
        self.trigger_mask_entry = tk.Entry(
            self.trigger_frame,
            textvariable=self.trigger_mask,
            width=10
        )
        self.trigger_mask_entry.bind(
            "<Return>",
            lambda event: self.read(
                "Trigger Mask",
                self.trigger_mask_scale.get(),
                self.p_name.index("Trigger Mask")
            )
        )
        self.trigger_mask_entry.grid(row=6, column=2)
        # Trigger Noise Suppression Time Min 0s /Max 1s
        self.trigger_noise = tk.DoubleVar(value=1)
        self.trigger_noise_label = tk.Label(
            self.trigger_frame,
            text="Noise Suppression Time",
            bg=color
        )
        self.trigger_noise_label.grid(row=7, column=0, sticky=tk.E+tk.W)
        self.trigger_noise_scale = tk.Scale(
            self.trigger_frame,
            variable=self.trigger_noise,
            from_=0,
            to=1e5,
            length=256,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            showvalue=False,
        )
        self.trigger_noise_scale.bind(
            "<B1-Motion>",
            lambda event: self.read(
                "Trigger Denoise",
                self.trigger_noise_scale.get(),
                self.p_name.index("Trigger Denoise")
            )
        )
        self.trigger_noise_scale.set(
            self.p[self.p_name.index("Trigger Denoise")]
        )
        self.trigger_noise_scale.grid(row=7, column=1)
        self.trigger_noise_entry = tk.Entry(
            self.trigger_frame,
            textvariable=self.trigger_noise,
            width=10
        )
        self.trigger_noise_entry.bind(
            "<Return>",
            lambda event: self.read(
                "Trigger Denoise",
                self.trigger_noise_scale.get(),
                self.p_name.index("Trigger Denoise")
            )
        )
        self.trigger_noise_entry.grid(row=7, column=2)
        # Trigger Burst Count
        self.trigger_burst_count = tk.IntVar(value=1)
        self.trigger_burst_count_label = tk.Label(
            self.trigger_frame,
            text="Burst Count",
            bg=color
        )
        self.trigger_burst_count_label.grid(row=8, column=0, sticky=tk.E+tk.W)
        self.trigger_burst_count_scale = tk.Scale(
            self.trigger_frame,
            variable=self.trigger_burst_count,
            from_=1,
            to=1000,
            length=256,
            resolution=1,
            orient=tk.HORIZONTAL,
            showvalue=False,
        )
        self.trigger_burst_count_scale.bind(
            "<B1-Motion>",
            lambda event: self.read(
                "Trigger Burst Count",
                self.trigger_burst_count_scale.get(),
                self.p_name.index("Trigger Burst Count")
            )
        )
        self.trigger_burst_count_scale.set(
            self.p[self.p_name.index("Trigger Burst Count")]
        )
        self.trigger_burst_count_scale.grid(row=8, column=1)
        self.trigger_burst_count_entry = tk.Entry(
            self.trigger_frame,
            textvariable=self.trigger_burst_count,
            width=10
        )
        self.trigger_burst_count_entry.bind(
            "<Return>",
            lambda event: self.read(
                "Trigger Burst Count",
                self.trigger_burst_count_scale.get(),
                self.p_name.index("Trigger Burst Count")
            )
        )
        self.trigger_burst_count_entry.grid(row=8, column=2)


def main():
    # root = tk.Tk()
    Tis = TIS.TIS()
    app = Property(Tis)
    # root.protocol("WM_DELETE_WINDOW",app.on_closing)
    # # 左上のバツを押したら，on_closing関数を行う．
    app.mainloop()  # tkinter をループする．


if __name__ == "__main__":
    main()
