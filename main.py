from distutils.log import error
from Args_Folder import social_distancing_config as config
from Args_Folder.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import argparse
import imutils
import cv2
import os
from social_distance_det import check_violations,instantiate_model,model_run
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template,session
from werkzeug.utils import secure_filename
import MySQLdb
import matplotlib.pyplot as plt
import pandas as pd
import logging

logging.basicConfig(filename='sdm_logfile.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s : %(message)s')


@app.route('/')
def home():
	return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST':
		db=MySQLdb.connect(app.config['MYSQL_HOST'],app.config['MYSQL_USER'],app.config['MYSQL_PASSWORD'],app.config['MYSQL_DB'],port=3306)
		cursor=db.cursor()
		username = request.form['username']
		password = request.form['password']	
		cursor.execute('SELECT username,password FROM admins WHERE username = %s AND password = %s', (username, password))
		admin = cursor.fetchone()
		print(username,password)
		if admin:
			session['loggedin'] = True
			session['username'] = admin[0]
			return redirect('/dashboard')
		else:
			msg = 'Incorrect username/password!'
	return render_template('login.html', error=msg)


@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('username', None)
	if os.path.isfile(os.path.join(app.config['OUTPUT_FOLDER'], 'outputgraph.jpg')):
		os.remove(os.path.join(app.config['OUTPUT_FOLDER'], 'outputgraph.jpg'))
	# Redirect to login page
	return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

@app.route('/upload')
def upload_form():
	return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_video():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No video selected for uploading')
		return redirect(request.url)
	else:
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		print('upload_video filename: ' + filename)
		print(os.path.join(app.config['OUTPUT_FOLDER'], filename))
		flash('Video successfully uploaded and displayed below')
		net,ln,LABEL=instantiate_model()
		model_run(os.path.join(app.config['UPLOAD_FOLDER'],filename),os.path.join(app.config['OUTPUT_FOLDER'], filename),True,net,ln,LABEL)
		print("abc")
		return render_template('upload.html', filename=filename)

@app.route('/show_violations', methods=['GET', 'POST'])
def show_violations():
	violations = request.form['violations']
	db=MySQLdb.connect(app.config['MYSQL_HOST'],app.config['MYSQL_USER'],app.config['MYSQL_PASSWORD'],app.config['MYSQL_DB'])
	cursor=db.cursor()
	cursor.execute('SELECT * FROM violation_db where no_of_violations >= %s and DATE(created_at) = CURDATE()',(violations,))
	result = cursor.fetchall
	timing = []
	no_vio = []
	for i in cursor:
		timing.append(i[0])
		no_vio.append(i[1])
	print("Time = ", timing)
	print("No. of Violations = ", no_vio)
	vio_df = pd.DataFrame(list(zip(timing, no_vio)), columns = ['Time', 'No. of Violations'])
	table = vio_df.to_html(classes='table table-stripped')
	return render_template("dashboard.html",table=table)
	

@app.route('/graph', methods=['GET', 'POST'])
def graph():
	db=MySQLdb.connect(app.config['MYSQL_HOST'],app.config['MYSQL_USER'],app.config['MYSQL_PASSWORD'],app.config['MYSQL_DB'],port=3306)
	cursor=db.cursor()
	cursor.execute('SELECT TIME(created_at), no_of_violations from violation_db where DATE(created_at) = CURDATE();')
	result = cursor.fetchall
	timing = []
	no_vio = []
	for i in cursor:
		timing.append(str(i[0]))
		no_vio.append(int(i[1]))
	print("Time = ", type(timing[0]))	
	print("Time = ", timing)
	print("No. of Violations = ", no_vio)
	plt.figure(figsize=(10,6), tight_layout=True)
	ax = plt.subplot(111)
	#plotting
	ax.plot(timing,no_vio, 'o-', linewidth=2)
	#customization
	plt.xticks(range(len(timing)), timing, size='small')
	plt.xlabel('Time of Violation')
	plt.ylabel('No. of Violations')
	plt.title('All Violations Today')
	l = plt.fill_between(timing, no_vio)
	# change the fill into a blueish color with opacity .3
	l.set_facecolors([[.5,.5,.8,.3]])
	# change the edge color (bluish and transparentish) and thickness
	l.set_edgecolors([[0, 0, .5, .3]])
	l.set_linewidths([3])

	# tweak the axis labels
	xlab = ax.xaxis.get_label()
	ylab = ax.yaxis.get_label()

	xlab.set_style('italic')
	xlab.set_size(10)
	ylab.set_style('italic')
	ylab.set_size(10)
	ttl = ax.title
	ttl.set_weight('bold')
	ax.grid('on')
	plt.savefig("static/output/outputgraph.jpg")
	#plt.show()
	return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
