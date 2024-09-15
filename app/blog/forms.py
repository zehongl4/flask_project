#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 21:56:42 2024

@author: xuan
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message="Title cannot be empty")])
    content = TextAreaField('Content', validators=[DataRequired(message="Content cannot be empty")])
    submit = SubmitField('Post')
