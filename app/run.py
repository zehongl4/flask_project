#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 20:55:24 2024

@author: xuan
"""

# run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)