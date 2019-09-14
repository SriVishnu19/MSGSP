### The preprocess.py, MSGSP.py, extra.py and input files must be placed in the same directory while executing

import re

output_file = "C:\\Users\\SRI VISHNU\\Desktop\\Masters\\2nd sem\\DMTM\\MS-GSP\\project\\output_file.txt"

Data = []
Para = {}
SDC = 0
m = open("para1-1.txt","r")    #change the input file name here, in case a different file is bri         
text=m.read()
m1=text.split("\n")
n=open("data-1.txt","r")
text=n.read()
n1=text.split("\n")
def loadInput():
    row=[]
    row_data=[]
    row_data1=[]
    processed={}
    for line in n1:
        line = line.strip()[1:-1]
        
        for s in re.split(r'}{',line[1:-1]):
            for i in re.split(',| ',s):
                if i!='':
                    row.append(int(i))
                        
                
            row_data.append(row)
            row=[]
        Data.append(row_data)
        row_data=[]
        
                         
    for i in range(0,len(m1)):
        a=m1[i].split("=")
        j=a[0].strip()
        k=j[j.find("(")+1:j.find(")")]
        if k != "SD":
            Para[int(k)]= float(a[1].strip())
        else:
            Para[k]= float(a[1].strip())

    
    SDC=float(Para['SD'])
    del Para['SD']

    processed["T"]=Data
    processed["MS"]=Para
    processed["SDC"]=SDC
    return processed
    
def printOutput(data):
    if not data:
        print ("None")
        return

    with open(output_file, 'w') as outFile:
        for i in range(max(data.keys())):
            print ("No of length", i+1, "patterns:", len(data[i+1]))
            outFile.write("No of length " + str(i+1) + "patterns:" + str(len(data[i+1])) + "\n")

            for j in data[i+1]:
                seqi = []
                for k in j[0]:
                    #print("rtgr",k)
                    '''for l in k:
                        seqi.append("{" + ", ".join(l)+"}")'''
                    seqi.append("{" + ", ".join([str(l) for l in k]) + "}")

                seq = "<" + ", ".join(seqi) + ">"

                print ("pattern:", seq, " count:", j[1])
                outFile.write("pattern: " + seq + " count: " + str(j[1]) + "\n")
            print ("")
            outFile.write("\n")

