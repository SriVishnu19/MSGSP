import copy

def is_subset(sub, seq):
    if len(list(set(sub))) != len(sub):
          return False

    for i in sub:
        if i not in seq:
            return False

    return True

def is_subsequence(sub, seq):
    explored = []
    next = 0
    for i in sub:
        found = False
        j = next
        while j < len(seq):
            if j in explored:
                pass
            else:
                if is_subset(i, seq[j]):
                    explored.append(j)
                    found = True
                    next = j+1
                    break
            j =j+1
        if not found:
            return False

    return True


def support_count(Ck, data):
    sup = [0] * len(Ck)
    
    for s in range(len(Ck)):
        count = 0
        for d in data:
            if is_subsequence(Ck[s], d):
                count += 1
        sup[s] = count

    return sup

def seqLength(seq):
    length = 0
    l=0
    
    for i in seq:
        for j in i:
            l=l+1

    return l



def removeItem(seq, index):
    seqcopy = copy.deepcopy(seq)
    r=[]
    length = seqLength(seqcopy)
    if index < 0 or index >= length:
        return []

    count = 0
    for itemset in seqcopy:
        if count + len(itemset) <= index:
            count = count+len(itemset)
        else:
            del itemset[index - count]
            break
        
    for itemset in seqcopy:
        if len(itemset)>0:
            r.append(itemset)
    
    return r  

def getItem(seq, index):
    length = seqLength(seq)

    if index < 0 or index >= length:
        return None

    count = 0
    for itemset in seq:
        if count + len(itemset) <= index:
            count += len(itemset)
        else:
            return itemset[index - count]

    return None
