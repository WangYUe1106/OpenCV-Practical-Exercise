import csv
import subprocess
import os

#要下的数据集rain,test,valid
runMode = "train"
#类别
classes = ["Snowman"]

with open('class-descriptions-boxable.csv', mode='r') as infile:
    reader = csv.reader(infile)
    dict_list = {rows[1]:rows[0] for rows in reader}

#删除以前下载的
subprocess.run(['rd', '/s/q', 'JPEGImages'],shell=True)
subprocess.run(['mkdir', 'JPEGImages'],shell=True)

subprocess.run(['rd', '/s/q', 'labels'],shell=True)
subprocess.run(['mkdir', 'labels'],shell=True)

for ind in range(0, len(classes)):
    
    className = classes[ind]
    print("Class " + str(ind) + " : " + className)
    
    strs = dict_list[className]
    commandStr = "findstr /r "+ '"\<' + strs + '\>"' + " " + runMode + "-annotations-bbox.csv"

    class_annotations = subprocess.run(commandStr, stdout=subprocess.PIPE,shell=True).stdout.decode('utf-8')
    class_annotations = class_annotations.splitlines()
    print(commandStr.split(','))
    #多少张图像被下载
    totalNumOfAnnotations = len(class_annotations)
    print("Total number of annotations : "+str(totalNumOfAnnotations))

    cnt = 0
    for line in class_annotations[0:totalNumOfAnnotations]:
        cnt = cnt + 1
        print("annotation count : " + str(cnt))
        lineParts = line.split(',')
        subprocess.run([ 'aws', 's3', '--no-sign-request', '--only-show-errors', 'cp', 's3://open-images-dataset/'+runMode+'/'+lineParts[0]+".jpg", 'JPEGImages/'+lineParts[0]+".jpg"],shell=True)
        with open('labels/%s.txt'%(lineParts[0]),'a') as f:
            f.write(' '.join([str(ind),str((float(lineParts[5]) + float(lineParts[4]))/2), str((float(lineParts[7]) + float(lineParts[6]))/2), str(float(lineParts[5])-float(lineParts[4])),str(float(lineParts[7])-float(lineParts[6]))])+'\n')





