# Use an official Python runtime as an image
FROM python:3.6

# The EXPOSE instruction indicates the ports on which a container 
# will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5000

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction 
# creates a directory with this name if it doesn’t exist
WORKDIR /app


#Installing yolov3 wts
RUN wget https://pjreddie.com/media/files/yolov3.weights


# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
COPY app.py /app
COPY main.py /app
COPY social_distance_det.py /app
COPY test.py /app
COPY templates /app/templates
COPY static /app/static
COPY yolo-coco /app/yolo-coco
COPY Args_Folder /app/Args_Folder
RUN pip install -r requirements.txt
RUN cp yolov3.weights /app/yolo-coco/


