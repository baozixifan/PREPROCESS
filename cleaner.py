import json
import os
import shutil


class JsonCleaner():
    def __init__(self, projectPath):
        self.projectPath = projectPath
        self.jsonPath = os.path.join(projectPath, "completions")
        self.nanPath = os.path.join(projectPath, "nan")
        self.listPath = self._storeJson()
    
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
        修正：已注释掉清理
        '''
        if os.path.exists(self.nanPath) == False:
            os.mkdir(self.nanPath)

        # self._ClearFile(self.nanPath)

    def loadJson(self):
        for jsonName in self.listPath:
            jsonName = os.path.join(self.jsonPath, jsonName)
            f =  open(jsonName, 'r')
            jsonDict = json.load(f)
            # print(f"{i} = {jsonDict}")
            num = 0
            for item in jsonDict["completions"]:
                if item["result"]: #判断result是否为空
                    num += 1
            print(f"num = {num}")
            f.close()

            if num == 0:
                #copy or move
                self._move(jsonDict["data"]["audio"].replace('/','\\')[1:], jsonName)
                print("*"*10)

    def _copy(self, waveName, jsonName):
        waveName = os.path.join(self.projectPath, waveName)
        if os.path.exists(waveName) == True:
            shutil.copy(waveName, self.nanPath)
            shutil.copy(jsonName, self.nanPath)

    def _move(self, waveName, jsonName):
        waveName = os.path.join(self.projectPath, waveName)
        if os.path.exists(waveName) == True:
            shutil.move(waveName, self.nanPath)
            shutil.move(jsonName, self.nanPath)



if __name__ == "__main__":
    JSclean = JsonCleaner(
        projectPath=r"E:\项目汇报node\三门峡项目\音频切分程序与文档\原始数据集\project8090")
    JSclean.fileExistClear()
    JSclean.loadJson()

        



    
        