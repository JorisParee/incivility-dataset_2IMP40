import pprint
from database import Database
from datetime import datetime

DATABASE_PATH = "extended.db"
db = Database(DATABASE_PATH)

# print(db.get_annotation_count())


import pandas as pd

df_issues = pd.read_csv('../dataset/issue_threads.csv')

try:
    db.insert_test(f'test_run_{datetime.today()}')
except Exception as e:
    print(e)


print(len(db.get_all_comment_annotations()))
