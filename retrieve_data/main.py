import time
import random

from git_api import *
from database import Database

DATABASE_PATH = "extended.db"
db = Database(DATABASE_PATH)


def save_single_commit(commit, project_id):

    db.insert_commit([x for x in parse_single_commit(commit, project_id)])

def parse_single_commit(commit, project_id):
    authorlogin, authorid, committerlogin, committorid = None, None, None, None
    if (not commit['author'] is None and commit['author'] != {}):
        authorlogin = commit['author']['login']
        authorid = commit['author']['id']

    if (not commit['committer'] is None and commit['committer'] != {}):
        committerlogin = commit['committer']['login']
        committorid = commit['committer']['id']

    return[
        project_id,
        commit['node_id'],
        authorlogin or None,
        commit['commit']['author']['name'],
        authorid or None,
        committerlogin or None,
        commit['commit']['committer']['name'],
        committorid or None,
        commit['commit'].get('message', None),
        commit['commit']['verification']['verified_at'] or commit['commit']['author']['date'],
    ]



def save_all_commits_for_project(owner, repo):
    commits = get_repository_commits(owner, repo)
    commit_values = []
    for commit in commits:
        #save_single_commit(commit, f'{owner}/{repo}')
        commit_values.append(parse_single_commit(commit, f'{owner}/{repo}'))
    db.insert_commit_list(commit_values)
    print("Saved all commits for" + f'{owner}/{repo}')

def check_project_handled(project_name):
    data, columns = db.get_commits_by_project(project_name)
    return len(data) > 0

def handle_commits_for_issue(issue_id, runanyway = False):
    print("started for issue: " + str(issue_id) + " at time: " + str(time.ctime()))
    issue, columns = db.get_issue_thread_by_id(issue_id)
    if (len(issue) == 0):
        print("No issues are found for id")
        return
    url = issue[0][3]
    owner, repo = get_project_owner_and_name(url)
    if check_project_handled(f'{owner}/{repo}'):
       print("project already handled")
       if runanyway:
           print("deleting and rerunning anyway")
           db.delete_commits_for_project(f'{owner}/{repo}')
           save_all_commits_for_project(owner, repo)
    else:
        print("running project" + f'{owner}/{repo}')
        save_all_commits_for_project(owner, repo)
    print("finished for issue: " + str(issue_id))

def run_for_all_issues():
    issues, columns = db.get_all_issue_threads()
    for issue in issues:
        handle_commits_for_issue(issue[columns.index("issue_id")], )

#handle_commits_for_issue(12894489, True)
#run_for_all_issues()


def randomness_list(n):
    new = list(range(n))
    random.shuffle(new)
    list_res = []
    for i in range(n):
        list_res.append([new[i], i])
    return list_res

def add_random_to_issue_threads(new_column):
    idcol = 'id'
    issue_thread_list = db.get_all_issue_threads()
    highest = max(list(map(lambda x: x[issue_thread_list[1].index(idcol)],issue_thread_list[0])))
    replace = randomness_list(highest)
    db.add_column_with_number('issue_threads', idcol, new_column, replace)

add_random_to_issue_threads('random_sampling_int')