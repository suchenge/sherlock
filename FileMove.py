#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,os.path,shutil

rootPath = "/Users/vito/Downloads/Temp/Xunlei/12月國產APP原版合集/"
movePath = "/Users/vito/Movies/"

for childNode in os.listdir(rootPath):
    childNodePath = os.path.join(rootPath, childNode)
    if os.path.isdir(childNodePath):
        files = os.listdir(childNodePath)
        for file in os.listdir(childNodePath):
            if file.endswith(".jpg") != True:

                oldFilePath = os.path.join(childNodePath, file)
                file_name, file_extension = os.path.splitext(oldFilePath)
                fileName = file_name.replace(childNodePath, "").replace("/","").replace("[u9c9.com]","").replace(file_extension,"")
                newFileName = childNode.replace("/","") + "-" + fileName + file_extension
                newFilePath = os.path.join(movePath, newFileName)

                print oldFilePath
                print newFilePath
                shutil.move(oldFilePath, newFilePath)
            


