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


## Definitions

### Uncivil Features (TBDFs):
**Bitter frustration**: when someone expresses strong frustration

**Impatience**: participants might demonstrate impatience when they express a feeling that it is taking too long to solve a problem, understand a solution, or answer a question

**Irony**: contributors used expressions that usually signify the opposite in a mocking or blaming tone

**Insulting**: Insulting remarks directed at another person

**Mocking**: when a discussion participant is making fun of someone else, usually because that person has made a mistake

**Threat**: contributors put a condition impacting the result of another discussion participant or that person’s career

**Vulgarity**: using profanity or language that is not considered proper

**Entitlement**: expecting special privileges, attention, or resources without regard for the norms of collaboration and respect

**Identity attack/Name-Calling**: Race, Religion, Nationality, Gender, Sexual-oriented, or any other kind of attacks and mean/offensive words directed at someone or a gorup of people

### Triggers:
**Failed use of tool/code or error messages**: trouble with code/tool

**Communication breakdown**: being misinterpreted by people or being unable to follow

**Rejection**: receiving a quick rejection or a rejection without sufficient explanation

**Violation of community conventions**: disagreement with the workflow imposed by the community

**Past interactions**: comments are posted that refer to past interactions of the author with the project

**Politics/ideology**: arising over politics or ideology differences (specific beliefs)

**Technical disagreement**: have differing views on some technical component of the project

**Unprovoked**: uncivil behavior or hostility occurs without an apparent reason or trigger

### Targets:
**Code/tool**: code (things or objects)

**People**: targeted at people

**Company/organization**: targeted at companies or organizations

**Self-directed**: targeted at self

**Undirected**: can’t be targeted at people/things. Mostly in the form of profanities

### Consequences:
**Invoke Code of Conduct**: moderators/maintainers invoking CoC

**Turning constructive**: after the uncivil comment, discussion becomes constructive (no more uncivil comments)

**Escalating further**: more uncivil messages are exchanged after the first one

**Discontinued further discussion**: no more messages are exchanged

**Provided technical explanation**: provide technical explanations even after receiving uncivil comment

**Accepting criticism**: they accept the criticisms instead of closing/locking the issue, or discontinuing further discussion

**Trying to stop the incivility**: actively trying to put a stop to incivility, but not necessarily invoking Code of Conduct


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
| 1 | 6209234 | 6209234 | None         | "I noticed that Prepared Statements ..." |
| 2 | 6209234 | 7718792 | Entitlement | "Yes, prepared statements are on ..." |
| 3 | 6209234 | 7722530 | None         | "The only downside with the SQL-based ..."|
