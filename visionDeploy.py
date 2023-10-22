import collections as c
import numpy as np
import csv
import os
import sys
import time
import cv2
import fastdeploy as fd
import visionDeploy_rc
from PySide6 import QtCore, QtGui, QtNetwork, QtWidgets
from PySide6.QtCharts import (QBarCategoryAxis, QBarSeries, QBarSet, QChart,
                              QChartView, QValueAxis)
from ui_visionDeploy import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    isstop,issnap,isrec=False,False,False  #中断执行标记 #拍照标记 #录制标记 
    isscaled,iscam,isimg,isipcam,isvideo=False,True,False,False,False #勾选标记
    ip,camid,user,pwd="","","","" #录像机登录信息
    cap=cv2.VideoCapture()
    Video=cv2.VideoWriter()
    d={} #存放检测结果
    dev="" #设备信息
    prelabel="" #预测标签
    preids="" #预测IDs

    def __init__(self):
        super().__init__()
        self.setupUi(self)        
        #状态栏
        self.statusBar().showMessage("智能视频监控分析辅助管理系统")
        #默认勾选摄像头
        self.rbtcam.setChecked(True)       
        self.screengeometry=self.screen().availableGeometry()
        #self.resize(self.screengeometry.width()*0.7,self.screengeometry.height()*0.7)
        sw,sh=self.screengeometry.width(),self.screengeometry.height()
        w,h=int(sw*0.7),int(sh*0.7)
        self.setGeometry((sw-w)//2,(sh-h)//2,w,h) #窗口大小可调
        
        #槽信号
        self.btnclose.clicked.connect(self.Close)
        self.btnopen.clicked.connect(self.Open)
        self.cboxtask.currentIndexChanged.connect(self.schange)
        self.cboxmodel.currentIndexChanged.connect(self.modelchange)
        self.menuhelp.triggered.connect(self.winaction)
        self.cboxcamid.currentIndexChanged.connect(self.changecamid)
        self.btnsnap.clicked.connect(self.snap)
        self.btnrec.clicked.connect(self.rec)
        
        
         #释放资源文件
        if not os.path.exists("haarcascade_frontalface_alt.xml"):
            QtCore.QFile.copy(":harr/haarcascade_frontalface_alt.xml","haarcascade_frontalface_alt.xml")
               
        #显示启动画面                
        #self.img=QtGui.QImage(":img/start.jpg")    
        #self.lbldst.setPixmap(QtGui.QPixmap.fromImage(self.img).scaled(768,512, QtCore.Qt.KeepAspectRatio))
        font=QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        self.lbldst.setFont(font)
        self.lbldst.setText("智能视频监控分析辅助管理系统")
        self.lbldst.setFixedSize(self.width()*0.6,self.height()*0.6)
        #self.lbldst.setScaledContents(True) #自适应大小     
        self.lbldst.setAlignment(QtCore.Qt.AlignCenter)
    
        self.detlst.clicked.connect(self.on_detlst_clicked)
        #设置列表框多选
        self.detlst.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection) 
    
        #lineEdit 回车事件
        self.linekey.returnPressed.connect(self.on_linekey_returnPressed)
        #加载模型
        self.cboxtask.addItems(["请选择模型"])        
        if os.path.exists("models"):
            lst=os.listdir("models")
            self.cboxtask.addItems(lst)
        else:
            os.makedirs("models")
            os.makedirs("models/cls-model")
            os.makedirs("models/det-model")
            os.makedirs("models/face-model")
        #默认64通道数
        self.cboxcamid.addItems([str(id).rjust(2,"0") for id in range(1,65)])
            
        #设置列表框的宽度
        self.lstfile.setFixedWidth(self.width()//4)
        self.detlst.setFixedWidth(self.width()//4)
        self.linekey.setFixedWidth(self.width()//4)
        
        #加载分析结果文件
        filelst=[]
        if not os.path.exists("output"):
            os.makedirs("output")           
        fname=time.strftime("%Y%m%d",time.localtime())+".csv"
        file_name=os.path.join("output",fname)
        if not os.path.exists(file_name):
            with open(file_name,"w",encoding="utf-8_sig",newline="") as fp:
                csvwriter=csv.writer(fp)
                csvwriter.writerow(["datetime","dev","type","label","cnlabel","probability"]) 
        for f in os.listdir("output"):
            if f.endswith(".csv"):
                filelst.append(f)                 
        self.slmfile=QtCore.QStringListModel()
        self.slmfile.setStringList(filelst)
        self.lstfile.setModel(self.slmfile)
        
        #结果文件存放列表事件
        self.lstfile.clicked.connect(self.on_lstfile_clicked)
        
        #创建chart_view
        self.buildChart(self.horizontalLayout_6,"目标检测结果排名前5",False)
        
                
    #创建图表
    def buildChart(self,layout:QtWidgets.QHBoxLayout,title:str,visible=False):
        self.series = QBarSeries()  
        self.set_0 = QBarSet("次数——<font color='#FF0000'>点击查看全图和数据</font>")                                              
        self.series.append(self.set_0)        
        self.chart = QChart()
        self.chart.addSeries(self.series)        
        self.chart.setTitle(title)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)       
        self.axis_x = QBarCategoryAxis()        
        self.chart.addAxis(self.axis_x, QtCore.Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)
        self.axis_y = QValueAxis()        
        self.chart.addAxis(self.axis_y, QtCore.Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(QtCore.Qt.AlignBottom)
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        layout.addWidget(self.chart_view)        
        self.chart_view.setVisible(visible)                
        #图表鼠标事件
        self.chart_view.mousePressEvent=self.showchartWin
        
    #更新图表数据
    def barChart(self,d):
        self.axis_x.clear()        
        self.set_0.remove(0,self.set_0.count())        
        #d=self.d  
        #print(d)  
        klst=[]
        vlst=[]
        if len(d)>0:
            for v in d.values():  
                vlst.append(v)
            #print(vlst) 
            for k in d.keys():
                klst.append(k)
            #print(klst)        

            self.set_0.append(vlst)
            self.categories=klst        
            self.axis_x.append(self.categories)              
            self.axis_y.setRange(min(vlst), max(vlst))
        self.chart_view.setVisible(True)
        
    #菜单选项        
    def winaction(self,action):
        q=action.text()
        if q=="说明":
            QtWidgets.QMessageBox.information(self,
                "程序说明：",
                "1、程序主要实现智能视频监控分析辅助管理，任务模型分三大类：人脸识别、图像分类、目标检测。\n\n\
2、存放任务模型默认目录分别是：cls-model(图像分类模型)、det-model(目标检测模型)、face-model(人脸分类模型),默认目录名不能更改\n\n\
3、任务模型默认目录里可以增加用户自己的模型目录，用来存放用户自已的推理模型文件\n")
        if q=="关于":
            # img=QtGui.QImage(":img/start.jpg")    
            # self.lbldst.setPixmap(QtGui.QPixmap.fromImage(img).scaled(768,512 , QtCore.Qt.KeepAspectRatio))
            self.lbldst.setText("智能视频监控分析辅助管理系统")
            self.lbldst.setScaledContents(True) #自适应大小
            QtWidgets.QMessageBox.about(self, "关于", "智能视频监控分析辅助管理系统")     
                    
    #文本框回车事件
    def on_linekey_returnPressed(self):
        #返回列表值的索引
        index=self.class_names.index(self.linekey.text())
        lstindex=self.slm.index(index)
        self.detlst.setCurrentIndex(lstindex)
        self.on_detlst_clicked(lstindex)
 
    #目标列表框选择事件
    def on_detlst_clicked(self,index):
        #获取选择的目标名称
        self.detobj=[]
        self.detobjcn=[] #中文标签
        detname=self.detlst.model().stringList()[index.row()]
        for i in self.detlst.selectedIndexes():
            f=self.detlst.model().stringList()[i.row()]
            fcn=self.class_names_cn[i.row()]
            self.detobj.append(f)    
            self.detobjcn.append(fcn)
        self.txtmsg.setText("当前检测的目标："+','.join(self.detobj)+'('+','.join(self.detobjcn)+')')                    
        return self.detobj
    
    #文件列表框选择事件    
    def on_lstfile_clicked(self,index):
        reslst=[]
        reslsten=[]
        self.tabWin=tableWindow() #实例化表格
        filename=self.lstfile.model().stringList()[index.row()]
        filepath=os.path.join("output",filename)
        with open(filepath, 'r',encoding="utf-8") as fp:
            reader = csv.reader(fp,skipinitialspace=True)
            for i,row in enumerate(reader):
                if i==0:
                    self.tabWin.model.setHorizontalHeaderLabels(row) #表头
                else:
                    reslst.append(row[4]) #取cnlabel列
                    reslsten.append(row[3])
                    for j,col in enumerate(row):
                        self.tabWin.model.setItem(i-1,j,QtGui.QStandardItem(row[j]))
            self.tabWin.tabview.setModel(self.tabWin.model)
                                    
    
        r=c.Counter(reslst)
        ren=c.Counter(reslsten)
        self.d=dict(r.most_common())
        self.den=dict(ren.most_common())
        self.top5=dict(r.most_common(5))
        #print(d)             
        #显示top5           
        self.chart_view.deleteLater()                         
        self.buildChart(self.horizontalLayout_6,"目标检测结果排名前5",True)
        self.chart_view.setFixedHeight(self.lbldst.height()*0.6)
        self.barChart(self.top5)        
        self.txtmsg.setText(f"目标检测结果文件统计分析（{filename}）(目标：次数)：\n"+str(self.d)+"\n"+str(self.den))
        
                   
    #显示完整图表        
    def showchartWin(self,event):
        self.tabWin.show() #显示表格窗体
        self.chart_view.deleteLater()
        self.chartWin=chartWindow() 
        self.chartWin.show()   
        #重新显示top5
        self.buildChart(self.horizontalLayout_6,"目标检测结果排名前5",True)
        #self.chart_view.setFixedHeight(self.height()*0.3)
        self.barChart(self.top5)        
        
                
    #更换录像机通道        
    def changecamid(self,i):
        if self.rbtipcam.isChecked():
            self.Open()
    #选择任务模型
    def schange(self,i):
        #print(i,self.cboxtask.itemText(i)) 
        self.class_names=[]       
        self.cboxmodel.clear()
        try:
            lst=os.listdir(os.path.join("models",self.cboxtask.itemText(i)))
            self.cboxmodel.addItems(lst)
        except:
            pass       
                     
    #选择模型
    def modelchange(self,i):
        self.prelabel=""
        self.preids=""
        self.class_names=[]       
        self.class_names_cn=[]       
        modeltype=self.cboxtask.currentText()       
        model_dir=os.path.join("models",self.cboxtask.currentText(),self.cboxmodel.currentText())
        self.label_file=os.path.join(model_dir,"labels.txt") 
        self.label_file_cn=os.path.join(model_dir,"cnlabels.txt") 
        
        if os.path.exists(self.label_file) and os.path.exists(self.label_file_cn):        
            if modeltype in ["det-model"]:
                self.class_names=self.get_labels(self.label_file)    
                self.class_names_cn=self.get_labels(self.label_file_cn)                    
            if modeltype in ["face-model","cls-model"]:                        
                #self.class_info=self.get_class_info(self.label_file)
                self.class_names=self.get_class_info(self.label_file)
                self.class_names_cn=self.get_class_info(self.label_file_cn)                     
        else:
            self.class_names=[]
            self.class_names_cn=[]
            #QtWidgets.QMessageBox.warning(self,"错误提示","缺少标签文件：labels.txt")
            
        self.slm=QtCore.QStringListModel()
        self.slm.setStringList(self.class_names)
        self.detlst.setModel(self.slm)
        #print(self.class_names,self.class_names_cn)
        self.txtmsg.setText("当前检测的目标："+','.join(self.class_names)+'('+','.join(self.class_names_cn)+')')
        self.detobj=self.class_names[:]   
        
    #获取录像机的信息
    def getipcam(self):
        self.ip=self.leip.displayText()
        self.camid=self.cboxcamid.currentText()
        self.user=self.leuser.displayText()
        self.lepwd.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.pwd=self.lepwd.displayText() #获取密码
        self.lepwd.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        url="rtsp://"+self.user+":"+self.pwd+"@"+self.ip+"/Streaming/Channels/"+self.camid+"01?transportmode=multicas"
        ret=cv2.VideoCapture(url)
        if ret.grab():
            return url
        else:
            self.rbtcam.setChecked(True)
            return 0
    
    #获取录像机的通道数
    def getcamid(self):
        self.ip=self.leip.displayText()      
        self.user=self.leuser.displayText()
        self.lepwd.setEchoMode(self.lepwd.Normal)
        self.pwd=self.lepwd.displayText() #获取密码
        self.lepwd.setEchoMode(self.lepwd.Password)
        camidlst=[]
        for camid in range(64):
            url="rtsp://"+self.user+":"+self.pwd+"@"+self.ip+":554/Streaming/Channels/"+str(camid).rjust(2,"0")+"01?transportmode=multicas"
            ret=cv2.VideoCapture(url)
            grabbed=ret.grab()
            if grabbed:
                camidlst.append(str(camid).rjust(2,"0"))
            QtWidgets.QApplication.processEvents()
        return camidlst
     
    #开启拍照或录制 
    def snap(self):
        if self.cap.isOpened():
            self.issnap=True
    def rec(self):
        if self.cap.isOpened():
            self.isrec =not self.isrec
            if self.isrec:
                #创建video writer
                ret,frame=self.cap.read()
                self.createVideo(frame)
                self.btnrec.setText("停止录制")    
                self.statusBar().showMessage("文件录制中…………\n")                    
            else:
                self.video.release() #释放video writer
                self.btnrec.setText("开始录制") 
                self.statusBar().showMessage("文件保存在output目录里\n")     
        
    #摄像头或监控拍照
    def imgsave(self,frame):
        if self.rbtcam.isChecked() or self.rbtipcam.isChecked() or self.rbtvideo.isChecked():
            fname=time.strftime("%Y%m%d%H%M%S",time.localtime())+".jpg"
            #fname=datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
            if not os.path.exists("output"):
                os.makedirs("output")                
            cv2.imwrite(os.path.join("output",fname),frame)
            self.statusBar().showMessage(fname+"文件保存在output目录里\n")
            self.issnap=False            
    #摄像头或监控录制            
    def createVideo(self,frame):
        if self.rbtcam.isChecked() or self.rbtipcam.isChecked() or self.rbtvideo.isChecked():
            fname=time.strftime("%Y%m%d%H%M%S",time.localtime())+".mp4"
            #fname=datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".mp4"
            if not os.path.exists("output"):
                os.makedirs("output")
            self.video=cv2.VideoWriter(
                filename=os.path.join("output",fname),
                fourcc=cv2.VideoWriter_fourcc(*"mp4v"),
                fps=15,
                frameSize=(frame.shape[1],frame.shape[0])
                ) 
            #video.write(frame)                    
            #video.release()
                
    
    #在label控件上显示图像 
    def imgshow(self,frame,lbl):
        lbl.setFixedSize(self.width()*0.5,self.height()*0.5)
        #img=QtGui.QImage(frame.data,frame.shape[1],frame.shape[0],QtGui.QImage.Format_BGR888)    
        #重载修复图像显示变形问题      
        img = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,QtGui.QImage.Format_BGR888)
        #是否图像隐藏
        self.isscaled=self.cboxscaled.isChecked()
        if self.isscaled:  
            lbl.setVisible(False)
        else:
            lbl.setVisible(True)
            lbl.setPixmap(QtGui.QPixmap.fromImage(img).scaled(lbl.width(), lbl.height(), QtCore.Qt.KeepAspectRatio))
            #lbl.setScaledContents(True) #自适应大小                        
        QtWidgets.QApplication.processEvents()
        
##########################################################################
    def get_class_info(self,file_path):
        class_info =[]
        with open(file_path, 'r',encoding="utf-8") as f:
            for line in f:
                line = line.strip('0123456789\n') #去数字                
                class_info.append(line.strip())
        return class_info
    
    #分类模型预测
    def ClsModel(self,model_dir):
        model_file=os.path.join(model_dir,"inference.pdmodel")
        params_file=os.path.join(model_dir,"inference.pdiparams")
        config_file=os.path.join(model_dir,"inference_cls.yaml")
        self.clsmodel = fd.vision.classification.PaddleClasModel(
            model_file, params_file, config_file)

    #写入csv文件
    def SaveCSV(self,predict_data):
        fname=time.strftime("%Y%m%d",time.localtime())+".csv"
        file_name=os.path.join("output",fname)
        if not os.path.exists(file_name):
            with open(file_name,"w",encoding="utf-8_sig",newline="") as fp:
                csvwriter=csv.writer(fp)
                csvwriter.writerow(["datetime","dev","type","label","cnlabel","probability"])

        #中文乱码解决，utf-8_sig
        with open(file_name,"a+",encoding="utf-8_sig",newline="") as fp:
            csvwriter=csv.writer(fp)
            #csvwriter.writerow(header)
            csvwriter.writerow(predict_data)
    
    #预测结果,
    def predict(self, img):   
        result = self.clsmodel.predict(img.copy())       
        #解析返回的结构体信息，获取ID和score
        #print(result)
        ids=result.label_ids
        label=self.class_names[result.label_ids[0]]
        cnlabel=self.class_names_cn[result.label_ids[0]]
        score=result.scores[0]      
        if self.cboxtask.currentText()=="face-model" and score<=0.8:
            return img
        #print(label,score)
        dt=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        res=[dt,self.dev,self.cboxtask.currentText(),label,cnlabel,round(score,2)]
       
        if label in self.detobj:  
            self.txtmsg.setText(label)
            if self.chkall.isChecked():
                self.SaveCSV(res)
            else:
                if self.prelabel=="" or self.prelabel!=label:
                    self.SaveCSV(res)
                cv2.putText(img, label+":"+str(round(score,2)),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
                self.prelabel =label #前一个预测标签
        return img
    
 
    #标签文本
    def get_labels(self,file_path):
        class_names=[]
        with open(file_path, 'r',encoding="utf-8") as f:
            for line in f:
                class_names.append(line.strip())
        return class_names

    #检测模型部署
    def DetModel(self,model_dir):
        model_file=os.path.join(model_dir,"model.pdmodel")
        params_file=os.path.join(model_dir,"model.pdiparams")
        config_file=os.path.join(model_dir,"infer_cfg.yml")
        self.detmodel=fd.vision.detection.PPYOLOE(model_file,params_file,config_file,
                                                  runtime_option=None,model_format=fd.ModelFormat.PADDLE)         
    #检测结果
    def detect(self,img):
        result=self.detmodel.predict(img.copy())
        #vis_img= fd.vision.vis_detection(img,result,score_threshold=0.5)
        idslst=[]
        #获取大于score的目标IDs
        scorelst=result.scores
        for i,score in enumerate(scorelst):
            if score>=0.5:
                idslst.append(result.label_ids[i])
        #print(set(idslst))
        ids="".join(list(map(lambda x:str(x),set(idslst)))) #数字元素转字符串
        reslst=str(result).split("\n")
        for res in reslst[1:-1]:
            r=res.split(",")        
            if float(r[4].strip())>=0.5:
                x0=int(float(r[0].strip()))
                y0=int(float(r[1].strip()))
                x1=int(float(r[2].strip()))
                y1=int(float(r[3].strip()))
                id=int(r[5].strip())
                #print(x0,y0,x1,y1,id) #(xmin,ymin,xmax,ymax), id
                idcolor=((id*50)%255,(id*100)%255,(id*200)%255) #id颜色区分
                label=self.class_names[id]
                if label in self.detobj: #只显示和保存要检测的目标
                    cv2.rectangle(img,(x0,y0),(x1,y1),idcolor,2) #画框              
                    cv2.putText(img,self.class_names[id]+":"+str(round(float(r[4].strip()),2)),(x0+5,y0+10),cv2.FONT_HERSHEY_SIMPLEX,0.6,idcolor,2) #目标名称
                    dt=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
                    rdata=[dt,self.dev,self.cboxtask.currentText(),self.class_names[id],self.class_names_cn[id],round(float(r[4].strip()),2)]
                    #csv_file=os.path.join("output","predict_result.csv")        
                    self.txtmsg.setText("当前检测的目标："+','.join(self.detobj)+"\n"+str(rdata))
                    if self.chkall.isChecked():
                        self.SaveCSV(rdata)
                    else:
                        if self.prelabel=="" or self.prelabel!=label:
                            if self.preids=="" or self.preids!=ids:
                                self.SaveCSV(rdata)
                        self.prelabel=label
        self.preids=ids
        return img
    
##########################################################################
    #打开输入数据类型
    def Open(self):        
        self.Close()
        self.isstop=False      
        self.isscaled=self.cboxscaled.isChecked()
        #获取选项按钮状态
        self.iscam=self.rbtcam.isChecked()
        self.isimg=self.rbtimg.isChecked()
        self.isvideo=self.rbtvideo.isChecked()
        self.isipcam=self.rbtipcam.isChecked()
        
        taskid=self.cboxtask.currentIndex()
        task=self.cboxtask.currentText()
        model_dir=os.path.join("models",self.cboxtask.currentText(),self.cboxmodel.currentText())
        
        
        #print(model_dir) 
        #图像缩放
        self.isscaled=self.cboxscaled.isChecked()                         
        
        if taskid==0:#预览
            if self.isimg:
                self.fileName, self.fileType = QtWidgets.QFileDialog.getOpenFileName(self, '选择','', "图像文件(*.jpg *.png)")
                if self.fileName!="":
                    #frame=cv2.imread(self.fileName)          
                    frame=cv2.imdecode(np.fromfile(self.fileName,dtype=np.uint8),cv2.IMREAD_COLOR) #兼容中文路径问题                  
                    self.imgshow(frame,self.lbldst)            
            else:
                 self.Display()
        else:#预测
            if self.iscam or self.isipcam:
                if self.isipcam:
                    self.dev=self.leip.text()+":"+self.cboxcamid.currentText() #dev
                if self.iscam:
                    self.dev="VideoCameran" #dev
                if task in ["face-model"] :
                    self.ClsModel(model_dir)
                    self.cls_videodetect(model_dir,isface=True)
                if task in ["cls-model"]:
                    self.ClsModel(model_dir)
                    self.cls_videodetect(model_dir,isface=False)
                if  task in ["det-model"]:
                    self.DetModel(model_dir)
                    self.det_videodetect(model_dir)
                
                
            if self.isimg:
                self.fileName, self.fileType = QtWidgets.QFileDialog.getOpenFileName(self, '选择','', "图像文件(*.jpg *.png)")
                if self.fileName!="":
                    #frame=cv2.imread(self.fileName)       
                    frame=cv2.imdecode(np.fromfile(self.fileName,dtype=np.uint8),cv2.IMREAD_COLOR) #兼容中文路径问题                     
                    self.imgshow(frame,self.lbldst)   
                    self.dev=self.fileName #dev
                
                #print(task)
                if task in ["face-model"]:#调用图像分类-人脸检测与识别任务,结果显示在dst上           
                    self.ClsModel(model_dir)     
                    self.cls_imgpredict(model_dir,self.fileName,isface=True)#预测返回结果
                                        
                if task in ["cls-model"]: #调用图像分类-
                    self.ClsModel(model_dir)
                    self.cls_imgpredict(model_dir,self.fileName,isface=False)#预测返回结果
                
                if  task in ["det-model"]:#调用目标检测-
                    self.DetModel(model_dir)
                    self.det_imgpredict(model_dir,self.fileName)
                                                                                
            if self.isvideo:
                self.fileName, self.fileType = QtWidgets.QFileDialog.getOpenFileName(self, '选择视频文件','', '*.mp4')
                if self.fileName!="":
                    self.dev=self.fileName #dev
                    if task in ["face-model"] :
                        self.ClsModel(model_dir)
                        self.cls_videodetect(model_dir,self.fileName,isface=True)
                    if task in ["cls-model"]:
                        self.ClsModel(model_dir)
                        self.cls_videodetect(model_dir,self.fileName,isface=False)
                    if  task in ["det-model"]:
                        self.DetModel(model_dir)
                        self.det_videodetect(model_dir,self.fileName)
                    
            
    #显示数据            
    def Display(self):
        isscaled=self.cboxscaled.isChecked()
        if self.isipcam:
            self.cap=cv2.VideoCapture(self.getipcam())
        if self.iscam:
            self.cap = cv2.VideoCapture(0)
        if self.isvideo:
            self.fileName, self.fileType = QtWidgets.QFileDialog.getOpenFileName(self, '选择视频文件','', '*.mp4')
            self.cap=cv2.VideoCapture(self.fileName)
        while self.cap.isOpened():
            ret,frame=self.cap.read()
            if not ret:
                break        
                
            if self.rbtcam.isChecked() or self.rbtipcam.isChecked() or self.rbtvideo.isChecked():
                if self.issnap:
                    self.imgsave(frame)
                if self.isrec:#开始录制
                    self.video.write(frame)   
            else:
                self.issnap = False
                self.isrec = False
                self.btnrec.setText("开始录制") 
                self.statusBar().showMessage("当前模式不支持拍照和录制")            
                                                     
            #if self.rbtipcam.isChecked():
            #获取帧宽
            w= int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h= int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            if w>1024 and w<=1920:
                w,h=w//2,h//2
                frame=cv2.resize(frame, (w,h))#缩小图像
            elif w>1920:
                w,h=w//4,h//4
                frame=cv2.resize(frame, (w,h))#缩小图像 
            self.imgshow(frame,self.lbldst)    
            cv2.waitKey(0)
            if self.isstop:
                if self.isrec:
                    self.video.release()
                    self.btnrec.setText("开始录制")
                    self.statusBar().showMessage("文件保存在output目录里\n") 
                    self.isrec=False
                
                self.cap.release()
                break
        self.cap.release()
    #关闭显示   
    def Close(self):             
        if self.rbtcam.isChecked() or self.rbtvideo.isChecked() or self.rbtipcam.isChecked():
            self.isstop=True 
        try:
            self.cap.release()    
        except:
            pass                
        self.lbldst.clear()        
        #self.resize(self.screengeometry.width()*0.7,self.screengeometry.height()*0.7)

                  
    #图像文件分类检测（人脸检测与识别）    
    def cls_imgpredict(self,model_dir,imgfile:str,isface=True):
        #创建推理
        if isface:
            #加载人脸检测分类器
            face_detector = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
            #img=cv2.imread(imgfile)
            img=cv2.imdecode(np.fromfile(imgfile,dtype=np.uint8),cv2.IMREAD_COLOR)
            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces=face_detector.detectMultiScale(gray,1.3,5)
            # 如果有检测有结果，画框        
            if len(faces)>0:
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)
                    faceimg=img[y:y+h,x:x+w] #人脸图像
                    faceimg=self.predict(faceimg)
                    img[y:y+h,x:x+w]=faceimg
                                              
        else:
            #img=cv2.imread(imgfile)
            img=cv2.imdecode(np.fromfile(imgfile,dtype=np.uint8),cv2.IMREAD_COLOR)
            img=self.predict(img)
        self.imgshow(img,self.lbldst) 

    #图像分类-视频-人脸检测并识别
    def cls_videodetect(self,model_dir,*videofile:str,isface=True):        
        self.isscaled=self.cboxscaled.isChecked()
        if isface:
            #加载人脸检测分类器
            face_detector = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml') 
            if  videofile:
                self.cap=cv2.VideoCapture(videofile[0])
            else:
                if self.isipcam:
                    self.cap=cv2.VideoCapture(self.getipcam())
                if self.iscam:
                    self.cap = cv2.VideoCapture(0)
            while self.cap.isOpened:
                #读取数据
                ret,frame=self.cap.read()
                if not ret:
                    break
                if self.rbtcam.isChecked() or self.rbtipcam.isChecked() or self.rbtvideo.isChecked():
                    if self.issnap:
                        self.imgsave(frame)
                    if self.isrec:#开始录制
                        self.video.write(frame)   
                else:
                    self.issnap = False
                    self.isrec = False
                    self.btnrec.setText("开始录制") 
                    self.statusBar().showMessage("当前模式不支持拍照和录制")  
                #获取帧宽
                w= int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                h= int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                if w>1024 and w<=1920:
                    w,h=w//2,h//2
                    frame=cv2.resize(frame, (w,h))#缩小图像
                elif w>1920:
                    w,h=w//4,h//4
                    frame=cv2.resize(frame, (w,h))#缩小图像      
                #print(frame.shape)
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                #if self.rbtipcam.isChecked():
                       
                self.imgshow(frame,self.lbldst)
                faces=face_detector.detectMultiScale(gray,1.3,5)
                # 如果有检测有结果，画框        
                if len(faces)>0:
                    for (x,y,w,h) in faces:
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
                        faceimg=frame[y:y+h,x:x+w] #人脸图像
                        faceimg=self.predict(faceimg)
                        frame[y:y+h,x:x+w]=faceimg
                self.imgshow(frame,self.lbldst)               
                cv2.waitKey(15)
                #
                if self.isstop:
                    break
            self.cap.release()
                
        else:#不是人脸检测识别，是普通图像分类
            if  videofile:
                self.cap=cv2.VideoCapture(videofile[0])
            else:
                if self.isipcam:
                    self.cap=cv2.VideoCapture(self.getipcam())
                if self.iscam:
                    self.cap = cv2.VideoCapture(0)
            while self.cap.isOpened:
                #读取数据
                ret,frame=self.cap.read()
                if not ret:
                    break
                if self.rbtcam.isChecked() or self.rbtipcam.isChecked() or self.rbtvideo.isChecked():
                    if self.issnap:
                        self.imgsave(frame)
                    if self.isrec:#开始录制
                        self.video.write(frame)   
                else:
                    self.issnap = False
                    self.isrec = False
                    self.btnrec.setText("开始录制") 
                    self.statusBar().showMessage("当前模式不支持拍照和录制")   
                    
                #获取帧宽
                w= int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                h= int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                if w>1024 and w<=1920:
                    w,h=w//2,h//2
                    frame=cv2.resize(frame, (w,h))#缩小图像
                elif w>1920:
                    w,h=w//4,h//4
                    frame=cv2.resize(frame, (w,h))#缩小图像 
                self.imgshow(frame,self.lbldst)

                frame=self.predict(frame)
                self.imgshow(frame,self.lbldst)                   
                cv2.waitKey(0)
                
                                  
                if self.isstop:
                    break
            self.cap.release()
            
    
    #目标检测-图象
    def det_imgpredict(self,model_dir,imgfile:str):
        img=cv2.imread(imgfile)   
        img=self.detect(img)
        self.imgshow(img,self.lbldst)
    
    #目标检测-视频 
    def det_videodetect(self,model_dir,*videofile:str):
        self.isscaled=self.cboxscaled.isChecked()
        if  videofile:
            self.cap=cv2.VideoCapture(videofile[0])
        else:
            if self.isipcam:
                self.cap=cv2.VideoCapture(self.getipcam())
            if self.iscam:
                self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            if self.rbtcam.isChecked() or self.rbtipcam.isChecked() or self.rbtvideo.isChecked():
                if self.issnap:
                    self.imgsave(frame)
                if self.isrec:#开始录制
                    self.video.write(frame)     
            else:
                self.issnap = False
                self.isrec = False
                self.btnrec.setText("开始录制") 
                self.statusBar().showMessage("当前模式不支持拍照和录制")          
            #获取帧宽
            w= int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h= int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            if w>1024 and w<=1920:
                w,h=w//2,h//2
                frame=cv2.resize(frame, (w,h))#缩小图像
            elif w>1920:
                w,h=w//4,h//4
                frame=cv2.resize(frame, (w,h))#缩小图像  
            self.imgshow(frame,self.lbldst)
            if ret:
                 frame = self.detect(frame)
                 self.imgshow(frame,self.lbldst)
            else:
                break            
            cv2.waitKey(10)
            if self.isstop:
                break
        self.cap.release()
    
#图表窗体
class chartWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图表")
        screengeometry=self.screen().availableGeometry()
        self.resize(screengeometry.width()*0.5,screengeometry.height()*0.5)
        self.layout=QtWidgets.QHBoxLayout(self)

        mywin.buildChart(self.layout,"检测目标次数",True)
        #print(mywin.d)
        mywin.barChart(mywin.d)
        
#表格窗体
class tableWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("表格")
        screengeometry = self.screen().availableGeometry()
        self.resize(screengeometry.width()*0.6, screengeometry.height()*0.6)
        self.tabview=QtWidgets.QTableView()
        self.layout=QtWidgets.QHBoxLayout(self)
        self.model=QtGui.QStandardItemModel()
        #self.tabview.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        #self.tabview.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)  
        self.tabview.horizontalHeader().setStretchLastSection(True) #
        self.layout.addWidget(self.tabview)
 
if __name__ == '__main__':
    try:
        app=QtWidgets.QApplication(sys.argv)        
        app.processEvents()
        serverName="AppServer"
        socket=QtNetwork.QLocalSocket()
        socket.connectToServer(serverName)
        #防止程序实例重复启动
        if socket.waitForConnected(500):
            app.quit()
        else:
            localServer=QtNetwork.QLocalServer()
            localServer.listen(serverName)
            mywin=MainWindow()
            mywin.setWindowTitle("智能视频监控分析辅助管理系统")            
            mywin.show()                     
            sys.exit(app.exec())
             
    except:
        pass
