import pprint
from database import Database
from datetime import datetime

DATABASE_PATH = "extended.db"
db = Database(DATABASE_PATH)

# print(db.get_annotation_count())


import pandas as pd

df_issues = pd.read_csv('../dataset/issue_threads.csv')
df_issues_annotated = pd.read_csv('../dataset/annotated_issue_level.csv')
df_comments = pd.read_csv('../dataset/comments.csv')
df_comments_annotated = pd.read_csv('../dataset/annotated_comment_level.csv')

try:
    db.insert_test(f'test_run_{datetime.today()}')
except Exception as e:
    print(e)

try:
    for idx, issue in df_issues.iterrows():
        db.insert_issue_thread(issue['issue_id'], issue['total_comments'], issue['url'], issue['issue_title'])
except Exception as e:
    print(e)

try:
    for idx, comment in df_comments.iterrows():
        db.insert_comments(comment['project_name'], comment['issue_id'], comment['comment_id'], comment['comment_body'], comment['created_at'], comment['user_id'])
except Exception as e:
    print(e)

print("#issue threads: " + str(len(db.get_all_issue_threads()[0])))
print("#comments: " + str(len(db.get_all_comments()[0])))
