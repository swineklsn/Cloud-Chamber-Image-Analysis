from filter_frames import *
from video_tools import *
from to_from_file import *


def main():
    frames = read_frames_from_video('./data/video_Trim.mp4')
    filtered_frames = filter_frames(frames)

    save_as_video(filtered_frames)
    
    write_to_file('./data/frames.pkl', frames)
    write_to_file('./data/frames_filtered.pkl', filtered_frames)

if __name__ == '__main__':
    main()