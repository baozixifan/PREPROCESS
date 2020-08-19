import json
import os
import shutil
import torch
from wavTools import *
import torchaudio as ta

class JsonCutter():
    def __init__(self, projectPath, destPath):
        self.projectPath = projectPath
        self.jsonPath = os.path.join(projectPath, "completions")
        self.listPath = self._storeJson()
        self.destPath = destPath
        self.destComp = os.path.join(destPath, "completions")
        self.destUpload = os.path.join(destPath, "upload")
    
    def _storeJson(self):
        listPath = [i for i in os.listdir(self.jsonPath)]
        # print(f"listPath = {listPath}")
        return listPath

    def _ClearFile(self, filePath):
        '''
        清空需要存放文件的文件夹
        :param filePath: 存放文件的文件夹路径
        :return : 111
        '''
        # print(filePath)
        for i in os.listdir(filePath):
            # print(i)
            path_file = os.path.join(filePath,i)  # 取文件绝对路径
            os.remove(path_file)

    def fileExistClear(self):
        '''
        路径存在判断与清理
        '''
        if os.path.exists(self.destPath) == False:
            os.mkdir(self.destPath)
        if os.path.exists(self.destUpload) == False:
            os.mkdir(self.destUpload)
        if os.path.exists(self.destComp) == False:
            os.mkdir(self.destComp)

        self._ClearFile(self.destUpload)
        self._ClearFile(self.destComp)

    def _cutRename(self, dic, waveName):
        '''
        :param dic:存放一个json文件的字典，keys为id，value第一位为人物分类；第二位开始时间；第三位结束时间；第四位语音内容
        '''

        waveName = os.path.join(self.projectPath, waveName["audio"].replace('/','\\')[1:])
        print(waveName)
        waveNamePart = os.path.split(waveName)[-1][:-4]
        # print(waveNamePart)
        # print(list(dic.keys()))

        for i in list(dic.keys()):
            # print(dic[i][0])

            if len(dic[i]) == 4: #判断dic完整，过滤掉要素不全的dic

                flag = "O" #说话者标志位

                if dic[i][0][0] == "来访者":
                    flag = "N"   
                elif dic[i][0][0] == "客服":
                    flag = "Y" 
                else:
                    raise AssertionError
                context = dic[i][3][0] #文本写入内容
                
                destWaveName = os.path.join(self.destUpload, flag + waveNamePart + "_" + i + ".wav")
                destTxtName = os.path.join(self.destComp, flag + waveNamePart + "_" + i + ".txt")
                # print(destTxtName)
                get_ms_part_wav(waveName, dic[i][1]*1000, dic[i][2]*1000+1, destWaveName)
                with open(destTxtName, 'w') as f:
                    f.write(context)


    def loadJson(self):
        for jsonName in self.listPath:
            jsonName = os.path.join(self.jsonPath, jsonName)
            print("*"*10)
            print(f"jsonName = {jsonName}")
            f =  open(jsonName, 'r')
            jsonDict = json.load(f)
            # print(f"{i} = {jsonDict}")
            num = 0
            # listFile = []
            for item in jsonDict["completions"]:
                # print(item)
                dic = {}
                if item["result"]:#判断result是否为空
                    for j in item["result"]:
                        # print(f"j = {j}")
                        if j["from_name"] == "label":
                            dic.setdefault(j["id"],[]).append(j["value"]["labels"])
                            dic.setdefault(j["id"],[]).append(j["value"]["start"])
                            dic.setdefault(j["id"],[]).append(j["value"]["end"])
                        # elif j["from_name"] == "gender":
                        #     dic.setdefault(j["id"],[]).append(j["value"]["choices"])
                        elif j["from_name"] == "transcription":
                            dic.setdefault(j["id"],[]).append(j["value"]["text"])
                    print(dic)
                    self._cutRename(dic,jsonDict["data"])                                        
                else:
                    pass

                
            f.close()

class Resample(JsonCutter):
    def __init__(self, sourcePath, destPath):
        self.sourcePath = sourcePath
        self.destPath = destPath

    def fileExistClear(self, filePath):
        if os.path.exists(filePath) == False:
            os.mkdir(filePath)
        self._ClearFile(filePath)
            
    def resample(self):
        self.fileExistClear(self.destPath)
        errorName = []
        for root, dirs, files in os.walk(self.sourcePath):
            for fileName in files:
                wave = ta.load_wav(os.path.join(root, fileName))
                resampleObj = ta.transforms.Resample(orig_freq = 8000, new_freq = 16000)
                #TODO print name
                print(f"fileName = {fileName}")
                # print(f"wave = {wave}")
                try:
                    wave = resampleObj(wave[0])
                    ta.save(filepath = os.path.join(self.destPath, fileName), src = wave, sample_rate = 16000)
                except:
                    errorName.append(fileName[:-4])
                
        print(errorName)





if __name__ == "__main__":
    #stage 1:cut and move
    Cutter = JsonCutter(
        projectPath=r"E:\项目汇报node\三门峡项目\音频切分程序与文档\原始数据集\project8090-20200808\project8090",
        destPath=r"D:\版本音频处理\10.6")
        
    Cutter.fileExistClear()
    Cutter.loadJson()

    #stage 2:resample
    RS = Resample(r"D:\版本音频处理\10.6\upload", r"D:\版本音频处理\10.6\resample")
    RS.resample()




        


