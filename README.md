# incivility-dataset

The repository contains the collected heated issues and annotated data, focusing on identifying incivility in issue threads within GitHub open-source projects. Criteria for data selection included a minimum of 50 contributors, locked issues labeled as "too-heated," "off-topic," or "spam," and a timeframe from April 7, 2013, to October 24, 2023. Data was collected using the GitHub API and GH Archive, resulting in 338 instances labeled as "too-heated," 21 as "spam," and 33 as "off-topic." A custom annotation tool, built with Streamlit, facilitated the annotation process. The final annotated dataset comprises 5,961 issue comments, with 1,365 annotated with uncivil features. 

In the following, we briefly describe the different components that are included in this repository.

## Project Structure

The project includes the following files and folders:

- __/annotation_app__: A folder that contains the annotation interface we created using the `streamlit` library.
    - app.py: The main app file. You have to run this file after deploying the server. To run this file: `streamlit run app.py`.
    - database.py: This file contains the db queries for inserting, updating, or selecting various operations during the annotation period.
    - test_db.py: This creates the sample dummy data for hosting it on the server. Run this file once before running `app.py`. 
    - requirements.txt: The libraries needed to run the app.
    - instructions.txt: The definitions of the TBDF, Trigger, Target and Consequence.
    - config.ini: The configuration file for different input files.
    - - __/screenshot__: folder that contains screenshots of the annotation app in streamlit.



- __/dataset__: A folder that contains the annotated data.
    - comments.csv: All comments that need to be annotated.
    - issue_threads.csv: All issue threads that need to be annotated.
    - annotated_issue_level.csv: CSV file that contains the issue-level annotation data. This file has 5 columns: `id`, `issue_id`, `trigger`, `target`, and `consequences`.
    - annotated_comment_level.csv: CSV file that contains the comment level annotation data. This file has 5 columns: `id`, `issue_id`, `comment_id`, `tbdf`, and `comment_body`.


## Definitions

### Uncivil Features (TBDFs):
- **Bitter frustration**: when someone expresses strong frustration
- **Impatience**: participants might demonstrate impatience when they express a feeling that it is taking too long to solve a problem, understand a solution, or answer a question
- **Irony**: contributors used expressions that usually signify the opposite in a mocking or blaming tone
- **Insulting**: Insulting remarks directed at another person
- **Mocking**: when a discussion participant is making fun of someone else, usually because that person has made a mistake
- **Threat**: contributors put a condition impacting the result of another discussion participant or that person’s career
- **Vulgarity**: using profanity or language that is not considered proper
- **Entitlement**: expecting special privileges, attention, or resources without regard for the norms of collaboration and respect
- **Identity attack/Name-Calling**: Race, Religion, Nationality, Gender, Sexual-oriented, or any other kind of attack and mean/offensive words directed at someone or a group of people

### Triggers:
- **Failed use of tool/code or error messages**: trouble with code/tool
- **Communication breakdown**: being misinterpreted by people or being unable to follow
- **Rejection**: receiving a quick rejection or a rejection without sufficient explanation
- **Violation of community conventions**: disagreement with the workflow imposed by the community
- **Past interactions**: comments are posted that refer to past interactions of the author with the project
- **Politics/ideology**: arising over politics or ideology differences (specific beliefs)
- **Technical disagreement**: have differing views on some technical components of the project
- **Unprovoked**: uncivil behavior or hostility occurs without an apparent reason or trigger

### Targets:
- **Code/tool**: code (things or objects)
- **People**: targeted at people
- **Company/organization**: targeted at companies or organizations
- **Self-directed**: targeted at self
- **Undirected**: can’t be targeted at people/things. Mostly in the form of profanities

### Consequences:
- **Invoke Code of Conduct**: moderators/maintainers invoking CoC
- **Turning constructive**: after the uncivil comment, the discussion becomes constructive (no more uncivil comments)
- **Escalating further**: more uncivil messages are exchanged after the first one
- **Discontinued further discussion**: no more messages are exchanged
- **Provided technical explanation**: provide technical explanations even after receiving an uncivil comment
- **Accepting criticism**: they accept the criticisms instead of closing/locking the issue, or discontinuing further discussion
- **Trying to stop the incivility**: actively trying to put a stop to incivility, but not necessarily invoking the Code of Conduct


## Samples of data:

- annotated_issue_level.csv file: 

| id | issue_id  | trigger | target | consequences |
|---|------------|---------|--------------|------------------------------------------|
| 1 | 774727384  | None    | People       | ['Provided technical explanation', 'Discontinued further discussion', 'Accepting criticism'] |
| 2 | 654775761  | None    | People       | ['Discontinued further discussion']      |
| 3 | 1418577350 | None    | Code/tool    | ['Escalating further']                   |

- annotated_comment_level.csv file: 

| id  | issue_id   | comment_id   | tbdf     | comment              |
|----|-----------|-----------|-------------|----------------------|
| 12 | 12894489  | 913845504 | Irony       | "Imagine thinking anyone cares about design flaws." |
| 17 | 13258430  | 16461191  | None        | "Why do you close the issue?" |
| 18 | 13258430  | 16461276  | Bitter frustration | "Because you don't offer a patch, and profanity really pisses me off." |
