#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 19:00:39 2024

@author: xuan
"""

import pymysql
import os

class UserDAO:
    def __init__(self):
        # Use environment variables to determine the database settings
        self.host = os.getenv("DB_HOST", "blogflask.cb0icek8ubb6.us-east-2.rds.amazonaws.com")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.user = os.getenv("DB_USER", "xuan")
        self.password = os.getenv("DB_PASSWORD", "Lzh!09231201")
        self.database = os.getenv("DB_NAME", "db_blog")
        self.charset = "utf8"

        # Initialize the database if not in local development mode
        self.initialize_database()
        pass

    def conn_mysql(self):
        # Attempt to connect to the MySQL server
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset
        )

    def initialize_database(self):
        conn = self.conn_mysql()
        try:
            with conn.cursor() as cursor:
                # Create a table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_log (
                        username VARCHAR(255) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL,
                        PRIMARY KEY (username)
                    );
                """)
                conn.commit()
        except pymysql.Error as e:
            print(f"An error occurred while initializing the database: {e}")
        finally:
            conn.close()

    def __query_data(self, sql, params=None):
        conn = self.conn_mysql()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        except pymysql.Error as error:
            print(f"Database error: {error}")
            return None
        finally:
            conn.close()

    def __insert_or_update_data(self, sql, params=None):
        conn = self.conn_mysql()
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

