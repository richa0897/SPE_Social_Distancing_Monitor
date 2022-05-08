# %%

import MySQLdb
from Args_Folder import social_distancing_config as config
from Args_Folder.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import argparse
import imutils
import cv2
import os
from app import app
from datetime import datetime
# %%

def add_to_db(viol_frame):
    final_data={}
    max_key=max(viol_frame.items(),key=lambda k:k[1])
    print(max_key)
    print(type(max_key))
    final_data[max_key[0]]=max_key[1]
    db =MySQLdb.connect(app.config['MYSQL_HOST'],app.config['MYSQL_USER'],app.config['MYSQL_PASSWORD'],app.config['MYSQL_DB'],port=3200)
    cursor=db.cursor()
    for key,value in final_data.items():
        cursor.execute('Insert into violation_db values (%s,%s)',(key,value))
        db.commit()
    db.close()

# %%
def check_violations(results):
    violate=set()
    if len(results)>=2:
        centroids=[r[2] for r in results]
        D = dist.cdist(centroids, centroids, metric="euclidean") #distance matrix D
        for i in range(0, D.shape[0]):
            for j in range(i+1,D.shape[1]):
                if D[i, j] < config.MIN_DISTANCE:
                    violate.add(i)
                    violate.add(j)
    return violate


# %%
""" def set_paths(inp_path,out_path,disp):
    input_path=inp_path
    output_path=out_path
    display=disp """

# %%
def instantiate_model():
    labelsPath = os.path.join(config.MODEL_PATH, "coco.names")
    print(labelsPath)
    LABELS = open(labelsPath).read().strip().split("\n")
    print(LABELS)
    #loading yolov3 model and its weights
    weightsPath = os.path.join(config.MODEL_PATH, "yolov3.weights")
    configPath = os.path.join(config.MODEL_PATH, "yolov3.cfg")
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    #these output layers find bounding boxes at different scales, at each scale 3 bounding boxes are detected then 
    #non maximum suppresion is used to find the best bounding box 
    #these layers are passed to detect_people function for making the prediction given a frame
    return net,ln, LABELS

# %%
def model_run(input_path,output_path,display,net,ln,LABELS):
    print("[INFO] accessing video stream...")
    print(input_path)
    vs = cv2.VideoCapture(input_path)
    writer = None
    count=0
    list_viols={}

    while True:
        grabbed,frame=vs.read() #reading video frame by frame
        if not grabbed: #if frame not found i.e we have reached the end of video
            break
        count+=1
        frame=imutils.resize(frame,width=700)   #resizing the frame
        results = detect_people(frame, net, ln,personIdx=LABELS.index("person")) #calling the detect_people function
        #results contains coordinates of bounding boxes with their confidence, centroids
        
        violations=check_violations(results)
        dateB = datetime.now()
        timeNow = dateB.strftime('%Y-%m-%d %H:%M:%S')
        list_viols[timeNow]=len(violations)
        if(count%10==0):
            add_to_db(list_viols)
            list_viols={}

        # extract the bounding box and centroid coordinates, then initialize the color based on violations or no violations
        for (i, (prob, bbox, centroid)) in enumerate(results):
            (startX, startY, endX, endY) = bbox
            (cX, cY) = centroid
            color = (0, 255, 0)
            if i in violations:# if the index pair exists within the violation set, then # update the color
                color = (0, 0, 255)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            cv2.circle(frame, (cX, cY), 5, color, 1)

        # draw the total number of social distancing violations on the output frame
        text = "Social Distancing Violations: {}".format(len(violations))
        cv2.putText(frame, text, (10, frame.shape[0] - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)    

        if display==True:
            cv2.imshow("frame",frame)
            key=cv2.waitKey(1) & 0xFF
            if key==ord("q"):
                break
        
        if output_path!= "" and writer is None:
            # initialize our video writer
            fourcc = cv2.VideoWriter_fourcc(*'MP4V') ## fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
            writer = cv2.VideoWriter(output_path, fourcc, 25,(frame.shape[1], frame.shape[0]), True)

        if writer is not None:
            writer.write(frame)

    cv2.destroyAllWindows()


# %%



