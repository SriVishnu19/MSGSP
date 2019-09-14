from collections import defaultdict
import sys
import copy
import logging
from datetime import datetime
from extra import is_subset
from extra import is_subsequence
from extra import support_count
from extra import seqLength
from extra import removeItem
from extra import getItem
from preprocess import loadInput,printOutput

inputData = loadInput()
T=inputData["T"]
MS=inputData["MS"]
SDC=inputData["SDC"]



def MSGSP():
    L=[]
    F1=[]
    M=[]
    SUP=[]
    for k in MS.keys():                                   #appending unique items into M
        M.append(k)
    M.sort(key=lambda item: MS[item])                     #sorting M in asc order of MIS values of each item
    
    for i in M:
        count=0
        for j in T:
            for k in j:
                if i in k:
                    count=count+1
                    break
        SUP.append(count)
        

#To enter the first element in L
    for i in range(0,len(M)):
        a=SUP[i]
        if (a/len(T) >= MS[M[i]]):
            L.append((M[i],SUP[i]))
            break
    
#to enter the remaining elements into L
    for i in range(1,len(M)):
        a=SUP[i]
        b=L[len(L)-1][0]
        p=MS[b]
        if(a/len(T) >= p):
            L.append((M[i],SUP[i]))

        
    for i in L:
        if i[1]/len(T) >= MS[i[0]]:
            F1.append(i)
        
    F = [[[f[0]]] for f in F1 ]
        
    k = 2
    Fk, Ck = F1, []
        
    while(Fk):
        if k == 2:                                                                     #level 2 candidate generation
            Ck = level2Candidate_gen(L)
            
        else:                                                                       #candidate generation for k>2
            Ck = candidate_gen(Fk)
         
        cSUP = support_count(Ck, T)
        
        Fk=[]
        for c in range(len(Ck)):
            if float(cSUP[c])/len(T)>=getMinMIS(Ck[c]):
                a=Ck[c]
                Fk.append(a)
                    
            
        F.extend(Fk)
        k += 1
        
    return F



def getMinMIS(seq):
    minMIS = 1000
    for itemset in seq:
        for item in itemset:
            if MS[item] < minMIS:
                minMIS = MS[item]

    return minMIS

def getStrictlyMinimumMIS(seq):
    minMIS = 1000
    strict = True
    for itemset in seq:
        for item in itemset:
            if MS[item] < minMIS:
                minMIS = MS[item]
                strict = True
            elif minMIS == MS[item]:
                strict = False
    if strict:
        return minMIS
    else:
        return 10000



##############To join two itemsets##################
def Join(s1, s2, c):
    candidates = []
    if c == 1:                          #Joining forward
        if len(s2[-1]) == 1:            #If last item in s2 is seperate then appending at last of s1 
            s1copy = copy.deepcopy(s1)
            s1copy.append(s2[-1])
            candidates.append(s1copy)

            if seqLength(s1) == 2 and len(s1) == 2 and s2[-1][-1] > s1[-1][-1]:
                s1copy1 = copy.deepcopy(s1)
                s1copy1[-1].append(s2[-1][-1])
                candidates.append(s1copy1)

        elif (seqLength(s1) == 2 and len(s1) == 1 and s2[-1][-1] > s1[-1][-1]) or seqLength(s1) > 2:
            s1copy = copy.deepcopy(s1)
            s1copy[-1].append(s2[-1][-1])
            candidates.append(s1copy)
                
    elif c == 2:                        #Joining Reverse order of s1 and s2
        if len(s1[0]) == 1:             #If first item in s1 is seperate then appending at first of s2
            s2copy = copy.deepcopy(s2)
            #print("yt",s2copy)
            s2copy.insert(0, s1[0])
            candidates.append(s2copy)
            #print("hd",s2copy)
            if seqLength(s2) == 2 and len(s2) == 2 and s1[0][0] > s2[0][0]:
                s2copy1 = copy.deepcopy(s2)
                    
                s2copy1[0].insert(0, s1[0][0])
                candidates.append(s2copy1)

        elif (seqLength(s2) == 2 and len(s2) == 1 and s1[0][0] > s2[0][0]) or seqLength(s2) > 2:
            s2copy1 = copy.deepcopy(s2) 
            s2copy1[0].insert(0, s1[0][0])
            candidates.append(s2copy1)
                
    elif c == 3:                        #Joining by APRIORI
        if len(s2[-1]) == 1:            #If last item in s2 is seperate then appending at last of s1
            s1copy = copy.deepcopy(s1)
                
            s1copy.append(s2[-1])
            candidates.append(s1copy)

        else:
            s1copy = copy.deepcopy(s1)
                
            s1copy[-1].append(s2[-1][-1])
                
            candidates.append(s1copy)

    return candidates

