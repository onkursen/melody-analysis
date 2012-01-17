import random, copy

def modded(chord):
    return sorted([note % 12 for note in chord])

def isSubset(sub, sup):
    return set(sub).isSubset(set(sup))

# Chord database; major and minor chords only
chords = {i:[modded([i, i+4, i+7]),modded([i, i+3, i+7])] for i in range(12)}

# Scale database; major and harmonic minor scales only
scales = {i:[modded([i,i+2,i+4,i+5,i+7,i+9,i+11]), modded([i,i+2,i+3,i+5,i+7,i+8,i+11])] for i in range(12)}

def scaleType(scale):
    third = scale[2]-scale[0]
    if third == 4: return 'major'
    elif third == 3: return 'minor'
    return '?'

# Looks at note occurrences of a piece and assumed key and determines if major or minor by comparing thirds
def MajMin(count, j):
    Maj = (j+4)%12; Min = (j+3)%12;
    if count[Maj] > count[Min]: return j, 'major'
    elif count[Maj] < count[Min]: return j, 'minor'
    return j, '?'
        
def key(piece):    
    # Count occurrences of notes
    count = [0]*12
    for x in piece:
        if type(x) is int: count[x%12]+=1
        else: count[x[0]%12] += 1
        
    # Create triad of three most frequently occurring notes
    triad = []; d = copy.copy(count)
    for j in range(3):
        loc = d.index(max(d))
        triad.append(loc)
        d[loc] = -1
        
    # If this triad is in our chord database, we've found the key    
    for j in range(12):
        if sorted(triad) in chords[j]: return MajMin(count, j)
    
    # Otherwise, look at top two notes, and see if they are contained in an existing chord.
    # If they are, we've found the key.
    dyad = triad[0:2]
    for j in range(12):
        for i in range(len(chords[j])):
            if isSubset(dyad, chords[j][i]):
                return MajMin(count, j)
                
    # SPECIAL CASE: If V and vi found most often, then we know that i is the most likely key
    # since it contains the tonics of all considerable chords.
    if (dyad[1]-dyad[0])%12 == 1:
        return (dyad[0]-7)%12, 'minor'
    
    # Otherwise, choose the most frequently occurring note as the key
    # print 'assumed tonic', triad[0]
    # for i in range(len(piece)):
    #     if piece[i] == triad[0] and i < len(piece)-1:
    #         print 'found; before: {}, after: {}'.format(piece[i-1], piece[i+1])
    # return MajMin(count, triad[0])
    
    possible = []
    for tonic in range(12):
        for scale in range(tonic):
            if isSubset(dyad, scale):
                possible.append(tonic,scaleType(scale))
    
 

# twinkle = [[48,0.25], [48,0.25], [55,0.25], [55,0.25], [57,0.25], [57,0.25], [55,0.25], [55,0.25]]
# print 'twinkle1',key(twinkle)
# 
# twinkle = [[48,0.25], [48,0.25], [55,0.25], [55,0.25], [57,0.25], [57,0.25], [55,0.25], [55,0.25], [53,0.25], [53,0.25], [52,0.25], [52,0.25], [50,0.25], [50,0.25], [48,0.25], [48,0.25]]
# print 'twinkle2',key(twinkle)
# 
# k545 = [0,0,0,0,4,4,7,7,-1,-1,-1,2,0,0,0,0]
# print 'k545',key(k545)
# 
# hot = [4,4,2,2,0,0,0,0,4,4,2,2,0,0,0,0]
# print 'hot',key(hot)
# 
# test = [0,4,7,4,0]
# print 'test',key(test)
# 
# chopin = [-1, -1, 11, 11, 11, 11, 11, 11, 12, 12, 11, 11, 11, 11]
# print 'chopin', key(chopin)
# 
# k545_2 = [11, 11, 11, 11, 11, 11, 11, 11, 14, 12, 11, 12, 14, 14, 14, 11, 7, 7, 7, 7]
# print 'k545_2', key(k545_2)