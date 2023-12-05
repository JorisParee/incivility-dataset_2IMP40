# incivility-dataset

In the following, we briefly describe the different components that are included in this project.

## Project Stucture

The project includes the following files and folders:

- __/annotation_app__: A folder that contains the annotation interface we created using `streamlit` library.
    - app.py: The main app file. You have to run this file after deploying the server. To run this file: `streamlit run app.py`.
    - database.py: This file contains the db queries for inserting, updating or selecting various operations during the annotation period.
    - test_db.py: This creates the samples dummy data for hosting it in the server. Run this file once before running `app.py`. 
    - comments.csv: All comments that needs to be annotated.
    - issue_threads.csv: All issue threads that need to be annotated.
    - requirements.txt: the libraries needed to run the app.



- __/dataset__: A folder that contains the annotated data.
    - annoatated_issue_level.csv: csv file that contains the issue level annotation data. This file has 5 columns: `id`, `issue_id`, `trigger`, `target`, `consequences`.
    - annoatated_comment_level.csv: csv file that contains the comment level annotation data. This file has 5 columns: `id`, `issue_id`, `comment_id`, `tbdf`, `comment_body`.


## Samples of data:

- annoatated_issue_level.csv file: 

| id | issue_id  | trigger | target | consequences |
|---|------------|---------|--------------|------------------------------------------|
| 1 | 774727384  | None    | People       | ['Provided technical explanation', 'Discontinued further discussion', 'Accepting criticism'] |
| 2 | 654775761  | None    | People       | ['Discontinued further discussion']      |
| 3 | 1418577350 | None    | Code/tool    | ['Escalating further']                   |

- annotatated_comment_level.csv file: 

| id | issue_id | comment_id | tbdf      | comment_body      |
|---|---------|---------|--------------|--------------|
| 1 | 6209234 | 6209234 | None         | "I noticed... |
| 2 | 6209234 | 7718792 | Entitlement | "Yes, prepare... |
| 3 | 6209234 | 7722530 | None         | "The only dow... |
