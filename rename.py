'''
! Not relevant anymore: the main.py now names in the correct format when downloading the videos.

File for renaming the videos to include palm orientation class (for easier distribution of the frame images into class directories).
'''

import os

with open('annotations.txt', 'r') as f:
    for line in f:
        if line.startswith('Page'):
            page_number = int(line.split()[1][:-1]) # page number
        elif line.startswith('Palm orientation class'):
            palm_orientation_class = line.split()[-1] # palm orientation class

            if palm_orientation_class == 'None':
                continue

            # rename the video file
            old_name = f'videos/video_{page_number}.mp4'
            new_name = f'videos/video_{page_number}_{palm_orientation_class}.mp4'
            os.rename(old_name, new_name)
