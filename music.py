# Onkur Sen and Kurt Stallmann
# Last edited: 2/22/2012

import copy

# Settings for decimal usage
from decimal import *
getcontext().prec = 8
getcontext().rounding = ROUND_HALF_EVEN

# Constants; use decimals for precision
one = Decimal('1')
two_thirds = Decimal('2') / Decimal('3')
one_half = Decimal('1') / Decimal('2')
one_third = Decimal('1') / Decimal('3')
zero = Decimal('0')

# Shifts the note to the base chromatic scale
def mod(note):
    return note % 12

# Returns sorted, modded chord
# NOTE: Must use tuples for hashing purposes
def modded(chord): 
    return tuple(sorted([mod(note) for note in chord]))

# Chord database; major and minor chords only
chords = {}
chords.update({modded([i, i+4, i+7]): (i, 'major') for i in range(12)})
chords.update({modded([i, i+3, i+7]): (i, 'minor') for i in range(12)})

# Scale database; major and harmonic minor scales only
scales = {}
scales.update({modded([i,i+2,i+4,i+5,i+7,i+9,i+11]): (i, 'major') 
    for i in range(12)})
scales.update({modded([i,i+2,i+3,i+5,i+7,i+8,i+10,i+11]): (i, 'minor') 
    for i in range(12)})

# Reverse lookup in a dictionary: given value, finds key
def lookup(item, database):
    keys = [key for key, value in database.iteritems() if item == value]
    return keys[0] if len(keys) == 1 else keys

# Reverse lookup for maximum value
def lookupMax(database):
    return lookup(max(database.values()), database)

# Returns a tuple of:
# 1. occurrence of notes in the chromatic scale for a given piece
# 2. normalized weights of notes based on frequency of occurrence. 
def count_notes(piece):
    # Count occurrences of notes
    noteCount = [0] * 12
    for x in piece:
        target = x if type(x) is int else x[0]
        noteCount[target % 12] += 1
        
    # Use Decimal to avoid floating-point error
    weights = [Decimal(str(w)) / Decimal(str(len(piece))) 
        for w in noteCount]
        
    return noteCount, weights

# Consonance relation between a key and a pitch in accordance
# with music theory. Note that this relation is NOT SYMMETRIC,
# e.g. a 5th above is not the same as a 4th below
def consonance_with_key(musicKey, pitch):
    diff = (pitch - musicKey[0]) % 12
    if diff == 0: # 1st
        return one
    if diff == 7: # 5th
        return two_thirds
    if diff == 5: # 4th
        return one_third
        
    # Major key with minor interval should have no consonance, and vice versa
    if (musicKey[1] == 'major' and diff in [4,9]) or \
    (musicKey[1] == 'minor' and diff in [3,8]):
        return one_third
    
    return zero

# Correlation function of keys in possible key set using weighted consonance
def consonance_correlations(possibleKeySet, weights):
    return {musicKey: sum([weights[note] * consonance_with_key(musicKey, note) 
        for note in range(12)])
        for musicKey in possibleKeySet}
    
# Binary operation indicating whether a note is in a scale or not   
def membership(note, scale):
    return one if note in scale else zero

# Correlation function of keys in possible key set using weighted membership
def membership_correlations(possibleKeySet, weights):
    return {musicKey: sum([weights[note] * membership(note, lookup(musicKey, scales))
        for note in range(12)]) 
        for musicKey in possibleKeySet}

def resolve(musicKey, last_note):
    diff = mod(last_note - musicKey[0])
    if last_note == musicKey[0]:
        return one
    if (musicKey[1] == 'major' and diff == 4) or (musicKey[1] == 'minor' and diff == 3):
        return two_thirds
    if diff == 7:
        return one_half
    return zero

def resolve_correlations(piece, possibleKeySet):
    last_note = piece[-1]
    return {musicKey: resolve(musicKey, last_note) for musicKey in possibleKeySet}

# Determines the key of a piece
def key(piece, possibleKeySet):
    # Get note counts and normalized weights
    noteCount, weights = count_notes(piece)
    
    # Get consonance and membership correlations for each key
    c_correlations = consonance_correlations(possibleKeySet, weights)
    m_correlations = membership_correlations(possibleKeySet, weights)
    r_correlations = resolve_correlations(piece, possibleKeySet)

    # Return the key with the highest consonance correlation that also 
    # has a perfect membership correlation.
    # Perfect defined as >= 0.9999 due to floating point error;
    # PROBLEM: too high of a threshold? need to explore
    perfect_matches = {musicKey: c_correlations[musicKey]
        for musicKey in m_correlations 
        if m_correlations[musicKey] >= Decimal('0.9')}
    # for k,v in perfect_matches.iteritems():
    #     print k,v
    return lookupMax(perfect_matches)

# Returns opposite mode
def complement(mode):
    return 'minor' if mode == 'major' else 'major'

# Returns chord progression for piece, with one chord per every "interval" notes
def getProgression(piece, musicKey, interval):
    tonic, mode = musicKey
    
    # Assume possible key set only contains, I, IV, V, and relative major/minor
    possibleKeySet = set([musicKey, (mod(tonic+5), mode), (mod(tonic+7), mode)])
    if mode == 'major': # add relative minor
        possibleKeySet.add((mod(tonic-3), complement(mode)))
    else: # add relative major
        possibleKeySet.add((mod(tonic+3), complement(mode)))
    # Splits piece up into groups of "interval" notes
    groups = [piece[i*interval:(i+1)*interval] for i in range(len(piece)/interval)]
    
    harmony = [key(group, possibleKeySet) for group in groups]
    returns = []
    curr = 0
    i = 1
    while i < len(harmony):
        if harmony[i] == musicKey:
            while i+1 < len(harmony) and harmony[i+1] == musicKey:
                i += 1
            returns.append(i-curr+1)
            curr = i+1
        i += 1
    print 'returns', returns
    return harmony