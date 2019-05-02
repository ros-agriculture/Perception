import os
import argparse
import json
import cv2
from utils.utils import get_yolo_boxes, makedirs
from utils.bbox import draw_boxes
from keras.models import load_model
from tqdm import tqdm
import numpy as np

class Model():

    def __init__(self,config_path = 'config.json'):
        # Empty json file
        #
        with open(config_path) as config_buffer:    
            self.config = json.load(config_buffer)

        ###############################
        #   Set Model parameters
        ###############################       
        self.net_h, self.net_w = 416, 416 # a multiple of 32, the smaller the faster
        self.obj_thresh, self.nms_thresh = 0.5, 0.45

        ###############################
        #   Load the model
        ###############################
        os.environ['CUDA_VISIBLE_DEVICES'] = self.config['train']['gpus']
        self.infer_model = load_model(self.config['train']['saved_weights_name'])
        print("Model Inferred...")
        #print(infer_model.)
        

    def predict(self,input_path, output_path):

        config = self.config
        infer_model = self.infer_model
        net_h = self.net_h
        net_w = self.net_w
        obj_thresh  = self.obj_thresh, 
        nms_thresh = self.nms_thresh
        print("Net h: ", net_h)
        ###############################
        #   Predict bounding boxes 
        ###############################
        if 'webcam' in input_path: # do detection on the first webcam
            video_reader = cv2.VideoCapture(0)

            # the main loop
            batch_size  = 1
            images      = []
            while True:
                ret_val, image = video_reader.read()
                if ret_val == True: images += [image]

                if (len(images)==batch_size) or (ret_val==False and len(images)>0):
                    batch_boxes = get_yolo_boxes(self.infer_model, images, net_h, net_w, config['model']['anchors'], obj_thresh, nms_thresh)

                    for i in range(len(images)):
                        draw_boxes(images[i], batch_boxes[i], config['model']['labels'], obj_thresh) 
                        cv2.imshow('video with bboxes', images[i])
                    images = []
                if cv2.waitKey(1) == 27: 
                    break  # esc to quit
            cv2.destroyAllWindows()        
        elif input_path[-4:] == '.mp4': # do detection on a video  
            video_out = output_path + input_path.split('/')[-1]
            video_reader = cv2.VideoCapture(input_path)

            nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_h = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_w = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))

            video_writer = cv2.VideoWriter(video_out,
                                cv2.VideoWriter_fourcc(*'MPEG'), 
                                50.0, 
                                (frame_w, frame_h))
            # the main loop
            batch_size  = 1
            images      = []
            start_point = 0 #%
            show_window = False
            for i in tqdm(range(nb_frames)):
                _, image = video_reader.read()

                if (float(i+1)/nb_frames) > start_point/100.:
                    images += [image]

                    if (i%batch_size == 0) or (i == (nb_frames-1) and len(images) > 0):
                        # predict the bounding boxes
                        batch_boxes = get_yolo_boxes(infer_model, images, net_h, net_w, config['model']['anchors'], obj_thresh, nms_thresh)

                        for i in range(len(images)):
                            # draw bounding boxes on the image using labels
                            draw_boxes(images[i], batch_boxes[i], config['model']['labels'], obj_thresh)   

                            # show the video with detection bounding boxes          
                            if show_window: cv2.imshow('video with bboxes', images[i])  

                            # write result to the output video
                            video_writer.write(images[i]) 
                        images = []
                    if show_window and cv2.waitKey(1) == 27: break  # esc to quit

            if show_window: cv2.destroyAllWindows()
            video_reader.release()
            video_writer.release()       
        else: # do detection on an image or a set of images
            image_paths = []

            if os.path.isdir(input_path): 
                for inp_file in os.listdir(input_path):
                    image_paths += [input_path + inp_file]
            else:
                image_paths += [input_path]

            image_paths = [inp_file for inp_file in image_paths if (inp_file[-4:] in ['.jpg', '.png', 'JPEG'])]

            # the main loop
            for image_path in image_paths:
                image = cv2.imread(image_path)
                print(image_path)
                #cv2.imshow("test",image)
                print(image.shape)
                
                # predict the bounding boxes
                boxes = get_yolo_boxes(infer_model, [image], net_h, net_w, config['model']['anchors'], obj_thresh, nms_thresh)[0]
            
                # draw bounding boxes on the image using labels
                draw_boxes(image, boxes, config['model']['labels'], obj_thresh) 

                #cv2.imshow("Test",image)
                #cv2.waitKey()
                # write the image with bounding boxes to file
                out_path_val = output_path + image_path.split(os.path.sep)[-1] #+output_path
                print("Out Path: ", out_path_val)
                cv2.imwrite(out_path_val, np.uint8(image))    
