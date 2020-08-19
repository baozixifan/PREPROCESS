import os
import shutil
import chardet
import re


def statistics(files:list,div :list):
    """
    #统计Y和N的数量，并按比例划分数据集
    """
#计数器
    Y = 0
    N = 0
#划分字典与链表
    divDict = {}
    listY = []
    listN = []
    for fileName in files:
        if fileName[0] == "Y":
            Y += 1
        else:
            N += 1

    listY.append(Y//sum(div)*div[0])
    listY.append(Y//sum(div)*(div[0]+div[1]))
    listN.append(N//sum(div)*div[0])
    listN.append(N//sum(div)*(div[0]+div[1]))
    divDict["Y"] = listY
    divDict["N"] = listN

    return  divDict

def RenameAndMove(origPath,destPath):
    Ynum = 0
    Nnum = 0
    
    for root, dirs, files in os.walk(origPath): 
        divDict = statistics(files,[8,1,1])
        print(divDict)
        for fileName in files:
            if fileName[0] == "Y":
                if Ynum < divDict["Y"][0]:
                    oldName = root + "\\" + fileName
                    # print(f"oldName = {oldName}")
                    destName = destPath + fileName
                    shutil.copyfile(oldName,destName)
                    newName = destPath + "\\" + "BAC009" + "S1071" + "W" + str(Ynum).zfill(4) + fileName[-4:]
                    # print(f"newName = {newName}")
                    os.rename(destName,newName)
                elif Ynum < divDict["Y"][1]:
                    oldName = root + "\\" + fileName
                    # print(f"oldName = {oldName}")
                    destName = destPath + fileName
                    shutil.copyfile(oldName,destName)
                    newName = destPath + "\\" + "BAC009" + "S1072" + "W" + str(Ynum-divDict["Y"][0]).zfill(4) + fileName[-4:]
                    # print(f"newName = {newName}")
                    os.rename(destName,newName)
                else:
                    oldName = root + "\\" + fileName
                    # print(f"oldName = {oldName}")
                    destName = destPath + fileName
                    shutil.copyfile(oldName,destName)
                    newName = destPath + "\\" + "BAC009" + "S1073" + "W" + str(Ynum-divDict["Y"][1]).zfill(4) + fileName[-4:]
                    # print(f"newName = {newName}")
                    os.rename(destName,newName)                    

                Ynum += 1
            else:
                if Nnum < divDict["N"][0]:
                    oldName = root + "\\" + fileName
                    # print(f"oldName = {oldName}")
                    destName = destPath + fileName
                    shutil.copyfile(oldName,destName)
                    newName = destPath + "\\" + "BAC009" + "S2071" + "W" + str(Nnum).zfill(4) + fileName[-4:]
                    # print(f"newName = {newName}")
                    os.rename(destName,newName)
                elif Nnum < divDict["N"][1]:
                    oldName = root + "\\" + fileName
                    # print(f"oldName = {oldName}")
                    destName = destPath + fileName
                    shutil.copyfile(oldName,destName)
                    newName = destPath + "\\" + "BAC009" + "S2072" + "W" + str(Nnum-divDict["N"][0]).zfill(4) + fileName[-4:]
                    # print(f"newName = {newName}")
                    os.rename(destName,newName)
                else:
                    oldName = root + "\\" + fileName
                    # print(f"oldName = {oldName}")
                    destName = destPath + fileName
                    shutil.copyfile(oldName,destName)
                    newName = destPath + "\\" + "BAC009" + "S2073" + "W" + str(Nnum-divDict["N"][1]).zfill(4) + fileName[-4:]
                    # print(f"newName = {newName}")
                    os.rename(destName,newName)                    

                Nnum += 1

def WriteInTxt(transcript,labelDest,NAN):
    ClearFile(NAN)
    for root, dirs, files in os.walk(labelDest):
        for fileName in files:
            filePath = root + "\\" +fileName
            print(filePath)
       
            try:
                with open(filePath,mode="r") as fileOld:
                    context = fileOld.read() 
                with open(transcript,mode="a",encoding="utf-8") as fileNew:
                    newContext = fileName[:-4] + " " + re.sub(reg, '', context) + "\n"
                    newContext.encode(encoding='UTF-8')
                    fileNew.write(newContext)
                    print("*"*50)
            except:
            #TODO 清空NAN文件夹，将错误文件复制进去。
                shutil.copy(filePath,NAN)

            # with open(filePath,mode="r",encoding="utf-8") as fileOld:
            #     context = fileOld.read() 
            # with open(transcript,mode="a",encoding="utf-8") as fileNew:
            #     newContext = fileName + " " + context + "/r/n"
            #     newContext.encode(encoding='UTF-8')
            #     fileNew.write(newContext)
            # pass

def MoveAudio(oldPath,newPath):
    newPathTrain = newPath + r"\train"
    trainS1 = newPathTrain + r"\S1XX1"
    trainS2 = newPathTrain + r"\S2XX1"
    newPathDev = newPath + r"\dev"
    devS1 = newPathDev + r"\S1XX2"
    devS2 = newPathDev + r"\S2XX2"
    newPathTest = newPath + r"\test"
    testS1 = newPathTest + r"\S1XX3"
    testS2 = newPathTest + r"\S2XX3"
    
    #验证路径是否存在
    if os.path.exists(newPath) == False:
        os.mkdir(newPath)
    if os.path.exists(newPathTrain) == False:
        os.mkdir(newPathTrain)
    if os.path.exists(newPathDev) == False:
        os.mkdir(newPathDev)
    if os.path.exists(newPathTest) == False:
        os.mkdir(newPathTest)
    if os.path.exists(trainS1) == False:
        os.mkdir(trainS1)
    if os.path.exists(trainS2) == False:
        os.mkdir(trainS2)
    if os.path.exists(devS1) == False:
        os.mkdir(devS1)
    if os.path.exists(devS2) == False:
        os.mkdir(devS2)
    if os.path.exists(testS1) == False:
        os.mkdir(testS1)
    if os.path.exists(testS2) == False:
        os.mkdir(testS2)

    for root, dirs, files in os.walk(oldPath):
        print(root)
        for fileName in files:
            if fileName[10] == '1':
                if fileName[7] == '1':
                    shutil.copy(root+'\\'+fileName, trainS1)
                elif fileName[7] == '2':
                    shutil.copy(root+'\\'+fileName, trainS2)                    
            elif fileName[10] == '2':
                if fileName[7] == '1':
                    shutil.copy(root+'\\'+fileName, devS1)
                elif fileName[7] == '2':
                    shutil.copy(root+'\\'+fileName, devS2)    
            elif fileName[10] == '3':
                if fileName[7] == '1':
                    shutil.copy(root+'\\'+fileName, testS1)
                elif fileName[7] == '2':
                    shutil.copy(root+'\\'+fileName, testS2)    



def ClearFile(filePath):
    '''
    判断文件夹路径是否存在，不存在则创建
    清空需要存放文件的文件夹
    :param filePath: 存放文件的文件夹路径
    :return :
    '''
    if os.path.exists(filePath) == False:
        os.mkdir(filePath)

    for i in os.listdir(filePath):
        path_file = os.path.join(filePath,i)  # 取文件绝对路径
        os.remove(path_file)

if __name__ == "__main__":

    reg = "[^0-9A-Za-z\u4e00-\u9fa5]"

    root = r"D:\版本音频处理\10.0"
    audio = root + r"\resample"
    label = root + r"\completions"
    audioDest = root + r"\resampleDest"
    labelDest = root + r"\completionsDest"
    NAN = root + r"\NAN"
    transcript = root + r"\transcript.txt"
    finalPath = root +r"\localism"

    '''
    程序第一阶段，audio和label改名，版本说话人名字注意修改。
    '''
    ClearFile(labelDest)
    RenameAndMove(label,labelDest)
    ClearFile(audioDest)
    RenameAndMove(audio,audioDest)

    '''
    程序第二阶段，将labelDest转为一个transcript文本文件。
    '''
    if os.path.exists(NAN) == False:
        os.mkdir(NAN)

    WriteInTxt(transcript,labelDest,NAN)
    judge = os.listdir(NAN)
    if len(judge) != 0:
        print("请更正NAN文件夹中的错误文件，并删除transcript，重新生成") 
    else:
        if os.path.exists(finalPath) == False:
            os.mkdir(finalPath)        
        #将audio划分至三个文件夹
        MoveAudio(audioDest,finalPath)
    
    # print("ok")
    # pass


