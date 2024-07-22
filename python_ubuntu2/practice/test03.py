import TIS
import cv2
import time

#########
class CustomData:
    ''' Example class for user data passed to the on new image callback function
        '''
    def __init__(self, newImageReceived, image):
        self.newImageReceived = newImageReceived
        self.image = image
        self.busy = False
#########
def on_new_image(tis, userdata):# イメージを取得する関数 
        '''
        Callback function, which will be called by the TIS class
        :param tis: the camera TIS class, that calls this callback
        :param userdata: This is a class with user data, filled by this call.
        :return:
        '''
        #userdata = userdata
        # Avoid being called, while the callback is busy
        if userdata.busy is True:
                return
        userdata.busy = True
        userdata.newImageReceived = True
        userdata.image = tis.Get_image()
        userdata.busy = False

#########
CD = CustomData(False,None) # CustomData をインスタンス化
Tis = TIS.TIS() # TIS.py をインスタンス化
Tis.openDevice("27810554",960,720,"30/1",TIS.SinkFormats.GRAY8,False) # カメラに接続
Tis.Set_Image_Callback(on_new_image,CD) # 必須．よくわからない omajinai
CD.busy = True # CMOS カメラが ready
Tis.Start_pipeline() # パイプラインの構築
CD.busy = False # CMOS カメラが busy setuzokudekita
###############
while True:#while senngen
    if CD.newImageReceived is False: # CD.newImageReceived が True になるまでx待機する loop
        time.sleep(0.01)
    else:
        CD.newImageReceived = False
        cv2.imshow("capture",CD.image[:,:,0]) #monokuro0 960*720*1 eizomiru
        if cv2.waitKey(1) & 0xFF == ord('q'): #q osaretara cv2Surya
                cv2.destroyAllWindows()
                break
###############

