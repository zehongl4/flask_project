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
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT"))
        self.user = os.getenv("DB_USER", "xuan")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
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
                # Create Users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        username VARCHAR(255) PRIMARY KEY,
                        password VARCHAR(255) NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # Create Posts table with a foreign key referencing the Users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS blogs (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) NOT NULL,
                        title VARCHAR(255) NOT NULL,
                        content TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
                    );
                """)

                # Commit the changes
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
        return self.__query_data("SELECT password FROM users WHERE username = %s", (username,))

    def check_user_exist(self, username):
        result = self.__query_data("SELECT password FROM users WHERE username = %s", (username,))
        print(result)
        return result != ()  # Check if the result is not empty

    def add_user(self, username, password):
        self.__insert_or_update_data("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))

    def update_password(self, username, password):
        self.__insert_or_update_data("UPDATE users SET password = %s WHERE username = %s", (password, username))
    
    def add_blog(self, username, title, content):
        print("yyy")
        self.__insert_or_update_data("INSERT INTO blogs (username, title, content) VALUES (%s, %s, %s)", (username, title, content))
    
    def get_blogs_by_username(self, username):
        return self.__query_data("SELECT id, username, title, created_at FROM blogs WHERE username = %s ORDER BY created_at DESC Limit 5", (username,))
    
    def get_blog_by_id(self, id):
        return self.__query_data("SELECT title, content, created_at FROM blogs WHERE id = %s", (id,))       
    def get_user_allblogs(self, username):
        return self.__query_data("SELECT id, username, title, created_at FROM blogs WHERE username = %s ORDER BY created_at DESC", (username,))
