import cv2
import numpy as np
import matplotlib.pyplot as plt
import keyboard

def read_frames_from_video(video_path,to_grayscale=True):
    """
    opens the .mp4 file at video_path and returns a list with all (gray-scale) frames as 2D numpy arrays
    """
    # Open the video
    video = cv2.VideoCapture(video_path)
    frames = []

    # Check if the video is actually opened
    if video.isOpened() == False:
        print('Error opening .mp4 file')
    
    while video.isOpened():
        # Read a new frame while the video is opened
        ret,frame = video.read()
        if len(frames)%10==0: print(f"{len(frames)} frames read")
        
        # If there is a new frame available, save it to frames, otherwise, close the programm
        if ret:
            if to_grayscale:
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            frames.append(frame)
        else:
            break
    return frames

def save_as_video(frames,video_name):
    """
    save the frames as a .mp4 file at video_name location
    """
    frames = np.array(frames)
    no_frames,height,width = frames.shape
    fps = 30
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name,fourcc, float(fps), (width,height), 0)
    
    for frame in frames:
        m = np.amax(frame)
        frame = frame/m*255
        video.write(frame.astype(np.uint8))
    video.release()

def show_as_video(frames,secondary_frames='no secondary frames',fps=30):
    """
    Show frames as a video using matplotlib.
    Two sets of frames can be shown side-by-side by providing a second set of frames (secondary_frames).
    The playing of the video can be interrupted by pressing escape.
    """
    if secondary_frames == 'no secondary frames':
        fig,ax = plt.subplots()
        for frame in frames:
            ax.cla()
            ax.imshow(frame)
            plt.draw()
            plt.pause(1/fps)
            if keyboard.is_pressed('esc'): break
    else:
        fig,axes = plt.subplots(1,2)
        for frame1,frame2 in zip(frames,secondary_frames):
            for ax in axes: ax.cla()
            axes[0].imshow(frame1)
            axes[1].imshow(frame2)
            plt.draw()
            plt.pause(1/fps)
            if keyboard.is_pressed('esc'): break