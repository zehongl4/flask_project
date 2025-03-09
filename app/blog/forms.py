#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 21:56:42 2024

@author: xuan
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message="Title cannot be empty")])
    content = TextAreaField('Content', validators=[DataRequired(message="Content cannot be empty")])
    submit = SubmitField('Post')

class SearchForm(FlaskForm):
   content = StringField('Content', validators=[Optional()])
   author = StringField('Author', validators=[Optional()])

   # Custom validator to ensure at least one field is filled
   def validate(self, extra_validators=None):
       # First run the default validators
       if not super(SearchForm, self).validate():
           return False
       
       # Check if both fields are empty
       if not self.content.data and not self.author.data:
           msg = "At least one search field must be filled"
           self.content.errors.append(msg)
           self.author.errors.append(msg)
           return False
           
       return True
