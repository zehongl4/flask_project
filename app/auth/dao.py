#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 19:00:39 2024

@author: xuan
"""

import pymysql

# Database connection function
def conn_mysql():
    return pymysql.connect(
        host="127.0.0.1", 
        port=3306, 
        user="root", 
        password="lanzehong0997", 
        database="flask_db", 
        charset="utf8"
    ) 

class UserDAO:
    def __init__(self):
        pass

    # Execute query and return results              
    def __query_data(self, sql, params=None):
        conn = conn_mysql()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        except pymysql.Error as error:
            print(f"Database error: {error}")
            return None
        finally:
            conn.close()

    # Insert or update data in database
    def __insert_or_update_data(self, sql, params=None):
        conn = conn_mysql()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                conn.commit()
        except pymysql.Error as error:
            print(f"Database error: {error}")
            conn.rollback()
        finally:
            conn.close()

    def get_user_password(self, username):

        return self.__query_data("SELECT password FROM user_log WHERE username = %s", (username,))

    def check_user_exist(self, username):
        result = self.__query_data("SELECT password FROM user_log WHERE username = %s", (username,))
        return result != ()  # Check if the result is not empty


    def add_user(self, username, password):
        self.__insert_or_update_data("INSERT INTO user_log (username, password) VALUES (%s, %s)", (username, password))

    def update_password(self, username, password):
        self.__insert_or_update_data("UPDATE user_log SET password = %s WHERE username = %s", (password, username))