def canPrune(seq):
    sLowestMIS = getStrictlyMinimumMIS(seq)
    k = seqLength(seq)

    for i in range(k):
        item = getItem(seq, i)
        
        if MS[item] == sLowestMIS:
            continue

        k_1_subseq = removeItem(seq, i)

        count = 0
        for d in T:
            if is_subsequence(k_1_subseq, d):
                count += 1

        if float(count) / len(T) < getMinMIS(k_1_subseq):
            return True

    return False

def level2Candidate_gen(L):
    C2=[]
    for l in range(len(L)):
        supl = float(L[l][1]) / len(T)
        if supl>=MS[L[1][0]]:
            for h in range(l,len(L)):
                suph=float(L[h][1]) / len(T)
                if suph>=MS[L[1][0]] and abs(supl-suph)<=SDC:

                    C2.append([[L[l][0]], [L[h][0]]])

                    if L[l][0]!=L[h][0]:
                        C2.append([[L[h][0]], [L[l][0]]])

                    if L[l][0]<L[h][0]:
                        C2.append([[L[l][0], L[h][0]]])
                    else:
                        C2.append([[L[h][0], L[l][0]]])
        
    return C2

def candidate_gen(F):
    cs = []
    cgen=[]
    for s1 in F:
        for s2 in F:
            if MS[s1[0][0]] == getStrictlyMinimumMIS(s1):
                s1copy=copy.deepcopy(s1)
                s2copy=copy.deepcopy(s2)
                    
                a=getItem(s1copy,1)
                b=getItem(s2copy,seqLength(s2)-1)

                #To remove 2nd item of S1
                if len(s1copy[0])>1:
                    del s1copy[0][1]
                else:
                    if len(s1copy[1])==1:
                        del s1copy[1]
                    else:
                        del s1copy[1][0]
                        
                #To remove 2nd last item of S2
                if len(s2copy[-1])==1:
                    del s2copy[-1]
                else:
                    del s2copy[-1][-1]
                    
                    
                m=support_count([[[a]]],T)
                n=support_count([[[b]]],T)
                s=abs((m[0]/len(T))-(n[0]/len(T)))

                        
                    
                if (s1copy==s2copy) and (MS[s2[-1][-1]] >= MS[s1[0][0]]) and (s<=SDC) : 
                    
                    nc = Join(s1, s2, 1)
                    for c in nc:
                        cs.append(c)
                            
            elif MS[s2[-1][-1]] == getStrictlyMinimumMIS(s2):
                    
                s1copy=copy.deepcopy(s1)
                s2copy=copy.deepcopy(s2)
                    
                a=getItem(s1copy,0)
                b=getItem(s2copy,seqLength(s2)-2)
                    
                #To remove 1st item of S1
                if len(s1copy[0])==1:
                    del s1copy[0]
                else:
                    del s1copy[0][1]

                #To remove 2nd last item of S2
                if len(s2copy[-1])>1:
                    del s2copy[-1][-2]
                else:
                    if len(s2copy[-2])==1:
                        del s2copy[-2]
                    else:
                        del s2copy[-2][-1]
        
                    
                m=support_count([[[a]]],T)                                
                n=support_count([[[b]]],T)
                s=abs((m[0]/len(T))-(n[0]/len(T)))

                        
                if (s2copy==s1copy) and (MS[s1[0][0]] > MS[s2[-1][-1]]) and (s <=SDC):
                    nc = Join(s1, s2, 2)
                    for c in nc:
                        cs.append(c)
                            
            else:
                s1copy=copy.deepcopy(s1)
                s2copy=copy.deepcopy(s2)
                a=getItem(s1copy,0)
                b=getItem(s2copy,seqLength(s2)-1)

                #To remove 1st item of S1
                if len(s1copy[0])==1:
                    del s1copy[0]
                else:
                    del s1copy[0][1]

                #To remove last item of S2
                if len(s2copy[-1])==1:
                    del s2copy[-1]
                else:
                    del s2copy[-1][-1]

                    
                m=support_count([[[a]]],T)
                n=support_count([[[b]]],T)
                    
                s=abs((m[0]/len(T))-(n[0]/len(T)))
                    
                if s1copy==s2copy and s<=SDC:
                    nc = Join(s1, s2, 3)
                    for c in nc:
                        cs.append(c)

    for c in cs:
        if canPrune(c) is False:
            cgen.append(c)
                
    return cgen


output = MSGSP()

output_dict = defaultdict(list)
for seq in output:
    count = 0
    for d in inputData["T"]:
        if is_subsequence(seq, d):
            count=count+1
    output_dict[seqLength(seq)].append((seq, count))    

printOutput(output_dict)



