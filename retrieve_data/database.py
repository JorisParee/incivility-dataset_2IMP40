import sqlite3
import pandas as pd

class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        c = self.conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS annotated_comments(id INTEGER PRIMARY KEY, \
                issue_id INTEGER not null, \
                comment_id INTEGER not null UNIQUE,\
                tbdf TEXT not null,\
                comment_body TEXT not null);"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS annotated_issues(id INTEGER PRIMARY KEY, \
                issue_id INTEGER not null, \
                trigger TEXT not null, \
                target TEXT not null, \
                consequences TEXT not null);"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS issue_threads(id INTEGER PRIMARY KEY, \
                issue_id INTEGER not null UNIQUE, \
                total_comments INTEGER not null, \
                url TEXT not null, \
                issue_title TEXT);"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS comments(id INTEGER PRIMARY KEY, \
                project_name TEXT not null, \
                issue_id INTEGER not null, \
                comment_id INTEGER not null, \
                comment_body TEXT not null, \
                created_at TEXT not null, \
                user_id INTEGER not null);"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS project_props(id INTEGER PRIMARY KEY, \
                issue_id INTEGER not null UNIQUE, \
                project_id INTEGER not null, \
                project_name TEXT not null, \
                nr_of_commits INTEGER not null);"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS commenter_props(user_id INTEGER PRIMARY KEY, \
                score INTEGER not null);"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS testing(id INTEGER PRIMARY KEY, \
                text TEXT not null);"
        )

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()
        return c.lastrowid

    def close(self):
        self.conn.close()


    def insert_test(self, testtext):
        return self.execute(
            "INSERT INTO testing (text) VALUES (?)",
            [testtext],
        )

    def get_all_annotated_issues(self):
        c = self.conn.cursor()
        data = c.execute("SELECT * FROM annotated_issues").fetchall()
        # Get column names from the cursor description
        columns = [column[0] for column in c.description]
        return data, columns

    def get_all_annotated_comments(self):
        c = self.conn.cursor()
        data = c.execute("SELECT * FROM annotated_comments").fetchall()
        # Get column names from the cursor description
        columns = [column[0] for column in c.description]
        return data, columns



    def get_all_comment_annotations(self):
        data = self.select("SELECT * FROM annotated_comments;")
        comment_annotations = []
        for d in data:
            retval = {
                "issue_id": d[1],
                "comment_id": d[2],
                "tbdf": d[3]
            }
            comment_annotations.append(retval)
        return comment_annotations

    def get_all_issue_annotations(self):
        data = self.select("SELECT * FROM annotated_issues;")
        annotated_issues = []
        for d in data:
            retval = {
                "issue_id": d[1],
                "trigger": d[2],
                "target": d[3],
                "consequences": d[4],
                "additional_comments": d[5]
            }
            annotated_issues.append(retval)
        return annotated_issues
