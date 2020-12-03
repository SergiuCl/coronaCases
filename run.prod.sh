#!/bin/bash

/home/$USER/.local/bin/gunicorn --chdir /home/$USER/coronaCases --bind 0.0.0.0:5000 wsgi:app
