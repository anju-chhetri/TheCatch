import torch
import cv2
import numpy as np
import os

class ImageRecog():
    imgPath = None
    def __init__(self, imagepath):
        self.imgPath = imagepath

    def detection(self):
        weight = os.getcwd()  + '/CriminalRecog.pt'
        model = torch.hub.load("/home/anju_chhetri/Desktop/DBMS/Project/yolov5/", "custom",path = weight,  force_reload = True, source = "local")  #------>add yolov5 path
        img = cv2.imread(self.imgPath)
        img = cv2.resize(img, (416, 416))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = model(img, size = 416)
        className = result.pandas().xyxy[0]
        confDummy = 0
        index = 0
        name = ""
        for conf in className['confidence']:
            if(conf>confDummy):
                confDummy = conf
                name= className["name"][index]
            index+=1
        return(name,confDummy)
