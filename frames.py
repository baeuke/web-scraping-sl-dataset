'''
A script that saves a range of frames in the videos for dataset.
We are not taking the starting and ending frames as 'signing' mainly  happens in the middle of a video.
'''

import cv2
import os

input_dir = 'videos/'
output_dir = 'frames-45/'

# percentage of frames to remove from each end
remove_frames_percent = 0.45

# output directories for each palm orientation class
for i in range(8):
    os.makedirs(os.path.join(output_dir, str(i)), exist_ok=True)

# looping through all the videos in the input directory
for video_file in os.listdir(input_dir):
    if not video_file.endswith('.mp4'):
        continue

    # palm orientation class from the video filename
    palm_orientation_class = int(video_file.split('_')[-1].split('.')[0])

    video_path = os.path.join(input_dir, video_file)
    cap = cv2.VideoCapture(video_path)

    # getting the total number of frames in the video
    # and calculating the number of frames to skip from the beginning and end
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    skip_frames = int(total_frames * remove_frames_percent)
    start_frame = skip_frames # start of the range
    end_frame = total_frames - skip_frames # end of the range


    frame_num = 0
    while True:
        # reading a frame from the video
        ret, frame = cap.read()

        # if no more frames, break
        if not ret:
            break

        # if not in the range, skip the frame
        if frame_num < start_frame or frame_num >= end_frame:
            frame_num += 1
            continue

        # saving the frame as an image
        output_filename = f'frame_{video_file.split("_")[1]}_{frame_num}.jpg'
        output_path = os.path.join(output_dir, str(palm_orientation_class), output_filename)
        cv2.imwrite(output_path, frame)

        frame_num += 1


    cap.release()
