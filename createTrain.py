import re
from tqdm import tqdm
import time
import random
query = open('F:\data\wiki-clir\english\wiki_en.queries','r',encoding='utf-8')
doc = open('out.txt','r',encoding='utf-8')
d = doc.readlines()
q = query.readlines()
querys2idx = {}
querys = {}
docs = {}
ids = []
cnt = 0
for i in tqdm(range(len(q))):
    line = q[i]
    tmp = line.split('\t')
    querys[tmp[0]]=tmp[2][:-1]
    querys2idx[tmp[2][:-1]]=tmp[0]
query.close()
for i in tqdm(range(len(d))):
    line = d[i]
    tmp = line.split('\t')
    ids.append(tmp[0])
    while ''in tmp:tmp.remove('')
    try:
        if(tmp[2][-1]=='\n'):
            docs[tmp[0]]=re.sub('}}','',tmp[2][:-1])
        else:
            docs[tmp[0]] = re.sub('}}','',tmp[2])
    except:
        print(tmp)
doc.close()
def getRandom():
    return ids[random.randrange(0,len(ids))]
f = open('en-de+en_train.txt','r',encoding='utf-8')
fs = f.readlines()
out = open('en-de+en_train0.txt','w',encoding='utf-8')
buffer = []
cnt = -1
for i in tqdm(range(len(fs))):
    #新的一个query 清空buffer

    tmp = fs[i].split('\t')
    if(tmp!=None and len(tmp)<3):continue
    #判定该line有效才cnt+1，有可能存在无效条目
    cnt+=1
    if cnt % 5 == 0: buffer = []
    #文件拆分，防止内存不够用
    if (cnt+1)%400000 == 0:
        name = 'en-de+en_train{}'.format(int((cnt+1)/400000))
        out.close()
        out = open(name,'w',encoding='utf-8')
    #填入buffer里
    buffer.append(['de','\t',tmp[0],'\t',tmp[1],'\t',tmp[2]])
    if(cnt+1)%5==0:
        #print(buffer)
        cur = buffer[0]
        #print(cur)
        id = querys2idx[cur[4]]
        if(id not in ids):continue
        entmp = ['en','\t','2','\t',cur[4],'\t',docs[id],'\n']
        buffer.append(entmp)
        #random采样4个负样本
        for i in range(4):
            id = getRandom()
            entmp = ['en','\t','0','\t',cur[4],'\t',docs[id],'\n']
            buffer.append(entmp)
        for line in buffer:
            out.write(''.join(line))


