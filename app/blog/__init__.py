#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 22:20:39 2024

@author: xuan
"""

from flask import Blueprint

blog = Blueprint('blog', __name__)

from . import routes


