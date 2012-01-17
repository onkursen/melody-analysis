# Onkur Sen and Kurt Stallmann

import music
key = music.key
getProgression = music.getProgression

# Determine whether to process manual input or database
manual = raw_input('Enter m to input your own piece. Enter anything else to evaluate database: ')

# If input matches, ask for a piece and find the key.
if manual.strip() == 'm':
    piece = map(int, raw_input(
        "Enter your piece separated by commas (no spaces): ").split(','))
    print "The key of your piece is", key(piece)

else:
    # Construct database of test pieces
    pieces = {
        # 'TwinkleLess': [[48,0.25], [48,0.25], [55,0.25], [55,0.25], [57,0.25], [57,0.25], [55,0.25], [55,0.25]],
        # 'TwinkleMore': [[48,0.25], [48,0.25], [55,0.25], [55,0.25], [57,0.25], [57,0.25], [55,0.25], [55,0.25], [53,0.25], [53,0.25], [52,0.25], [52,0.25], [50,0.25], [50,0.25], [48,0.25], [48,0.25]],
        # 'K545-1-8ths': [0,0,0,0,4,4,7,7,-1,-1,-1,2,0,0,0,0],
        # 'K545-1-16ths': [0,0,0,0,0,0,0,0,4,4,4,4,7,7,7,7,-1,-1,-1,-1,-1,-1,0,2,0,0,0,0,0,0,0,0],
        # 'HotCrossBuns': [4,4,2,2,0,0,0,0,4,4,2,2,0,0,0,0],
        # 'ChopinPrelude-Em': [11, 11, 11, 11, 11, 11, 12, 12],
        # 'K545-2nd-Mvt': [11, 11, 11, 11, 11, 11, 11, 11, 14, 12, 11, 12, 14, 14, 14, 11, 7, 7, 7, 7, 7, 7, 7, 7],
        # 'K545-2nd-Mvt2': [11, 11, 11, 11, 11, 11, 11, 11, 14, 12, 11, 12, 14, 14, 14, 11, 7, 7, 7, 7, 7, 7, 7, 7,7,7,7,7,7,7,9,7,6,4,2,1,2,2,2,11,7,7,7,7,7,7,7,7,0,0,0,9,6,6,9,9,11,11,0,0,2,2,2,11,7,7,7,7,7,7,7,7]#,9,7,6,7,6,4,3,4,2,0,-1,0,11,11,11,0,9,9,2,2,1,1,0,0,11,11,11,11,11,11,11,7,11,2,0,9,0,4]
        # 'Invention': [0,2,4,5,2,4,0,7,7,0,0,-1,-1,0,0,2,2],
        # 'Berlioz': [1,1,1,1,1,1,1,3,5,5,5,5,5,5,5,7,8,8,8,8,8,8,8,8,3,3,3,1,8,8],
        # 'Minuet': [2,2,7,9,11,0,2,2,7,7,7,7,4,4,0,2,4,6,7,7,7,7,7,7]
        # 'Minuet in Gm': [10,10,9,9,7,7,2,2,2,2,3,3,7,9,10,0,2,2]
        # 'sym40': [0,-1,-1,-1,0,-1,-1,-1,0,-1,-1,-1,7,7,7,7,7,6,4,4,4,2,0,0,0,-1,9,9,9,9]
        # 'pathetique': [5,5,5,5,3,3,3,3,8,8,8,8,8,8,6,6,5,5,8,8,1,1,3,3,8,8,8,8,8,8]
        # 'fminor-sonata': [0,0,5,5,8,8,0,0,5,5,8,8,8,7,5,5,5,5]
        'schumann': [10,10,10,10,10,10,8,8,11,11,11,11,11,11,10,10,6,6,6,6,6,6,8,8,10,10,10,10,10,10]
        # 'schumann2':[6,10,6,10,5,8,8,11,8,11,6,10,3,6,3,6,5,8,6,10,6,10,6,10]
        # 'social': [6,6,6,4,7,7,7,7,4,4,4,2,2,2,2,2]
        # 'invention-2': [0,11,0,2,3,7,8,10,8,5,5,3,2,0,11,8,7,5,3,2,0,11,0,2,0,2,3,2,3,2,3]
    }

    if manual in pieces:
        print 'The key of', manual, 'is', key(pieces[manual], music.scales.values())
    else:
        # Print keys of all pieces
        for piece in sorted(pieces):
            # NOTE: we have given scales.values() as the argument because
            # we have no prior knowledge to limit our possible key set
            musicKey = key(pieces[piece], music.scales.values())
            print 'The key of', piece, 'is', musicKey
            print getProgression(pieces[piece], musicKey, 4)