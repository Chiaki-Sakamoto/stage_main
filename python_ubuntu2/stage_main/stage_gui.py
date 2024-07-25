import tkinter as tk  # gui
import tkinter.ttk as ttk
from tkinter import font
# from tkinter import messagebox
# from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os


class Gui(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.font = font.Font(family="Helvetica", size=10)  # Guiのフォント
        self.color = "#D2ffD2"  # nbの色 R210 G255 B210
        self.color_b = "#bebeff"  # nbのボタン R255 G190 B190 (使っていない)
        self.style = ttk.Style()  # nb_Tabの設定
        self.style.configure(
            "example.TNotebook",
            tabposition=tk.N,
        )  # Tab の位置設定
        self.style.configure(
            "example.TNotebook.Tab",
            font=self.font)  # Tabのフォント
        self.style.map("example.TNotebook.Tab", foreground=[
            ('active', 'red'),
            ('disabled', 'gray'),
            ('selected', 'white'),], background=[
                ('active', 'white'),
                ('disabled', 'gray'),
                ('selected', 'blue'),])  # ボタンの色設定
        self.gui()

    def test(self):
        print("test")

    def directory(self):
        self.iDir = os.path.abspath(os.path.dirname(__file__))
        self.iDirPath = filedialog.askdirectory(initialdir=self.iDir)
        self.dirname.set(self.iDirPath+"/")

    def gui(self):
        # root #
        self.master.configure(background='Light Green')  # Gui の色
        self.master.title(u"Stage Control_ver3")  # タイトル
        self.bg = self.master.cget("background")
        self.master.geometry("750x1000")  # サイズ
        # Note Book #
        self.nb = ttk.Notebook(
            self.master,
            width=500,
            height=300,
            style="example.TNotebook"
        )  # nbの定義
        self.nb.grid(row=0, column=0, sticky=tk.S+tk.N)  # nbの場所
        self.nb.grid_propagate(False)  # 自動で大きさを変更しない
        # txt Frame #
        self.txtframe = tk.Frame(
            self.master, width=250, height=360, bg="gray85")  # rogframe を作成
        self.txtframe.grid(row=0, column=1)  # txtframe の配置
        self.txtframe.grid_propagate(False)  # 自動で大きさを変更しない
        # Graph frame #
        self.graphframe = tk.Frame(
            self.master,
            width=600,
            height=500,
            bg="white",
            relief="groove",
            bd=10
        )
        self.graphframe.grid(row=1, columnspan=2, pady=50)  # graphframeの 配置
        self.graphframe.grid_propagate(False)  # 自動で大きさを変更しない
        # Figure instance
        self.fig, self.ax = plt.subplots(1)  # figure の作成
        # ax1.set_title('Experiment Data')
        self.ax.set_xlabel("Angle (degree)", fontsize=15)  # 横軸
        self.ax.set_ylabel('Voltage (mV)', fontsize=15)  # 縦軸
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
        self.ax.set_title("Angle distribution", fontsize=15)  # タイトル
        self.ax.set_xlim(0, 80)  # 横軸の範囲
        self.ax.set_ylim(0, 60)  # 縦軸の範囲
        # Canvas matplotlib と tkinter を結びつけるもの
        # Generate canvas instance, Embedding fig in master
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphframe)
        self.canvas.get_tk_widget().pack()  # canvas の配置
        # gui に用いる変数 #
        self.angle = tk.StringVar()  # 現在の角度を示す変数
        self.now_pressure = tk.StringVar()  # 現在の角度を示す変数
        self.hantei = tk.StringVar()  # 強制終了に用いる
        self.dirname = tk.StringVar()
        self.C = tk.StringVar()
        self.ex_C = tk.StringVar()  # 変数
        # NoteBook の追加 #
        self.gui_stage()
        self.gui_oshiro()
        self.gui_camera()
        self.gui_ex()
        self.gui_auto_save()

    # tab_stage (回転ステージ) #
    def gui_stage(self):
        self.tab_stage = tk.Frame(self.nb)  # Tab を定義
        self.nb.add(self.tab_stage, text="回転ステージ")  # Tab の配置、名前
        self.speedframe = tk.LabelFrame(
            self.tab_stage,
            text="速度設定",
            font=self.font,
            height=170,
            width=500,
            bg=self.color
        )  # frame
        self.speedframe.grid(row=0, column=0, sticky=tk.E+tk.W)
        self.speedframe.grid_propagate(False)
        self.speed_s = tk.Label(
            self.speedframe,
            text="最小速度\n(1~200)",
            font=self.font,
            bg=self.color
        )  # label
        self.speed_s.grid(row=0, column=0, padx=10, pady=20)
        self.speed_s_box = tk.Entry(
            self.speedframe,
            width=5,
            font=self.font
        )  # txtbox
        self.speed_s_box.grid(row=1, column=0)
        self.speed_s_box.insert(tk.END, "100")
        self.speed_f = tk.Label(
            self.speedframe,
            text="最大速度\n(1~1000?)",
            font=self.font,
            bg=self.color
        )  # label
        self.speed_f.grid(row=0, column=1, padx=10)
        self.speed_f_box = tk.Entry(
            self.speedframe,
            width=5,
            font=self.font
        )  # txtbox
        self.speed_f_box.grid(row=1, column=1)
        self.speed_f_box.insert(tk.END, "1000")
        self.speed_r = tk.Label(
            self.speedframe,
            text="加減速時間\n(0~1000)",
            font=self.font,
            bg=self.color
        )  # label
        self.speed_r.grid(row=0, column=2, padx=10)
        self.speed_r_box = tk.Entry(
            self.speedframe,
            width=5,
            font=self.font
        )  # txtbox
        self.speed_r_box.grid(row=1, column=2)
        self.speed_r_box.insert(tk.END, "200")
        self.speed_B = tk.Button(
            self.speedframe,
            text="速度変更",
            width=10,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )  # button
        self.speed_B.grid(row=0, rowspan=2, column=3, padx=30)
        self.exeframe_1 = tk.LabelFrame(
            self.tab_stage,
            width=500,
            height=170,
            bg=self.color,
            relief="groove",
            bd=10
        )  # frame
        self.exeframe_1.grid(row=1, column=0)
        self.exeframe_1.grid_propagate(False)
        self.thetala = tk.Label(
            self.exeframe_1,
            text=u"回転角度",
            font=self.font,
            bg=self.color
        )  # label
        self.thetala.grid(row=0, column=0, padx=10, pady=20)
        self.thetabox = tk.Entry(
            self.exeframe_1,
            width="5",
            font=self.font
        )  # txtbox
        self.thetabox.insert(tk.END, "0")
        self.thetabox.grid(row=0, column=1)
        self.Run_B = tk.Button(
            self.exeframe_1,
            text=u"RUN",
            width=15,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )  # button
        self.Run_B.grid(row=1, column=0)
        self.restart = tk.Button(
            self.exeframe_1,
            text=u"原点回帰",
            width=15,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )  # button
        self.restart.grid(row=1, column=1)
        self.now_theta = tk.Label(
            self.exeframe_1,
            text=u"現在の角度",
            font=self.font,
            bg=self.color
        )  # label
        self.now_theta.grid(row=0, column=2, padx=20)
        self.now_theta_txt = tk.Label(
            self.exeframe_1,
            textvariable=self.angle,
            bg=self.color
        )  # txtbox
        self.now_theta_txt.grid(row=0, column=3)
        self.StatusNamelabel = tk.Label(
            self.exeframe_1,
            text=u"status",
            font=self.font,
            bg=self.color
        )  # label
        self.StatusNamelabel.grid(row=1, column=2)
        self.Statuslabel = tk.Label(
            self.exeframe_1,
            text=u"   ",
            bg="green"
        )  # label
        self.Statuslabel.grid(row=1, column=3)

    # オシロスコープ #
    def gui_oshiro(self):
        self.tab_oshiro = tk.Frame(self.nb)
        self.nb.add(self.tab_oshiro, text="オシロスコープ")
        self.saveframe = tk.LabelFrame(
            self.tab_oshiro,
            width=500,
            height=170,
            bg=self.color
        )  # frame
        self.saveframe.grid(row=0, column=0)
        self.saveframe.grid_propagate(False)
        self.savedirectory = tk.Label(
            self.saveframe,
            text="保存先のディレクトリ",
            font=self.font,
            bg=self.color)  # labelS
        self.savedirectory.grid(
            row=0,
            column=0,
            padx=10,
            pady=(10, 5),
            sticky=tk.W
        )
        self.savedirectory_box = tk.Entry(
            self.saveframe,
            width=40,
            textvariable=self.dirname
        )  # txtbox
        self.savedirectory_box.grid(row=1, column=0)
        self.dirname.set("./experiment/1229/")
        self.sansyou = tk.Button(
            self.saveframe,
            text="参照",
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )
        self.sansyou.bind("<Button-1>", lambda event: self.directory())
        self.sansyou.grid(row=1, column=1)
        self.savename = tk.Label(
            self.saveframe,
            text="保存するファイル名(拡張子不要)",
            font=self.font,
            bg=self.color
        )  # label
        self.savename.grid(row=2, column=0, padx=10, pady=(10, 5), sticky=tk.W)
        self.savename_box = tk.Entry(self.saveframe, width=40)  # txtbox
        self.savename_box.grid(row=3, column=0)
        self.savename_box.insert(tk.END, "test")
        self.exeframe_2 = tk.LabelFrame(
            self.tab_oshiro,
            width=500,
            height=170,
            bg=self.color,
            relief="groove",
            bd=10
        )  # frame
        self.exeframe_2.grid(row=1, column=0)
        self.exeframe_2.grid_propagate(False)
        self.chanelname = tk.Label(
            self.exeframe_2,
            text=u"保存する波形",
            font=self.font,
            bg=self.color)  # label
        self.chanelname.grid(row=0, column=0, padx=10, pady=60)
        self.chanel = ttk.Combobox(
            self.exeframe_2,
            textvariable=self.C,
            values=["C1", "C2", "C3", "C4"],
            width=5,
            font=self.font
        )  # combobox
        self.chanel.set("C1")
        self.chanel.grid(row=0, column=1, padx=10)  # ,sticky=tkinter.S)
        self.save_B = tk.Button(
            self.exeframe_2,
            text=u"波形の保存",
            width=15,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )  # button
        self.save_B.grid(row=0, column=3, padx=50)

    # CMOS カメラ #
    def gui_camera(self):
        self.tab_camera = tk.Frame(self.nb)
        self.nb.add(self.tab_camera, text="CMOS カメラ")
        self.cameraframe = tk.Frame(
            self.tab_camera,
            width=500,
            height=300,
            bg=self.color,
            relief="groove",
            bd=10
        )  # frame
        self.cameraframe.grid(row=0, column=0)
        self.cameraframe.grid_propagate(False)
        self.property_B = tk.Button(
            self.cameraframe,
            text="プロパティ",
            width=15,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )
        self.property_B.grid(row=0, column=0, padx=50)
        self.image_B = tk.Button(
            self.cameraframe,
            text="イメージ",
            width=15,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )
        self.image_B.grid(row=0, column=1, padx=50)
        self.image_savedirectory = tk.Label(
            self.cameraframe,
            text=u"保存先のディレクトリ",
            font=self.font,
            bg=self.color
        )  # label
        self.image_savedirectory.grid(
            row=1,
            column=0,
            pady=(10, 5),
            sticky=tk.W
        )
        self.image_savedirectory_box = tk.Entry(
            self.cameraframe,
            width=30,
            textvariable=self.dirname
        )  # txtbox
        self.image_savedirectory_box.grid(row=2, column=0, pady=10)
        self.image_sansyou = tk.Button(
            self.cameraframe,
            text="参照",
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )
        self.image_sansyou.bind("<Button-1>", lambda event: self.directory())
        self.image_sansyou.grid(row=1, column=0, padx=(100, 5))
        self.image_savename = tk.Label(
            self.cameraframe,
            text=u"保存するファイル名(拡張子不要)",
            font=self.font,
            bg=self.color)  # label
        self.image_savename.grid(row=3, column=0, pady=(10, 5), sticky=tk.W)
        self.image_savename_box = tk.Entry(
            self.cameraframe,
            width=30
        )  # txtbox
        self.image_savename_box.grid(row=4, column=0, pady=10)
        self.image_savename_box.insert(tk.END, "test")
        self.image_save_B = tk.Button(
            self.cameraframe,
            text="保存",
            width=15,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )
        self.image_save_B.grid(row=1, column=1, rowspan=4, padx=50)
        self.ave_B = tk.Button(
            self.cameraframe,
            text="AVERAGE",
            width=15,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )  # button
        self.ave_B.grid(row=4, column=1)

    # 実験 #
    def gui_ex(self):
        self.tab_ex = tk.Frame(self.nb)
        self.nb.add(self.tab_ex, text="実験")
        self.ex_setframe = tk.LabelFrame(
            self.tab_ex,
            width=250,
            height=220,
            text="初期設定",
            font=self.font,
            bg=self.color
        )  # frame
        self.ex_setframe.grid(row=0, column=0)
        self.ex_setframe.grid_propagate(False)
        self.ex_start = tk.Label(
            self.ex_setframe,
            text="開始角度",
            font=self.font,
            bg=self.color
        )  # label
        self.ex_start.grid(row=0, column=0, padx=5, pady=10)
        self.ex_start_box = tk.Entry(
            self.ex_setframe,
            width=3,
            font=self.font
        )  # txtbox
        self.ex_start_box.grid(row=0, column=1, padx=10)
        self.ex_start_box.insert(tk.END, "-30")
        self.ex_end = tk.Label(
            self.ex_setframe,
            text="終了角度",
            font=self.font,
            bg=self.color
        )  # label
        self.ex_end.grid(row=1, column=0, pady=10)
        self.ex_end_box = tk.Entry(
            self.ex_setframe,
            width=3,
            font=self.font
        )  # txtbox
        self.ex_end_box.grid(row=1, column=1)
        self.ex_end_box.insert(tk.END, "30")
        self.ex_width = tk.Label(
            self.ex_setframe,
            text="角度幅",
            font=self.font,
            bg=self.color
        )  # label
        self.ex_width.grid(row=2, column=0, pady=10)
        self.ex_width_box = tk.Entry(
            self.ex_setframe,
            width=3,
            font=self.font
        )  # txtbox
        self.ex_width_box.grid(row=2, column=1)
        self.ex_width_box.insert(tk.END, "1")
        self.ex_chanelname = tk.Label(
            self.ex_setframe,
            text="保存する波形",
            font=self.font,
            bg=self.color)  # label
        self.ex_chanelname.grid(row=3, column=0, pady=10)
        self.ex_chanel = ttk.Combobox(
            self.ex_setframe,
            textvariable=self.ex_C,
            values=["C1", "C2", "C3", "C4"],
            width=3,
            font=self.font
        )  # txtbox
        self.ex_chanel.set("C3")
        self.ex_chanel.grid(row=3, column=1, padx=10)
        self.pixel = tk.Label(
            self.ex_setframe,
            text="プロット範囲",
            font=self.font,
            bg=self.color
        )  # label
        self.pixel.grid(row=4, column=0, pady=10)
        self.pixel_box_1 = tk.Entry(
            self.ex_setframe,
            width=5,
            font=self.font
        )  # txtbox
        self.pixel_box_1.grid(row=4, column=1)
        self.pixel_box_1.insert(tk.END, "49000")
        self.pixel_range = tk.Label(
            self.ex_setframe,
            text="~",
            font=self.font,
            bg=self.color
        )
        self.pixel_range.grid(row=4, column=2, sticky=tk.W+tk.E)
        self.pixel_box_2 = tk.Entry(
            self.ex_setframe,
            width=5,
            font=self.font
        )  # txtbox
        self.pixel_box_2.grid(row=4, column=3)
        self.pixel_box_2.insert(tk.END, "51000")
        self.ex_saveframe = tk.LabelFrame(
            self.tab_ex,
            width=500,
            height=220,
            text="保存",
            font=self.font,
            bg=self.color
        )  # frame
        self.ex_saveframe.grid(row=0, column=1)
        self.ex_saveframe.grid_propagate(False)
        self.ex_savedirectory = tk.Label(
            self.ex_saveframe,
            text=u"保存先のディレクトリ",
            font=self.font,
            bg=self.color
        )  # label
        self.ex_savedirectory.grid(row=0, column=0, pady=(10, 5), sticky=tk.W)
        self.ex_savedirectory_box = tk.Entry(
            self.ex_saveframe,
            width=30,
            textvariable=self.dirname
        )  # txtbox
        self.ex_savedirectory_box.grid(row=1, column=0, pady=10)
        self.ex_sansyou = tk.Button(
            self.ex_saveframe,
            text="参照",
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )
        self.ex_sansyou.bind("<Button-1>", lambda event: self.directory())
        self.ex_sansyou.grid(row=0, column=0, padx=(100, 5))
        self.ex_savename = tk.Label(
            self.ex_saveframe,
            text=u"保存するファイル名(拡張子不要)",
            font=self.font,
            bg=self.color
        )  # label
        self.ex_savename.grid(row=2, column=0, pady=(10, 5), sticky=tk.W)
        self.ex_savename_box = tk.Entry(self.ex_saveframe, width=30)  # txtbox
        self.ex_savename_box.grid(row=3, column=0, pady=10)
        self.ex_savename_box.insert(tk.END, "test")
        self.ex_exeframe = tk.LabelFrame(
            self.tab_ex,
            width=750,
            height=120,
            bg=self.color,
            relief="groove",
            bd=10
        )  # frame
        self.ex_exeframe.grid(row=1, column=0, columnspan=2)
        self.ex_exeframe.grid_propagate(False)
        self.hakei_B = tk.Button(
            self.ex_exeframe,
            text="波形取得",
            width=10,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )  # button
        self.hakei_B.grid(
            row=0,
            rowspan=2,
            column=0,
            padx=10,
            pady=10,
            sticky=tk.S+tk.N
        )
        self.keisoku_B = tk.Button(
            self.ex_exeframe,
            text="計測開始",
            width=10,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )  # button
        self.keisoku_B.grid(
            row=0,
            rowspan=2,
            column=1,
            padx=10,
            pady=10,
            sticky=tk.S+tk.N
        )
        self.stop_B = tk.Button(
            self.ex_exeframe,
            text="強制終了",
            width=10,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )  # button
        self.stop_B.grid(row=0, rowspan=2, column=2, pady=10, sticky=tk.S+tk.N)
        self.ex_now_theta = tk.Label(
            self.ex_exeframe,
            text="現在の角度",
            font=self.font,
            bg=self.color
        )  # label
        self.ex_now_theta.grid(row=0, column=3, padx=10)
        self.ex_now_theta_txt = tk.Label(
            self.ex_exeframe,
            textvariable=self.angle,
            bg=self.color
        )  # label
        self.ex_now_theta_txt.grid(row=0, column=4)
        self.ex_StatusNamelabel = tk.Label(
            self.ex_exeframe,
            text="status",
            font=self.font,
            bg=self.color
        )  # label
        self.ex_StatusNamelabel.grid(row=1, column=3)
        self.ex_Statuslabel = tk.Label(
            self.ex_exeframe,
            text=u"   ",
            bg="green"
        )  # label
        self.ex_Statuslabel.grid(row=1, column=4)
        self.ex_pressure_label = tk.Label(
            self.ex_exeframe,
            text="ガス圧",
            font=self.font,
            bg=self.color
        )  # label
        self.ex_pressure_label.grid(row=2, column=3)
        self.ex_pressure_label = tk.Label(
            self.ex_exeframe,
            textvariable=self.now_pressure,
            bg=self.color
        )  # label
        self.ex_pressure_label.grid(row=2, column=4)
        # rog text #
        self.txtname = tk.Label(
            self.txtframe,
            text="Rog list",
            font=self.font,
            bg="Grey99"
        )  # label
        self.txtname.grid(row=0, column=0, columnspan=2)
        self.txt = tk.Text(
            self.txtframe,
            height=17,
            width=20,
            bg=self.color,
            relief="groove",
            bd=10
        )  # txtbox
        self.txt.configure(font="Helvetica")
        self.txt.grid(row=1, column=0, sticky=tk.W)
        self.yscroll = tk.Scrollbar(
            self.txtframe,
            orient=tk.VERTICAL,
            command=self.txt.yview
        )  # scrollbar
        self.yscroll.grid(row=1, column=1, sticky=tk.E+tk.W+tk.N+tk.S)
        self.txt["yscrollcommand"] = self.yscroll.set  # txtbox と結び付け

    # 自動保存 #
    def gui_auto_save(self):
        self.tab_auto_save = tk.Frame(self.nb)
        self.nb.add(self.tab_auto_save, text="自動保存")
        self.auto_save_setframe = tk.LabelFrame(
            self.tab_auto_save,
            width=250,
            height=220,
            text="初期設定",
            font=self.font,
            bg=self.color
        )  # frame
        self.auto_save_setframe.grid(row=0, column=0)
        self.auto_save_setframe.grid_propagate(False)
        self.auto_save_start = tk.Label(
            self.auto_save_setframe,
            text="開始角度",
            font=self.font,
            bg=self.color
        )  # label
        self.auto_save_start.grid(row=0, column=0, padx=5, pady=10)
        self.auto_save_start_box = tk.Entry(
            self.auto_save_setframe,
            width=3,
            font=self.font
        )  # txtbox
        self.auto_save_start_box.grid(row=0, column=1, padx=10)
        self.auto_save_start_box.insert(tk.END, "-30")
        self.auto_save_end = tk.Label(
            self.auto_save_setframe,
            text="終了角度",
            font=self.font,
            bg=self.color
        )  # label
        self.auto_save_end.grid(row=1, column=0, pady=10)
        self.auto_save_end_box = tk.Entry(
            self.auto_save_setframe,
            width=3,
            font=self.font
        )  # txtbox
        self.auto_save_end_box.grid(row=1, column=1)
        self.auto_save_end_box.insert(tk.END, "30")
        self.auto_save_width = tk.Label(
            self.auto_save_setframe,
            text="角度幅",
            font=self.font,
            bg=self.color
        )  # label
        self.auto_save_width.grid(row=2, column=0, pady=10)
        self.auto_save_width_box = tk.Entry(
            self.auto_save_setframe,
            width=3,
            font=self.font
        )  # txtbox
        self.auto_save_width_box.grid(row=2, column=1)
        self.auto_save_width_box.insert(tk.END, "1")
        self.auto_save_chanelname = tk.Label(
            self.auto_save_setframe,
            text="保存する波形",
            font=self.font,
            bg=self.color)  # label
        self.auto_save_chanelname.grid(row=3, column=0, pady=10)
        self.auto_save_chanel = ttk.Combobox(
            self.auto_save_setframe,
            textvariable=self.ex_C,
            values=["C1", "C2", "C3", "C4"],
            width=3,
            font=self.font
        )  # txtbox
        self.auto_save_chanel.set("C3")
        self.auto_save_chanel.grid(row=3, column=1, padx=10)
        self.autosave_saveframe = tk.LabelFrame(
            self.tab_auto_save,
            width=500,
            height=220,
            text="保存",
            font=self.font,
            bg=self.color
        )  # frame
        self.auto_save_saveframe.grid(row=0, column=1)
        self.auto_save_saveframe.grid_propagate(False)
        self.auto_save_savedirectory = tk.Label(
            self.auto_save_saveframe,
            text=u"保存先のディレクトリ",
            font=self.font,
            bg=self.color
        )  # label
        self.auto_save_savedirectory.grid(row=0, column=0, pady=(10, 5), sticky=tk.W)
        self.auto_save_savedirectory_box = tk.Entry(
            self.auto_save_saveframe,
            width=30,
            textvariable=self.dirname
        )  # txtbox
        self.auto_save_savedirectory_box.grid(row=1, column=0, pady=10)
        self.auto_save_sansyou = tk.Button(
            self.auto_save_saveframe,
            text="参照",
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )
        self.auto_save_sansyou.bind("<Button-1>", lambda event: self.directory())
        self.auto_save_sansyou.grid(row=0, column=0, padx=(100, 5))
        self.auto_save_savename = tk.Label(
            self.auto_save_saveframe,
            text=u"保存するファイル名(拡張子不要)",
            font=self.font,
            bg=self.color
        )  # label
        self.auto_save_savename.grid(row=2, column=0, pady=(10, 5), sticky=tk.W)
        self.auto_save_savename_box = tk.Entry(self.auto_save_saveframe, width=30)  # txtbox
        self.auto_save_savename_box.grid(row=3, column=0, pady=10)
        self.auto_save_savename_box.insert(tk.END, "test")
        self.auto_save_exeframe = tk.LabelFrame(
            self.tab_auto_save,
            width=750,
            height=120,
            bg=self.color,
            relief="groove",
            bd=10
        )  # frame
        self.auto_save_exeframe.grid(row=1, column=0, columnspan=2)
        self.auto_save_exeframe.grid_propagate(False)
        self.hakei_B = tk.Button(
            self.auto_save_exeframe,
            text="波形取得",
            width=10,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )  # button
        self.hakei_B.grid(
            row=0,
            rowspan=2,
            column=0,
            padx=10,
            pady=10,
            sticky=tk.S+tk.N
        )
        self.keisoku_B = tk.Button(
            self.auto_save_exeframe,
            text="計測開始",
            width=10,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )  # button
        self.keisoku_B.grid(
            row=0,
            rowspan=2,
            column=1,
            padx=10,
            pady=10,
            sticky=tk.S+tk.N
        )
        self.stop_B = tk.Button(
            self.auto_save_exeframe,
            text="強制終了",
            width=10,
            height=3,
            font=self.font,
            activebackground="blue",
            activeforeground="white"
        )  # button
        self.stop_B.grid(row=0, rowspan=2, column=2, pady=10, sticky=tk.S+tk.N)
        self.auto_save_now_theta = tk.Label(
            self.auto_save_exeframe,
            text="現在の角度",
            font=self.font,
            bg=self.color
        )  # label
        self.auto_save_now_theta.grid(row=0, column=3, padx=10)
        self.auto_save_now_theta_txt = tk.Label(
            self.auto_save_exeframe,
            textvariable=self.angle,
            bg=self.color
        )  # label

    def on_closing(self):
        # if messagebox.askokcancel("Quit","Do you want to quit ?"):
        self.master.quit()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)


def main():
    master = tk.Tk()
    app = Gui(master=master)
    # 左上のバツを押したら，on_closing関数を行う．
    master.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()  # tkinter をループする．


if __name__ == "__main__":
    main()
