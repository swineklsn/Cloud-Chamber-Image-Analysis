import numpy as np
from skimage.filters import difference_of_gaussians

def filter_frames(frames, threshold1 = 1, min_frequency = 2, max_frequency = 4, threshold2 = 15):
    filtered_frames = []

    # Calculate the average frame of the video
    avg_frame = np.average(frames,axis=0)
    frame_nr = 0
    for frame in frames:
        frame_nr+=1

        print(f'Filtering frame {len(filtered_frames)+1} of {len(frames)}')

        # Calculate the average of the last 10 frames
        try:
            avg_frame = np.average(frames[frame_nr-10:frame_nr],axis=0)
        except:
            avg_frame = np.average(frames,axis=0)
        
        # Subtract the average frame from the current frame
        filtered_frame = frame - avg_frame

        # Apply a threshold
        filtered_frame[filtered_frame < filtered_frame.mean()*threshold1] = 0

        # Apply a band-pass filter
        filtered_frame = difference_of_gaussians(filtered_frame, min_frequency, max_frequency)
        
        # Apply a threshold
        filtered_frame[filtered_frame < filtered_frame.mean()*threshold2] = 0
        
        # Append the filtered frames to the list
        filtered_frames.append(filtered_frame.astype('uint8'))
    return filtered_frames