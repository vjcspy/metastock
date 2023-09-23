#!/bin/bash
set -e  # Dừng script nếu có lỗi

# Cài đặt module metastock version mới nhất
pip install --upgrade metastock

# Chạy gunicorn
gunicorn -w 2 -b 0.0.0.0:3002 'metastock.http:app'
