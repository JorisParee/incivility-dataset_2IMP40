
WITH ISSUETHREADINFO AS (
    SELECT issue_threads.id, issue_threads.issue_id, issue_threads.project_name, min(comments.created_at) AS startDate, max(comments.created_at) AS endDate FROM issue_threads
    LEFT JOIN comments ON comments.issue_id = issue_threads.issue_id
    GROUP BY issue_threads.id, issue_threads.issue_id, issue_threads.project_name
),
COMMITSJOINEDQUERYBEFORE AS (
    SELECT issue_threads_info.*, project_commits.* FROM ISSUETHREADINFO issue_threads_info
    LEFT JOIN project_commits ON project_commits.project_name = issue_threads_info.project_name
    AND issue_threads_info.startDate > project_commits.verified_date
),
COMMITSJOINEDQUERYHALFYEAR AS (
    SELECT commits_before.* from COMMITSJOINEDQUERYBEFORE commits_before
    WHERE DATE(commits_before.startDate, '-6 month') <= commits_before.verified_date
),
COMMITSUNDUPED AS (
    select MIN(project_commits.id) AS id, project_name, MIN(node_id) AS node_id, author_id, author_login, author_name, committer_id, committer_login, committer_name, message, MIN(verified_date) AS verified_date FROM project_commits
    GROUP BY project_name, author_id, author_login, author_name, committer_id, committer_login, committer_name, message, STRFTIME('%F %H', verified_date)
),
COMMITSBOTREMOVED AS (
    SELECT project_commits.* FROM project_commits
    WHERE lower(committer_name) not like '%bot%' AND committer_name != 'GitHub' AND committer_id IS NOT null
),
COMMITSJOINEDQUERYBEFORENOBOT AS (
    SELECT issue_threads_info.*, project_commits.* FROM ISSUETHREADINFO issue_threads_info
    LEFT JOIN COMMITSBOTREMOVED project_commits ON project_commits.project_name = issue_threads_info.project_name
    AND issue_threads_info.startDate > project_commits.verified_date
),
COMMITSJOINEDQUERYHALFYEARNOBOT AS (
    SELECT commits_before.* from COMMITSJOINEDQUERYBEFORENOBOT commits_before
    WHERE DATE(commits_before.startDate, '-6 month') <= commits_before.verified_date
)

SELECT issue.*, c.count_before, c2.count_halfyear, c3.count_contributers_before, c4.count_contributers_halfyear, c5.count_before_nobot, c6.count_halfyear_nobot  FROM ISSUETHREADINFO issue
LEFT JOIN (
    SELECT issue_id, COUNT(commits.committer_id) AS count_before FROM COMMITSJOINEDQUERYBEFORE commits
    GROUP BY commits.issue_id
) c ON issue.issue_id = c.issue_id
LEFT JOIN (
    SELECT issue_id, COUNT(commits.committer_id) AS count_halfyear FROM COMMITSJOINEDQUERYHALFYEAR commits
    GROUP BY commits.issue_id
) c2 ON issue.issue_id = c2.issue_id
LEFT JOIN (
    SELECT issue_id, COUNT(distinct commits.committer_id) AS count_contributers_before FROM COMMITSJOINEDQUERYBEFORE commits
    GROUP BY commits.issue_id
) c3 ON issue.issue_id = c3.issue_id
LEFT JOIN (
    SELECT issue_id, COUNT(distinct commits.committer_id) AS count_contributers_halfyear FROM COMMITSJOINEDQUERYHALFYEAR commits
    GROUP BY commits.issue_id
) c4 ON issue.issue_id = c4.issue_id
LEFT JOIN (
    SELECT issue_id, COUNT(commits.committer_id) AS count_before_nobot FROM COMMITSJOINEDQUERYBEFORENOBOT commits
    GROUP BY commits.issue_id
) c5 ON issue.issue_id = c5.issue_id
LEFT JOIN (
    SELECT issue_id, COUNT(commits.committer_id) AS count_halfyear_nobot FROM COMMITSJOINEDQUERYHALFYEARNOBOT commits
    GROUP BY commits.issue_id
) c6 ON issue.issue_id = c6.issue_id;




