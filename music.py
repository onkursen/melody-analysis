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

NUM_NOTES_IN_SCALE = 12

# Shifts the note to the base chromatic scale
def mod(note):
  return note % NUM_NOTES_IN_SCALE

# Returns sorted, modded chord
# NOTE: Must use tuples for hashing purposes
def modded(chord):
  return tuple(sorted(mod(note) for note in chord))

# Chord database; major and minor chords only
chords = {}
chords.update({modded([i, i+4, i+7]): (i, 'Major') for i in xrange(NUM_NOTES_IN_SCALE)})
chords.update({modded([i, i+3, i+7]): (i, 'minor') for i in xrange(NUM_NOTES_IN_SCALE)})

# Scale database; major and harmonic minor scales only
scales = {}
scales.update({
  modded([i,i+2,i+4,i+5,i+7,i+9,i+11]): (i, 'Major')
  for i in xrange(NUM_NOTES_IN_SCALE)
})
scales.update({
  modded([i,i+2,i+3,i+5,i+7,i+8,i+10,i+11]): (i, 'minor')
  for i in xrange(NUM_NOTES_IN_SCALE)
})

# Reverse lookup in a dictionary: given value, finds key
def lookup(item, dictionary):
  keys = [key for key, value in dictionary.iteritems() if item == value]
  return keys[0] if len(keys) == 1 else keys

# Returns a tuple of:
# 1. occurrence of notes in the chromatic scale for a given piece
# 2. normalized weights of notes based on frequency of occurrence.
def count_notes(piece):
  # Count occurrences of notes
  note_counts = [0] * NUM_NOTES_IN_SCALE
  for x in piece:
    target = x if type(x) is int else x[0]
    note_counts[mod(target)] += 1

  # Use Decimal to avoid floating-point error
  weights = [
    Decimal(w) / len(piece)
    for w in note_counts
  ]

  return note_counts, weights

# Consonance relation between a key and a pitch in accordance
# with music theory. Note that this relation is NOT SYMMETRIC,
# e.g. a 5th above is not the same as a 4th below
def consonance_with_key(music_key, pitch):
  tonic, mode = music_key

  num_steps_apart = mod(pitch - tonic)
  if num_steps_apart == 0: return one # 1st
  if num_steps_apart == 7: return two_thirds # 5th
  if num_steps_apart == 5: return one_third # 4th

  # Major key with minor interval should have no consonance, and vice versa
  if (mode == 'Major' and num_steps_apart in [4,9]) or \
     (mode == 'minor' and num_steps_apart in [3,8]):
    return one_third

  return zero

# Correlation function of keys in possible key set using weighted consonance
def consonance_correlations(possible_keys, weights):
  return {
    music_key: sum(
      weights[note] * consonance_with_key(music_key, note)
      for note in xrange(12)
    )
    for music_key in scales.values()
  }

# Binary operation indicating whether a note is in a scale or not
def membership(note, scale):
  return one if note in scale else zero

# Correlation function of keys in possible key set using weighted membership
def membership_correlations(possible_keys, weights):
  return {
    music_key: sum(
      weights[note] * membership(note, lookup(music_key, scales))
      for note in xrange(12)
    )
    for music_key in possible_keys
  }

def resolve(music_key, last_note):
  num_steps_apart = mod(last_note - music_key[0])
  if num_steps_apart == 0: return one
  if num_steps_apart == 7: return one_half
  if (music_key[1] == 'Major' and num_steps_apart == 4) or \
     (music_key[1] == 'minor' and num_steps_apart == 3):
    return two_thirds
  return zero

def resolve_correlations(piece, possible_keys):
  last_note = piece[-1]
  return {
    music_key: resolve(music_key, last_note)
    for music_key in possible_keys
  }

# Determines the key of a piece
# NOTE: we have given scales.values() as the default argument if
# we have no prior knowledge to limit our possible key set
def key(piece, possible_keys=scales.values()):
  # Get note counts and normalized weights
  note_counts, weights = count_notes(piece)

  # Get consonance and membership correlations for each key
  c_correlations = consonance_correlations(possible_keys, weights)
  m_correlations = membership_correlations(possible_keys, weights)
  r_correlations = resolve_correlations(piece, possible_keys)

  # Return the key with the highest consonance correlation that also
  # has a perfect membership correlation.
  # Perfect defined as >= 0.9 due to floating point error
  perfect_matches = {
    music_key: c_correlations[music_key]
    for music_key in m_correlations
    if m_correlations[music_key] >= Decimal('0.9')
  }
  return lookup(max(perfect_matches.values()), perfect_matches)

# Returns opposite mode
def complement(mode):
  if mode == 'Major': return 'minor'
  return 'Major'

# Returns chord progression for piece, with one chord per every "interval" notes
def get_progression(piece, music_key, interval):
  tonic, mode = music_key

  # Assume possible key set only contains, I, IV, V, and relative major/minor
  possible_keys = set([music_key, (mod(tonic+5), mode), (mod(tonic+7), mode)])
  if mode == 'Major': # add relative minor
    possible_keys.add((mod(tonic-3), complement(mode)))
  else: # add relative major
    possible_keys.add((mod(tonic+3), complement(mode)))
  # Splits piece up into groups of "interval" notes
  groups = [piece[i*interval:(i+1)*interval] for i in xrange(len(piece)/interval)]

  harmony = [key(group, possible_keys) for group in groups]
  returns = []
  curr = 0
  i = 1
  while i < len(harmony):
    if harmony[i] == music_key:
      while i+1 < len(harmony) and harmony[i+1] == music_key:
        i += 1
      returns.append(i-curr+1)
      curr = i+1
    i += 1
  return harmony

def get_key_string(k):
  tonic, mode = k
  notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "B"]
  return notes[tonic] + " " + mode
