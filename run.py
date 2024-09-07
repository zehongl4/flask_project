#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 21:09:16 2024

@author: xuan
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
