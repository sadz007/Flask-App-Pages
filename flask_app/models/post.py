from flask_app.config.mysqlconnection import connectToMySQL
from flask  import Flask
from flask_app.models.user import User
from flask import flash

class Post:
    db = "pages_schema"
    def __init__(self,data):
        self.id =data["id"]
        self.content = data["content"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.user = data["user"]
        
    @classmethod
    def save(cls,data):
        if not cls.valid_post(data):
            
            return False
        
        
        
        query = """INSERT INTO posts(content,user_id)
                VALUES(%(content)s,%(user_id)s)"""
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results
    
    @classmethod
    def delete(cls,post_id):
        query = """DELETE FROM posts WHERE id = %(id)s"""
        connectToMySQL(cls.db).query_db(query,{"id":post_id})
        return post_id
    
    @classmethod
    def valid_post(cls,data):
        is_valid = False
        if len(data["content"]) == 0:
            flash("Error:Your submitting an empty post")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM posts
                JOIN users on posts.user_id = users.id"""
        results = connectToMySQL(cls.db).query_db(query)
        
        
        
        all_post  = []
        
        for row in results:
            user_post = User({
                "id": row["user_id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"]
            })
            new_post = Post({
                "id":row["id"],
                "content":row["content"],
                "created_at":row["created_at"],
                "updated_at":row["updated_at"],
                "user":user_post
            })
            all_post.append(new_post)
        
        return all_post