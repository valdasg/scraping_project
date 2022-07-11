#!/bin/bash
source ~/.venv/bin/activate
cd ~/code
python3 upload_to_s3.py
deactivate
