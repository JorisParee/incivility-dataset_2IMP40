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
            "CREATE TABLE IF NOT EXISTS project_properties(id INTEGER PRIMARY KEY, \
                issue_id INTEGER not null UNIQUE, \
                project_id INTEGER not null, \
                project_name TEXT not null, \
                nr_of_commits INTEGER not null);"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS commenter_properties(id INTEGER PRIMARY KEY, \
                commenter_id INTEGER not null, \
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

    def insert_annotated_comments(self, issue_id, comment_id, tbdf, comment_body):
        return self.execute(
            "INSERT INTO annotated_comments (issue_id, comment_id, tbdf, comment_body) VALUES (?, ?, ?, ?)",
            [issue_id, comment_id, tbdf, comment_body],
        )

    def insert_annotated_issue(self, issue_id, trigger, target, consequences):
        return self.execute(
            "INSERT INTO annotated_comments (issue_id, trigger, target, consequences) VALUES (?, ?, ?, ?)",
            [issue_id, trigger, target, consequences],
        )

    def insert_commenter_properties(self, commenter_id, score):
        return self.execute(
            "INSERT INTO annotated_comments ( commenter_id, score) VALUES (?, ?)",
            [ commenter_id, score],
        )

    def insert_comments(self, project_name, issue_id, comment_id, comment_body, created_at, user_id):
        return self.execute(
            "INSERT INTO annotated_comments (project_name, issue_id, comment_id, comment_body, created_at, user_id) VALUES (?, ?, ?, ? , ?, ?)",
            [project_name, issue_id, comment_id, comment_body, created_at, user_id],
        )

    def insert_issue_thread(self, issue_id, total_comments, url, issue_title):
        return self.execute(
            "INSERT INTO annotated_comments (issue_id, total_comments, url, issue_title) VALUES (?, ?, ?, ?)",
            [issue_id, total_comments, url, issue_title],
        )

    def insert_project_properties(self, issue_id, project_id, project_name, nr_of_commits):
        return self.execute(
            "INSERT INTO annotated_comments (issue_id, project_id, project_name, nr_of_commits) VALUES (?, ?, ?, ?)",
            [issue_id, project_id, project_name, nr_of_commits],
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

    #?? what use has this?
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


    def get_all_comments(self):
        c = self.conn.cursor()
        data = c.execute("SELECT * FROM comments").fetchall()
        # Get column names from the cursor description
        columns = [column[0] for column in c.description]
        return data, columns

    def get_all_issue_threads(self):
        c = self.conn.cursor()
        data = c.execute("SELECT * FROM issue_threads").fetchall()
        # Get column names from the cursor description
        columns = [column[0] for column in c.description]
        return data, columns

    def get_all_commenter_properteis(self):
        c = self.conn.cursor()
        data = c.execute("SELECT * FROM commenter_properties").fetchall()
        # Get column names from the cursor description
        columns = [column[0] for column in c.description]
        return data, columns

    def get_all_project_properties(self):
        c = self.conn.cursor()
        data = c.execute("SELECT * FROM project_properties").fetchall()
        # Get column names from the cursor description
        columns = [column[0] for column in c.description]
        return data, columns

