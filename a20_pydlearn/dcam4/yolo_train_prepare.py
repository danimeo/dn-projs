import csv
import shutil
import os

def copyfile(srcfile, dstpath):                       # 复制函数
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(srcfile)             # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)                       # 创建路径
        shutil.copy(srcfile, os.path.join(dstpath, fname))          # 复制文件
        print("copy %s -> %s"%(srcfile, os.path.join(dstpath, fname)))

root = r"F:\datasets\自己的monitor数据集"

with open(r"F:\datasets\自己的monitor数据集\project-3-at-2023-05-14-10-52-18fb9fcd (1).csv", 'r', encoding='utf-8') as f: 
   cr = csv.reader(f)
   for row in cr:
       cls_name = row[0]
       file_path = row[6][13:]
       copyfile(os.path.join(root, file_path), os.path.join(root, 'out', cls_name))
