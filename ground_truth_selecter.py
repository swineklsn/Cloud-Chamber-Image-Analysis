import cv2
import numpy as np
import keyboard
import pickle
import matplotlib.pyplot as plt

# the path to the pickle file containing the frames to analyse:
video_path = './data/video_Trim.mp4'

# the path to the pickle file containing the filtered frames to put in the ground-truth:
filtered_frames_path = './data/frames_filtered.pkl'

# the path at which the ground-truths have to be saved:
ground_truth_path = './data/ground-truths.pkl'


def merge(matrixA,matrixB):
    # merge matrixA and matrixB into a single matrix with the A and B values as tuples
    result = []
    for rowA,rowB in zip(matrixA,matrixB):
        result.append([*tuple(zip(rowA,rowB))])
    return result


def plot_line(img,points,thickness,color):
    for i in range(len(points)-1):
        cv2.line(img,points[i],points[i+1],color,thickness)


def update(event,x,y,flags,param):
    global lines, new_line, new_thickness, image, drawn_image, filtered_image
    if event == cv2.EVENT_LBUTTONDOWN:
        new_line.append([x,y])
    elif event == cv2.EVENT_RBUTTONDOWN:
        lines.append(new_line)
        thicknesses.append(new_thickness)
        new_line = []
        new_thickness = 1
    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            new_thickness = max(1,new_thickness-1)
        if flags < 0:
            new_thickness += 1
    elif event == cv2.EVENT_MBUTTONDOWN:
        if len(new_line) > 1:
            new_line.pop(len(new_line)-1)
        elif len(new_line) == 1:
            new_line = []
            new_thickness = 1
        else:
            if len(lines)>0:
                lines.pop(len(lines)-1)
    drawn_image = image.copy()
    for thickness,line in zip(thicknesses,lines):
        plot_line(drawn_image,line,thickness,(0,255,0))
    if len(new_line) > 0:
        temp_line = new_line.copy()
        temp_line.append([x,y])
        plot_line(drawn_image,temp_line,new_thickness,(0,0,255))
    cv2.imshow('window',drawn_image)


from video_tools import *
from to_from_file import *

images = read_frames_from_video(video_path)
filtered_images = read_from_file(filtered_frames_path)
ground_truths = []
current_image_number = 0
all_lines = []
all_thicknesses = []

for image,filtered_image in zip(images,filtered_images):
    current_image_number+=1
    print(f"You are at frame {current_image_number} of {len(images)}")

    image = cv2.cvtColor(filtered_image,cv2.COLOR_GRAY2RGB)
    if np.amax(image) != 0:
        image = image/np.amax(image)*255
    # open the new image and reset the shapes
    drawn_image = image.copy()
    lines = []
    thicknesses = []
    new_line = []
    new_thickness = 1

    # initialise the window to draw the shapes
    cv2.namedWindow('window')
    cv2.setMouseCallback('window',update)
    cv2.imshow('window',drawn_image)

    # wait for keypress to continue
    key = cv2.waitKey()
    
    # is escape was pressed, close the program
    if key == 27:
        print("Clsoing the program...")
        cv2.destroyAllWindows()
        break
    
    # close the current window
    cv2.destroyAllWindows()

    # create a mask from the shapes, merge it with the frame to create the ground-truth
    mask = np.zeros((image.shape[0],image.shape[1]),dtype=np.uint8)
    for line,thickness in zip(lines,thicknesses):
        plot_line(mask,line,thickness,255)
    #cv2.imshow('window2',mask)

    # wait for keypress to continue
    #key = cv2.waitKey()
    
    # is escape was pressed, close the program
    if key == 27:
        print("Clsoing the program...")
        cv2.destroyAllWindows()
        break
    
    # close the current window
    #cv2.destroyAllWindows()
    
    mask = np.asarray(mask,dtype='uint8')
    ground_truth = merge(filtered_image.tolist(),mask.tolist())
    ground_truths.append(ground_truth)
    all_lines.append([lines])
    all_thicknesses.append([thicknesses])
    
    # if escape was pressed, close the program
    if key == 27:
        print("Clsoing the program...")
        break

write_to_file('./data/ground_truths.pkl', ground_truths)