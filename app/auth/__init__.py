#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 22:20:39 2024

@author: xuan
"""

# app/auth/__init__.py
from flask import Blueprint
auth = Blueprint('auth', __name__)

from . import routes


