##### CMOS カメラのプログラム ######
# TIS.py，profile.py および property.py を同じディレクトリに配置すること
# CMOS カメラとは シリアル番号で通信を行う
# シリアル番号は tcam-ctrl -l で確認できる
#################################
import sys
import os
import time
import cv2 # カメラ
import PIL.Image,PIL.ImageTk # カメラ
import numpy as np
import concurrent.futures
import multiprocessing
import matplotlib.pyplot as plt

### gui 関係 ###
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog # save に用いる

### TIS ###
import TIS
from collections import namedtuple

### original ###
from profile import Profile
from property import Property

class CustomData:
    ''' Example class for user data passed to the on new image callback function
        '''
    def __init__(self, newImageReceived, image):
        self.newImageReceived = newImageReceived
        self.image = image
        self.busy = False


class Application(tk.Frame):
    def __init__(self,master=None):
        super().__init__()
        #exector = concurrent.futures.ThreadPoolExecutor(max_workers = multiprocessing.cpu_count())
        f,ax = plt.subplots(1) # 早くなる 
        self.master = master # root
        self.width = 1280
        self.height = 960
        self.m = (self.height/1000,self.width/800)
        self.count = 0 # FPS 用
        self.max_count = 10
        self.t = cv2.TickMeter() # FPS 用
        self.t.start()
        
        self.CD = CustomData(False,None) # CustomData をインスタンス化
        self.Tis = TIS.TIS() # TIS.py をインスタンス化
        self.Tis.openDevice("27810554",self.width,self.height,"10/1",TIS.SinkFormats.GRAY8,False) # カメラに接続
        self.Tis.Set_Image_Callback(self.on_new_image,self.CD) # 必須．よくわからない
        self.CD.busy = True # CMOS カメラが ready
        self.Tis.Start_pipeline() # パイプラインの構築
        self.Tis.Set_Property("Trigger Mode","OFF") # 設定
        #print(self.Tis.Get_Property("Trigger Source").value) # 設定確認
        #cv2.waitKey(1000) # 1 秒待機．よくわからない．
        self.CD.busy = False # CMOS カメラが busy

        ### gui 関係 ###
        self.gui_root()
        self.gui_frame()
        self.gui_button()
        ### profile.py ###
        self.profile = Profile(self.master) # original インスタンス化
        self.profile_button.bind("<Button-1>",lambda event : self.profile_function()) # PROFILE ボタンと property_function()の結びつけ

        ### property.py ###
        self.property = Property(self.Tis) # インスタンス化
        self.property_button.bind("<Button-1>",lambda event : self.property_function()) # 関数と結びつけ
        ### image ###
        self.capture()
        #self.capture()


    def test(self):
        f,ax = plt.subplots(1)
    def on_new_image(self,tis, userdata):# イメージを取得する関数 
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
    
    def define(self): # self.loop_capture_A を定義する関数
            pass
    ### main.py の処理 ###
    def capture(self):
        if self.CD.newImageReceived is False: # CD.newImageReceived が True になるまでx待機する loop
            #print("no image received")
            self.loop_capture = self.master.after(10,self.capture) # 1 ms capture_A を繰り返す．
        else: # loop から抜け出したら
            self.CD.newImageReceived = False
            #print(self.tries)
            self.img = cv2.resize(self.CD.image[:,:,0],dsize = (1000,800))
            #print(self.img)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.img)) # canvas に用いるため，データの形式を変更
            start = time.time()
            self.canvas.delete("image")
            self.canvas.create_image(0,0,image=self.photo,anchor=tk.NW,tag="image") # canvas に表示
            self.canvas.update()
            end = time.time()
            #print(end-start)
            self.count += 1 # FPS カウンター
            if self.count == self.max_count: # FPS 用．1 秒経過したら
                self.t.stop()
                #print("fps")
                self.fps_count.set("FPS : %0.1f"%(self.max_count/self.t.getTimeSec()))
                self.t.reset()
                self.t.start()
                self.count = 0 # self.count のリセット
            self.loop_capture = self.master.after(1,self.capture) # 1 ms capture_A を繰り返す．
    def average_property(self):
        self.master.after_cancel(self.loop_capture) # loop_capture を停止
        self.ave_count = 0
        self.average_num = average_number_box.get()
        self.average()
        
    def average(self): ### average ###
        if self.CD.newImageReceived is False: # CD.newImageReceived が True になるまでx待機する loop
            #print("no image received")
            self.loop_average = self.master.after(10,self.average) # 1 ms capture_A を繰り返す．
        else: # loop から抜け出したら
            self.CD.newImageReceived = False
            ave_img = ave_img + self.CD.image[:,:,0].astype("uint16")
            self.ave_count += 1
            if ave_count == self.average_num:
                ave_img = ave_img/self.average_num
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.img)) # canvas に用いるため，データの形式を変更
                self.canvas.delete("image")
                self.canvas.create_image(0,0,image=self.photo,anchor=tk.NW,tag="image") # canvas に表示
                self.canvas.update()
                self.ave_count = 0

            self.loop_average = self.master.after(1,self.average) # 1 ms capture_A を繰り返す．
            #########
    def average_stop(self):
        self.master.after_cancel(self.loop_average) # loop_capture を停止
        self.capture()
        
    ### profile.py ###
    def profile_function(self): # profile 関数
        self.m = np.array((self.height/800,self.width/1000)) # 拡大率
        print(self.CD.image[:,:,0].shape,self.img.shape)
        self.profile.line(self.canvas,self.CD.image[:,:,0],self.m) # guiやグラフ等の初期設定．(映像を表示する場所，映像データー)を引数にもつ．
        self.loop_profile() # loop する関数
        self.profile_stop_B = self.profile.return_button() # STOP ボタンの所得
        self.profile_stop_B.bind("<Button-1>",lambda event : self.profile_stop(),"+") # STOP ボタンと profile_stop 関数の結びつけ

    def loop_profile(self):
        self.profile.line_profile_loop(self.CD.image[:,:,0]) # profile.py の関数．イメージを引数に持つ．
        self.loop = self.master.after(1,self.loop_profile) # 1 ms で loop_profile を繰り返す

    def profile_stop(self): # profile 終了の関数
        self.master.after_cancel(self.loop) # self.loop の終了
        self.profile.stop() # gui の非表示やグラフの初期化
    ### profile.py end ###
    ### property.py ###
    def property_function(self):
        self.property.gui() # property の gui 表示
        self.fps_box = self.property.return_box() # fps_box の取得
        self.fps_box.bind("<<ComboboxSelected>>",lambda event : self.property_get(),"+") # fps_box と property_get 関数の結びつけ

    def property_get(self):
        self.width,self.height,self.fps = self.property.return_property() # resolution,fps の取得
        #print(self.width,self.height,self.fps)
        self.device(self.width,self.height,self.fps) # device 関数

    def device(self,width,height,fps): # resolution,fps を設定する関数．
        self.Tis.Stop_pipeline() # パイプラインの停止
        self.Tis.openDevice("27810554",width,height,"{}".format(fps),TIS.SinkFormats.GRAY8,False) # resolution(width,height),fps の設定．再び接続する．
        self.Tis.Set_Image_Callback(self.on_new_image,self.CD) # 必須．よくわからない
        self.CD.busy = True # CMOS カメラが ready
        self.Tis.Start_pipeline() # パイプラインの構築
        self.Tis.Set_Property("Trigger Mode","OFF") # 設定
        #print(self.Tis.Get_Property("Trigger Source").value) # 設定確認
        cv2.waitKey(1000) # 1 秒待機．よくわからない．
        self.CD.busy = False # CMOS カメラが busy
        ### カメラの設定 ここまで ###
    ### property.py end ###

    ### Gui 関係の関数 ###
    def gui_root(self):# root の構築
        self.master.configure(background='Light Green') # Gui の色 
        self.master.title(u"Stage Control_ver1") # タイトル
        self.bg = self.master.cget("background")
        #self.master.geometry("1000x900") # サイズ

    def gui_frame(self): # frame の構築
        self.main_frame = tk.Frame(self.master,width = 1000,height = 900,bg = "white",relief = "groove",bd = 10) # image_frame と button_frame を入れる場所
        self.main_frame.grid(row = 0,column = 0) # 配置

        ### button_frame ###
        self.button_frame = tk.Frame(self.main_frame,width=450,height = 50,bg = "white",relief = "groove",bd =10)
        self.button_frame.grid(row=0,column=0,sticky = tk.W+tk.S)
        #self.button_frame.grid_propagate(False)
        ### image_frame ###
        self.image_frame = tk.Frame(self.main_frame,width= 1000,height = 800,bg="white",relief="groove",bd=10)
        self.image_frame.grid(row=1,column=0,padx = 0,pady = 0,sticky=tk.E+tk.W+tk.S+tk.E+tk.N)
        #self.image_frame.grid_propagate(False) # 自動で大きさを変更しない
        ### image_frame に 映像を表示する場所 ###
        self.canvas = tk.Canvas(self.image_frame)
        self.canvas.configure(width=1000,height=800)
        self.canvas.grid(row=0,column=0)
        self.canvas.grid_propagate(False)

    def gui_button(self):# button_frame の中身．widget.bind で関数と紐付け

        self.property_button = tk.Button(self.button_frame,text = "PROPERTY",width = 10,height = 1) # tk.Button(場所,名前,横幅，縦幅)
        self.property_button.grid(row = 0,column = 0) # bottun の配置

        self.profile_button = tk.Button(self.button_frame,text = "PROFILE",width = 10,height = 1)
        self.profile_button.grid(row = 0,column = 1)

        self.average_button = tk.Button(self.button_frame,text = "AVERAGE",command = self.average_gui,width = 10,height = 1)
        self.average_button.grid(row = 0,column = 2)
        
        self.save_button = tk.Button(self.button_frame,text = "SAVE",command = self.snap_shot_gui,width = 10,height = 1) # 修正箇所
        self.save_button.grid(row = 0,column = 3)

        self.fps_count = tk.StringVar()
        self.fps_label = tk.Label(self.button_frame,textvariable = self.fps_count,bg = "Light Green")
        self.fps_label.grid(row=0,column = 4,padx = 10,sticky = tk.E+tk.W)

    def average_gui(self):
        self.average_root = tk.Tk()
        self.average_frame = tk.Frame(self.average_root,width= 100,height = 80,bg="white",relief="groove",bd=10)
        self.average_frame.grid(row=1,column=0,padx = 0,pady = 0,sticky=tk.E+tk.W+tk.S+tk.E+tk.N)
        self.average_number = tk.StringVar()
        self.average_number_label = tk.Label(self.average_frame,text=u"平均回数") # label
        self.average_number_label.grid(row=1,column=0,pady=(10,5),sticky=tk.W)
        self.average_number_box = tk.Entry(self.average_frame,width=30,textvariable=self.average_number) # txtbox
        self.average_number_box.insert(tk.END,"100")

        self.average_number_box.grid(row=2,column=0,pady=10)
       
        self.average_button = tk.Button(self.average_frame,text="実行",activebackground="blue",activeforeground="white")
        self.average_button.bind("<Button-1>",lambda event : self.average_property())
        self.average_button.grid(row=1,column=1,padx = (100,5))

        self.average_stop_button = tk.Button(self.average_frame,text="終了",activebackground="blue",activeforeground="white")
        self.average_stop_button.bind("<Button-1>",lambda event : self.average_stop())
        self.average_stop_button.grid(row=1,column=1,padx = (100,5))

    def snap_shot_gui(self):
        self.snap_shot_root = tk.Tk()
        self.snap_shot_frame = tk.Frame(self.snap_shot_root,width= 1000,height = 800,bg="white",relief="groove",bd=10)
        self.snap_shot_frame.grid(row=1,column=0,padx = 0,pady = 0,sticky=tk.E+tk.W+tk.S+tk.E+tk.N)
        self.dirname = tk.StringVar()
        self.snap_shot_directory = tk.Label(self.snap_shot_frame,text=u"保存先のディレクトリ") # label
        self.snap_shot_directory.grid(row=1,column=0,pady=(10,5),sticky=tk.W)
        self.snap_shot_directory_box = tk.Entry(self.snap_shot_frame,width=30,textvariable=self.dirname) # txtbox
        self.snap_shot_directory_box.grid(row=2,column=0,pady=10)
        #self.snap_shot_directory_box.insert(tk.END,"./capture/")

        self.sansyou = tk.Button(self.snap_shot_frame,text="参照",activebackground="blue",activeforeground="white")
        self.sansyou.bind("<Button-1>",lambda event : self.directory())
       
        self.sansyou.grid(row=1,column=0,padx = (100,5))
        self.snap_shot_name = tk.Label(self.snap_shot_frame,text=u"保存するファイル名(拡張子不要)") # label
        self.snap_shot_name.grid(row=3,column=0,pady=(10,5),sticky=tk.W)
        self.snap_shot_name_box = tk.Entry(self.snap_shot_frame,width=30) # txtbox
        self.snap_shot_name_box.grid(row=4,column=0,pady=10)
        self.snap_shot_name_box.insert(tk.END,"test")
        self.snap_shot_button = tk.Button(self.snap_shot_frame,text = "SNAP",width = 10,height = 1) # 修正箇所
        self.snap_shot_button.bind("<Button-1>",lambda event : self.snap_shot(self.snap_shot_directory_box.get(),self.snap_shot_name_box.get()))
        self.snap_shot_button.grid(row = 0,column = 2)

    def directory(self):
        self.iDir = os.path.abspath(os.path.dirname(__file__))
        self.iDirPath = filedialog.askdirectory(initialdir = self.iDir)
        self.snap_shot_directory_box.insert(tk.END,self.iDirPath+"/")
        self.dirname.set(self.iDirPath+"/")
        
    def snap_shot(self,path,name): # 映像のスナップショット用の関数．修正箇所
        if not os.path.exists(path): # property.txt が存在しないなら
           os.makedirs(path,exist_ok = True) # cash 
           print("pathを作成しました")
           #適当に定めた初期値を適用する
        else: # property.txt が存在するなら
          print("pathは存在します")
        
        #print(path,name)
        print(self.CD.image[:,:,0],path,name)
        cv2.imwrite(path+name+".jpg",self.CD.image[:,:,0]) # image を保存
        print("saveしました")
        
    def on_closing(self): # 左上のバツを押したら動く関数．
        self.Tis.Stop_pipeline() # CMOS カメラとの通信終了
        self.master.destroy() # gui を閉じる
        print("program ends")
        sys.exit() # プログラム終了

def main(): # はじめに動く関数
    root = tk.Tk() # root を定義
    app = Application(master=root) # Applicationをインスタンス化．
    root.protocol("WM_DELETE_WINDOW",app.on_closing) # 左上のバツを押したら，on_closing関数を行う．
    app.mainloop() # 処理がない時，受付待機状態となりプログラムが終了するまで loop する．

if __name__ == "__main__": # python3 main.py でこのプログラムを動かしたら
    main()