WITH ISSUETHREADINFO AS (
    SELECT issue_threads.id, issue_threads.issue_id, issue_threads.project_name, min(comments.created_at) AS startDate, max(comments.created_at) AS endDate FROM issue_threads
    LEFT JOIN comments ON comments.issue_id = issue_threads.issue_id
    GROUP BY issue_threads.id, issue_threads.issue_id, issue_threads.project_name
),
ISSUECOMMENTERINFO AS (
    SELECT t.user_id, t.issue_id AS comment_issue_id, ISSUETHREADINFO.* FROM (SELECT comments.issue_id, comments.user_id
                      FROM comments
                      GROUP BY comments.issue_id, comments.user_id) t
    LEFT JOIN ISSUETHREADINFO ON t.issue_id = ISSUETHREADINFO.issue_id
    WHERE ISSUETHREADINFO.issue_id IS NOT NULL
),
COMMITSJOINEDQUERYBEFORE AS (
    SELECT issue_commenter_info.*, project_commits.*FROM ISSUECOMMENTERINFO issue_commenter_info
    LEFT JOIN project_commits ON project_commits.project_name = issue_commenter_info.project_name AND project_commits.committer_id = issue_commenter_info.user_id
    AND issue_commenter_info.startDate > project_commits.verified_date
),
COMMITSJOINEDQUERYHALFYEAR AS (
    SELECT commits_before.* from COMMITSJOINEDQUERYBEFORE commits_before
    WHERE DATE(commits_before.startDate, '-6 month') <= commits_before.verified_date
),
COMMITSUNDUPED AS (
    select MIN(project_commits.id) AS id, project_name, MIN(node_id) AS node_id, author_id, author_login, author_name, committer_id, committer_login, committer_name, message, MIN(verified_date) AS verified_date FROM project_commits
    GROUP BY project_name, author_id, author_login, author_name, committer_id, committer_login, committer_name, message, STRFTIME('%F %H', verified_date)
),
COMMITSBOTREMOVED AS (
    SELECT project_commits.* FROM project_commits
    WHERE lower(committer_name) not like '%bot%' AND committer_name != 'GitHub' AND committer_id IS NOT null
),
COMMITSJOINEDQUERYBEFORENOBOT AS (
    SELECT issue_commenter_info.*, project_commits.* FROM ISSUECOMMENTERINFO issue_commenter_info
    LEFT JOIN COMMITSBOTREMOVED project_commits ON project_commits.project_name = issue_commenter_info.project_name AND project_commits.committer_id = issue_commenter_info.user_id
    AND issue_commenter_info.startDate > project_commits.verified_date
),
COMMITSJOINEDQUERYHALFYEARNOBOT AS (
    SELECT commits_before.* from COMMITSJOINEDQUERYBEFORENOBOT commits_before
    WHERE DATE(commits_before.startDate, '-6 month') <= commits_before.verified_date
)


SELECT issuecommenter.*, c.count_before, c2.count_halfyear, c3.count_contributers_before, c4.count_contributers_halfyear, c5.count_before_nobot, c6.count_halfyear_nobot FROM ISSUECOMMENTERINFO issuecommenter
LEFT JOIN (
    SELECT issue_id, commits.user_id, COUNT(commits.committer_id) AS count_before FROM COMMITSJOINEDQUERYBEFORE commits
    GROUP BY commits.issue_id, commits.user_id
) c ON issuecommenter.issue_id = c.issue_id AND issuecommenter.user_id = c.user_id
LEFT JOIN (
    SELECT issue_id, commits.user_id, COUNT(commits.committer_id) AS count_halfyear FROM COMMITSJOINEDQUERYHALFYEAR commits
    GROUP BY commits.issue_id, commits.user_id
) c2 ON issuecommenter.issue_id = c2.issue_id AND issuecommenter.user_id = c2.user_id
LEFT JOIN (
    SELECT issue_id, commits.user_id, COUNT(distinct commits.committer_id) AS count_contributers_before FROM COMMITSJOINEDQUERYBEFORE commits
    GROUP BY commits.issue_id, commits.user_id
) c3 ON issuecommenter.issue_id = c3.issue_id AND issuecommenter.user_id = c3.user_id
LEFT JOIN (
    SELECT issue_id, commits.user_id, COUNT(distinct commits.committer_id) AS count_contributers_halfyear FROM COMMITSJOINEDQUERYHALFYEAR commits
    GROUP BY commits.issue_id, commits.user_id
) c4 ON issuecommenter.issue_id = c4.issue_id AND issuecommenter.user_id = c4.user_id
LEFT JOIN (
    SELECT issue_id, commits.user_id, COUNT(commits.committer_id) AS count_before_nobot FROM COMMITSJOINEDQUERYBEFORENOBOT commits
    GROUP BY commits.issue_id, commits.user_id
) c5 ON issuecommenter.issue_id = c5.issue_id AND issuecommenter.user_id = c5.user_id
LEFT JOIN (
    SELECT issue_id, commits.user_id, COUNT(commits.committer_id) AS count_halfyear_nobot FROM COMMITSJOINEDQUERYHALFYEARNOBOT commits
    GROUP BY commits.issue_id, commits.user_id
) c6 ON issuecommenter.issue_id = c6.issue_id AND issuecommenter.user_id = c6.user_id;


