#!/bin/bash

exec python app.py
exec python social_distance_det.py
exec python main.py
exec sh -c 'while true ; do wait ; done'
