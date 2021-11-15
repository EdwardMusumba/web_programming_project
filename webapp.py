import sqlite3
from sqlite3 import Error
import json 
import json

from flask import Flask, Response
from flask_restful import Api, Resource, request
from flask_cors import CORS


def create_connection(db_filename):
    conn = None
    try:
        conn = sqlite3.connect(db_filename)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn
def create_table(conn, create_table_sql):
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        print(e)
"""

CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY,
    name text NOT NULL,
    email text NOT NULL, 
    password text NOT NULL,
    
);
"""





def create_user(conn, user):
    query = """INSERT INTO users(name, email, password)
    VALUES(?,?,?)"""
    cur = conn.cursor()
    cur.execute(query, user)
    conn.commit()
    return cur.lastrowid


def get_users(conn):
    query = """SELECT * FROM users"""
    cur = conn.cursor()
    results = cur.execute(query)
    return list(results) 


def get_username_and_email(conn):
    query = "SELECT name, email FROM users"
    cur = conn.cursor()
    results = cur.execute(query)
    return list(results)


def username(users):
    for user in users:
        print(f"Username: {user[1]}")


app = Flask(__name__)
CORS(app)
api = Api(app)


class User(Resource):
   
    USER_DATABASE = "src/users.db"


    def get(self, user_id=None):
        conn = create_connection(self.USER_DATABASE)
        if user_id is None:
            try:
                users = get_username_and_email(conn)
                users_json = json.dumps(users)
                response = Response(response=users_json, status=200, content_type="application/json")
            except:
                conn.close()
                response = Response('{"error": "Failed to get all users"}', status=500, content_type="application/json")    
                error = {
                    "error": "Failed to get all users"
                }
                response = Response(json.dumps(error), status=500, content_type="application/json")
        else:
            response = Response(status=400, content_type='application/json')
        conn.close()
        return response 

    def post(self):
        
        conn = create_connection(self.USER_DATABASE)
        data = request.json
        user = (data['name'], data['email'], data['password'])
        try:
            create_user(conn, user)
            response = Response(status=200, content_type="application/json")
            new_user = {
                "email": data["email"],
                "name": data["name"]
            }
            response = Response(json.dumps(new_user), status=200, content_type="application/json")
        except Exception as e:
            print(e)
            response = Response('{"error": "Failed to get create user"}', status=500, content_type="application/json")
            error = {
                "error": "Failed to get create user"
            }
            response = Response(json.dumps(error), status=500, content_type="application/json")
        conn.close()
        return response 

api.add_resource(User, '/users', '/users/<string:id>')


if __name__ == "__main__":

 app.run(debug=True)

