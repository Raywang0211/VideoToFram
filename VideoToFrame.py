
import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import os


def digital_resize(input_img,scale_percent):
    '''
    foecr make image to certain size, the ration would change
    '''

    width = int(input_img.shape[1] * scale_percent / 100)
    height = int(input_img.shape[0] * scale_percent / 100)
    output_img = cv2.resize(input_img,(width,height))
    return output_img

def fix_ratial_resize(input_img,target_size):
    '''
    resize method which can keep ration of width and height, using letter-box to make the image fitting certain shape
    '''
    long_side_target = max(target_size)
    long_sid_inputimg = max(input_img.shape)
    ratial = long_side_target/long_sid_inputimg
    new_height = int(input_img.shape[0]*ratial)
    new_width = int(input_img.shape[1]*ratial)


    pad_h = int((target_size[0] - new_height)/2)
    pad_w = int((target_size[1] - new_width)/2)
    input_img = cv2.resize(input_img,(new_width,new_height))
    top, bottom = int(round(pad_h - 0.1)), int(round(pad_h + 0.1))
    left, right = int(round(pad_w - 0.1)), int(round(pad_w + 0.1))
    resize_img = cv2.copyMakeBorder(input_img, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                value=(114, 114, 114))  # add border
    return resize_img


def keystone_adjust(input_img):
    '''
    Kind of sharp method
    input
    input_img: input image [cv2]
    ---
    output
    output_img = output image [cv2]
    adj_time = processing time [ms]
    '''

    target_pt = np.float32([[0,670],[1920,670],[300,390],[1590,390]])
    source_pt = np.float32([[0,1080],[1920,1080],[0,0],[1920,0]])

    t1 = time.time()
    t_matrix = cv2.getPerspectiveTransform(target_pt,source_pt)
    output_img = cv2.warpPerspective(input_img,t_matrix,(input_img.shape[1],input_img.shape[0]),cv2.INTER_CUBIC)
    adj_time = time.time()-t1

    return output_img,adj_time


def crop_video(x1,y1,x2,y2,period,input_path,save_path):
    '''
    extract each frame from video. Each image can resize to certain size with fixed width and height ration.

    '''

    cap = cv2.VideoCapture(input_path)
    total_fram = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    count = 0
    cap_fram = total_fram
    

    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    fram_period = period*frame_rate


    while cap.isOpened():
        if count>=cap_fram:
            cap.release()
            break
        else:
            if not count%fram_period:
                ret,fram = cap.read()
                if not ret:
                    print("Read file fail!!!")
                    break
                fram = fram[y1:y2,x1:x2]
                cv2.imwrite(save_path+str(count)+".jpg",fram)
                count+=1
                print("Count = ",count,"/",cap_fram,end="\r")

            
            else:
                count+=1
                ret,fram = cap.read()
                continue
        
    print("Crop and save finish")



if __name__ == "__main__":

    """
    Using x1,y1,x2,y2 to crop video and save single frame
    input_path: source video
    save_preaddress: Saved image name
    save_path: image saved path
    save_period: decide how often to save single frame

    """

    x1 = 0
    y1 = 0
    x2 = 1920
    y2 = 1080

    input_path = "C:\\Users\sam\\Desktop\\tmp\\taipei\\20240103_10_48_38_电影.mp4"
    save_preaddress = "01_1"
    save_path = "C:\\Users\sam\\Desktop\\tmp\\taipei\\20240103_10_48_38_CROP\\"+save_preaddress
    save_period = 1
    video = crop_video(x1,y1,x2,y2,save_period,input_path,save_path)
