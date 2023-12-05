import pprint
from database import Database

DATABASE_PATH = "annotation.db"
db = Database(DATABASE_PATH)

# print(db.get_annotation_count())

db.create_user('db_admin', '1')
db.create_user('dummy_user', '0')

import pandas as pd

df_issues = pd.read_csv('issue_threads.csv')

for idx, row in df_issues.iterrows():
    db.create_issue_log(row['issue_id'])


print(db.get_next_avaiable_issue())