-- #Simple query counting amount of commits prevous of issue
SELECT t.issue_id, t.project_name, t.start_date, COUNT(project_commits.id) FROM
(SELECT issue_threads.issue_id, issue_threads.project_name, min(comments.created_at) as start_date FROM issue_threads
LEFT JOIN comments ON comments.issue_id = issue_threads.issue_id
GROUP BY issue_threads.issue_id, issue_threads.project_name) t
LEFT JOIN project_commits ON project_commits.project_name = t.project_name AND project_commits.verified_date < t.start_date
GROUP BY t.issue_id, t.project_name, t.start_date;

-- Rewrite of simple to use group in join
SELECT t.issue_id, t.project_name, t.start_date, COUNT(project_commits.id) FROM
(SELECT issue_threads.issue_id, issue_threads.project_name, min(comments.created_at) as start_date FROM issue_threads
LEFT JOIN comments ON comments.issue_id = issue_threads.issue_id
GROUP BY issue_threads.issue_id, issue_threads.project_name) t
LEFT JOIN project_commits ON project_commits.project_name = t.project_name AND project_commits.verified_date < t.start_date
GROUP BY t.issue_id, t.project_name, t.start_date;



-- #Double query for calculating both half year commits and alltime commits before issue start
SELECT t2.issue_id, t2.project_name, t2.start_date, t2.half_year_before, t2.commits_before, COUNT(halfyear.id) AS commits_half_year_before FROM
    (SELECT t.issue_id, t.project_name, t.start_date, t.half_year_before, COUNT(alltime.id) AS commits_before FROM
        (SELECT issue_threads.issue_id, issue_threads.project_name, date(min(comments.created_at)) as start_date, date(min(comments.created_at), '-6 month') AS half_year_before FROM issue_threads
        LEFT JOIN comments ON comments.issue_id = issue_threads.issue_id
        GROUP BY issue_threads.issue_id, issue_threads.project_name
        ) t
    LEFT JOIN project_commits AS alltime ON alltime.project_name = t.project_name AND alltime.verified_date <= t.start_date
    GROUP BY t.issue_id, t.project_name, t.start_date, t.half_year_before
    ) t2
LEFT JOIN project_commits AS halfyear ON halfyear.project_name = t2.project_name AND halfyear.verified_date <= t2.start_date AND halfyear.verified_date > t2.half_year_before
GROUP BY t2.issue_id, t2.project_name, t2.start_date, t2.half_year_before, t2.commits_before;


-- Query for calculating per distinct user that has posted comments how many commits they have in the project
SELECT t2.issue_id, t2.project_name, t2.user_id, t2.start_issue, t2.half_year_before, t2.commitamount_last_half, COUNT(project_commits.author_id) AS total_commits_author FROM
    (SELECT t.issue_id, issue_threads.project_name, t.user_id, t.start_issue, t.half_year_before, count(project_commits.author_id) AS commitamount_last_half FROM
        (SELECT c.issue_id, c.user_id, date(min(c2.created_at)) AS start_issue, date(min(c2.created_at), '-8 month') AS half_year_before  FROM
            (SELECT distinct comments.issue_id, comments.user_id from comments) c
        LEFT JOIN comments c2 on c.issue_id = c2.issue_id
        GROUP BY c.issue_id, c.user_id) t
    LEFT JOIN issue_threads ON t.issue_id = issue_threads.issue_id
    LEFT JOIN project_commits ON issue_threads.project_name = project_commits.project_name AND t.user_id = project_commits.author_id
        AND project_commits.verified_date <= t.start_issue AND project_commits.verified_date > t.half_year_before
    GROUP BY t.issue_id, t.user_id, t.start_issue, t.half_year_before, issue_threads.project_name) t2
LEFT JOIN project_commits ON t2.project_name = project_commits.project_name AND t2.user_id = project_commits.author_id
    AND project_commits.verified_date <= t2.start_issue
GROUP BY t2.issue_id, t2.project_name, t2.user_id, t2.start_issue, t2.half_year_before, t2.commitamount_last_half;


