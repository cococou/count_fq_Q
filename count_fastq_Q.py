#!/usr/bin/python3
#coding: utf-8

# ************************************************************
# file: ./count_fastq_Q.py PATH SAMPLEID
#
# ************************************************************
# In[19]:

import sys,os,re

def xopen(file):
    with open(file,'r') as handle:
        for line in handle:
            yield(line.rstrip())


# In[70]:

def find_as(line,i):
    if i % 4 == 0:
        return(line)
    else:
        pass


# In[71]:

def dic_as(asc,asc_dic):
    line_q=map(ord,asc)
    for one_q in line_q:
        if one_q not in asc_dic.keys():
            asc_dic.update({one_q:1})
        else:
            asc_dic[one_q] += 1
    return(asc_dic)


# In[72]:

def main(file):
    i = 0
    asc_dic={}
    for line in xopen(file):
        i += 1
        asc=find_as(line,i)
        if asc!=None:
            dic_as(asc,asc_dic)
    return(asc_dic)


# In[20]:

import sys,os,re


# In[21]:

def get_file(SAMPLEID,PATH):
    files = []
    DIR = os.listdir(os.path.join(PATH,SAMPLEID))
    imreg = re.compile('S.*160000.*fastq')
    for file in DIR:
        if re.findall(imreg,file):
            file = os.path.join(PATH,SAMPLEID,file)
            files.append(file)
    return(files)


# In[22]:

def mkdir_qc(SAMPLEID):
    full_path = os.path.join('/home/public/qcer/qc.raw',SAMPLEID)
    if not os.path.exists(full_path):
        print(full_path+' does not exist,because ',SAMPLEID,' pipline is not runned')
        exit()
    qc_file = os.path.join(full_path,"qc")
    if not os.path.exists(qc_file):
        os.mkdir(qc_file)
  

# In[81]:

def Q_percent(file_q,Q_th):
    Q_sum = sum(file_q.values())
    Q_th_value = 0
    for Q_one in file_q.keys():
        #print(Q_one)
        if Q_one-33 >=  Q_th:
            Q_th_value += file_q[Q_one]
    Q_per = (Q_th_value/Q_sum) * 100
    return(Q_per)

def main_plus(SAMPLEID,PATH):
    files = get_file(SAMPLEID,PATH)
    mkdir_qc(SAMPLEID)
    for file in files:
        file_basename = os.path.basename(file)
        file_th = os.path.join('/home/public/qcer/qc.raw',SAMPLEID,"qc",file_basename+".Q")
        #print(file_th)
        with open(file_th,"w") as handle:
            file_q = main(os.path.join(PATH,SAMPLEID,file))
            print('Q20','%.4f'%Q_percent(file_q,20),file=handle)
            print('Q30','%.4f'%Q_percent(file_q,30),file=handle)
            print(file_q,file=handle)

if __name__ == "__main__":
    SAMPLEID = sys.argv[2]
    PATH = sys.argv[1]
    main_plus(SAMPLEID,PATH)
