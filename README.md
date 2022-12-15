# Major Project- SPE_Social_Distancing_Monitor

Devops Project on Social Distance Monitoring 

The COVID-19 pandemic has led to a dramatic change in people's lives across the globe. It has caused a plethora of socio-economic concerns and a massive amount of loss of human life. Amidst this chaos, we have learned that social distancing is an effective method to restrict the spread of the coronavirus. However, it can often be a challenge in public places to practice social distancing due to reasons like large crowds, work requirements, or simple ignorance of people. In these scenarios, the authorities (such as government, college administrations, and workplaces) can have a hard time enforcing and monitoring if the people on the premise abide by the physical distancing rules.

Our application, the Social Distancing Monitor (hereinafter referred to as SDM), proposes tackling this issue by developing an application that aids authorities in enforcing social distancing of their premise and performing crowd control as and when necessary. We have used YOLOv3, a state-of-the-art object detection algorithm combined with functionalities that cater to the physical distancing issue.

SDM frontend is built using HTML, CSS, and JavaScript, and the backend is developed using Flask API and Python. MySQL is used to store all the data obtained from the application. Finally, we use DockerHub to fetch the images of our application and database and run them in multiple containers by using Docker-Compose. In addition to this, we also have four more containers running for Filebeat and ELK.
