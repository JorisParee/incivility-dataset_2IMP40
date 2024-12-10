import pprint
from database import Database

DATABASE_PATH = "extended.db"
db = Database(DATABASE_PATH)

# print(db.get_annotation_count())

try:
    db.create_user('db_admin', '1')
except Exception as e:
    print(e)
try:
    db.create_user('dummy_user', '0')
except Exception as e:
    print(e)

import pandas as pd

df_issues = pd.read_csv('../dataset/issue_threads.csv')

for idx, row in df_issues.iterrows():
    try:
        db.create_issue_log(row['issue_id'])
    except Exception as e:
        print(e)


print(db.get_next_avaiable_issue())
