##### CMOS カメラのラインプロファイル用プログラム #####
### 内容 ###
# main のプログラムに import して使用する
#ボタン入力で gui 上に x,y の強度分布を表示．映像に出力する LINE をドラッグすることで LINE 上の強度分布を所得する
###########
### 使用方法 ###
# 1 # from profile import Profile で import する
# 2 # self.profile = Profile(root) でインスタンス化．表示する root を引数にもつ
# 3 # profile_function(self): 関数を定義する
# 4 # self.X.bind("<Button-1>",lambda event : self.profile_function()) でボタン(X)と property_function()を結びつける
# 5 # 以下の内容を記入
#     def profile_function(self):
#         self.profile.line(映像を表示する canvas,映像データ)
#         self.loop_profile()
#         self.profile_stop_B = self.profile.return_button()
#         self.profile_stop_B.bind("<Button-1>",lambda event : self.profile_stop(),"+")
#
#     def loop_profile(self):
#         self.profile.line_profile_loop(映像データ)
#         self.loop = self.master.after(1,self.loop_profile)
#
#     def profile_stop(self): を定義し，以下の内容を記入
#         self.master.after_cancel(self.loop)
#         self.profile.stop()
###############

import cv2 # カメラ
import matplotlib.pyplot as plt # グラフ 
import numpy as np # 数値計算
import time # FPS 測定用
### gui 関係 ###
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PIL.Image,PIL.ImageTk
### test ###
import gc # memory
class Profile():
    def __init__(self,master=None):
        super().__init__()
        self.master = master
        print("line関数をインポートしました")

    def line(self,canvas,image,m): # 初期設定の関数
        self.canvas = canvas # 映像を表示する場所
        self.image = image # 映像データ
        self.m = m # 拡大率
        ### グラフ の体裁 ###
        self.fig,self.ax = plt.subplots(2) # 強度分布を書くグラフ
        self.ax[0].set_title("X Line Profile")
        self.ax[0].set_xlabel("x pixel")
        self.ax[0].set_ylabel("Intensity")
        self.ax[0].set_ylim(0,1)
        self.ax[0].set_xlim(0,self.image.shape[1])
        self.ax[0].minorticks_on()
        self.ax[0].grid()

        self.ax[1].set_title("Y Line Profile")
        self.ax[1].set_xlabel("y pixel")
        self.ax[1].set_ylabel("Intensity")
        self.ax[1].set_ylim(0,1)
        self.ax[1].set_xlim(0,self.image.shape[0])
        self.ax[0].minorticks_on()
        self.ax[1].grid()
        plt.tight_layout()
        
        self.gui() # gui 関係
        self.line_profile() # 実際の処理

    def gui(self): # gui 関係
        #self.master.geometry("1400x700") # サイズ
        ### 全体の frame ###
        self.profile_frame = tk.Frame(self.master,width = 500,height = 500,bg = "white",relief = "groove",bd = 10)
        self.profile_frame.grid(row = 0,column = 1) # ここを編集することで root に表示する位置を変更できる．

        ### STOP ボタンの frame とその中身 ###
        self.profile_button_frame = tk.Frame(self.profile_frame,width = 500,height = 100,bg = "white",relief = "groove",bd = 10)
        self.profile_button_frame.grid(row = 0,column = 0)
        self.profile_stop = tk.Button(self.profile_button_frame,text = "STOP")
        self.profile_stop.grid(row = 0,column = 0)

        ### ラインプロファイルの frame とその中身###
        self.intensity_frame = tk.Frame(self.profile_frame,width = 500,height = 500,bg = "white",relief = "groove",bd = 10)
        self.intensity_frame.grid(row = 1,column = 0)
        self.canvas_intensity = FigureCanvasTkAgg(self.fig, master=self.intensity_frame) # 強度分布を表示する場所
        self.canvas_intensity.get_tk_widget().grid(row=1,column=0) # canvas の配置

    def return_button(self): # STOP ボタンの情報を返す．
        return self.profile_stop

    def line_profile(self): # LINE とグラフの初期設定
        self.x_profile_y_0=400 # LINE の初期位置 tate
        self.y_profile_x_0=500 # LINE の初期位置 yoko
        self.line_width = 10 # LINE の線幅
        self.x = np.arange(0,self.image.shape[0],1) # グラフの横軸
        self.y = np.arange(0,self.image.shape[1],1) # グラフの横軸
        print(self.m)
        print(self.image.shape)
        print(self.image.shape,self.image.shape/self.m)

         ### LINE の定義 ###
         ### m(height,width) = CD.image(height,width)/img(height,width)
         ### img(height,width) = 800,1000 固定値
         ### LINE は event.x を m で割って補正(resolution から 800,1000にする)
         ### 強度分布は event.x に m をかけて補正(固定値 から resolution にする)
        self.x_profile = self.canvas.create_rectangle(0, self.x_profile_y_0, int(self.image.shape[1]/self.m[1]),self.x_profile_y_0+self.line_width, fill="red",tags = "x_profile") # ラインプロファイルの線を定義．x_0,y_0,x_1,y_1の順番で適当な数字を入力する．+ は LINE の線幅．
        print(self.image.shape[1]/self.m[1])
        self.canvas.tag_bind("x_profile", "<B1-Motion>", self.dragged_x) # ドラッグ操作 (対象，ドラッグ操作，対応する関数)
        self.y_profile = self.canvas.create_rectangle(self.y_profile_x_0, 0, self.y_profile_x_0+self.line_width,int(self.image.shape[0]/self.m[0]), fill="blue",tags = "y_profile") # ラインプロファイルの線を定義．x_0,y_0,x_1,y_1の順番で適当な数字を入力する．+ は LINE の線幅．
        self.canvas.tag_bind("y_profile","<B1-Motion>",self.dragged_y) # ドラッグ操作

        ### 強度分布の定義 ###
        self.line_0, = self.ax[0].plot(self.y,self.image[self.x_profile_y_0,self.y]/max(self.image[self.x_profile_y_0,:]),color = "red") # グラフ書き換え用．x 軸の強度分布
        self.line_1, = self.ax[1].plot(self.x,self.image[self.x,self.y_profile_x_0]/max(self.image[:,self.y_profile_x_0])) # グラフ書き換え用．y 軸の強度分布

    def line_profile_loop(self,image):# 実際の処理 loop させて使用する
        self.image = image # 映像データ
        self.canvas.coords(self.x_profile,0, self.x_profile_y_0, int(self.image.shape[1]/self.m[1]),self.x_profile_y_0+self.line_width) # ラインプロファイルの線の移動
        self.canvas.coords(self.y_profile,self.y_profile_x_0, 0, self.y_profile_x_0+self.line_width,int(self.image.shape[0]/self.m[0])) # ラインプロファイルの線の移動
        self.canvas.lift("x_profile") # canvas の一番上に LINE を配置
        self.canvas.lift("y_profile") # canvas の一番上に LINE を配置
        self.intensity(self.image) # 強度分布表示

    def intensity(self,image): # 強度分布表示
        self.x = np.arange(0,self.image.shape[0],1) # グラフの横軸
        self.y = np.arange(0,self.image.shape[1],1) # グラフの横軸
        self.line_0.set_ydata(image[int(self.x_profile_y_0*self.m[0]),self.y]/max(image[int(self.x_profile_y_0*self.m[0]),:])) # グラフのデータを書き換え．x 軸
        #print(int(self.x_profile_y_0*self.m[0]))

        #self.ax[0].draw_artist(self.ax[0].patch) #いらないかも．draw_artistで直接グラフをいじる
        #self.ax[0].draw_artist(self.line_0)
        self.line_1.set_ydata(image[self.x,int(self.y_profile_x_0*self.m[1])]/max(image[:,int(self.y_profile_x_0*self.m[1])])) # y 軸
        self.line_1.set_xdata(self.x)
        self.canvas_intensity.draw() # gui 上に反映

    def dragged_x(self,event): # マウスの座標を変数に代入する関数
        print(event.y)
        if event.y < 0 or event.y > int(self.image.shape[0]/self.m[0])-5: # イメージからはみ出した場合，グラフでエラーを返さないように仮の値を与える．
            event.y = 100
        self.x_profile_y_0 = event.y # LINE の座標．

    def dragged_y(self,event):
        print(event.x)
        if event.x < 0 or event.x > int(self.image.shape[1]/self.m[1])-5: # イメージからはみ出した場合，グラフでエラーを返さないように仮の値を与える．
            event.x = 100
        self.y_profile_x_0 = event.x # LINE の座標

    def stop(self): # 終了の関数
        self.canvas.delete(self.x_profile)  # line の削除
        self.canvas.delete(self.y_profile)
        self.ax[0].clear() # グラフ のリセット
        self.ax[1].clear()
        self.profile_frame.grid_forget() # profile_frame の非表示
        gc.collect() # メモリの開放．多分していない．
        #self.master.geometry("600x700") # root のリサイズ．小さくしている

def main(): # python3 profile.py でこのプログラムを動かしたら
    print("このファイルは読みこみ専用ファイルです.")
    print("profile = profile.Profile() でインスタンス化したあと,")
    print("profile.gui(cap，root，canvas) で使用してください． ")

if __name__ == "__main__":
    main()
