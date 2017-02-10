# Generate images showing the pentomino tilings.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

designs = pd.read_csv('matrix.csv', index_col=0)
solutions = pd.read_csv('exact-covers-sorted.csv',header=None)

for seq in range(len(solutions)):
    print (seq)
    row = solutions.iloc[seq]
    v = np.zeros(60, dtype='int')
    for i, n in enumerate(row):
        v += (i+1) * designs.iloc[n] [:60]
    m = np.zeros(64, dtype='int')
    m[1:7] = v[:6]
    m[8:56] = v[6:54]
    m[57:63] = v[54:]
    arr = m.reshape((8,8))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    imgplot = ax.imshow(arr, interpolation='nearest')
    imgplot.set_cmap('Paired')
    plt.axis('off')
    fig.savefig('tilings/pent%04d.png' % seq, bbox_inches='tight')
    fig.clf()
    plt.close()


# To create an animated gif:
#  $ convert -delay 25 tilings/*.png pentomino.gif  

# To create an MP4 video:
#  $ ffmpeg -r 60 -f image2 -s 1920x1080 -i pic%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4
# Maybe this? ffmpeg -i pent%04d.png pentomino.mp4

  #  0  1  1  5  5  9  9  0
  #  1  1  5  5  5  3  9  9 
  # 11  1  3  3  3  3  4  9 
  # 11  2  2  2  2  2  4  4 
  # 11 11  8  8  8 12 12  4
  # 11 10  7  7  8  6 12  4
  # 10 10 10  7  8  6 12 12 
  #  0 10  7  7  6  6  6  0
