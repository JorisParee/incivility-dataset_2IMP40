#Simple query counting amount of commits prevous of issue
SELECT t.issue_id, t.project_name, t.start_date, COUNT(project_commits.id) FROM
(SELECT issue_threads.issue_id, issue_threads.project_name, min(comments.created_at) as start_date FROM issue_threads
LEFT JOIN comments ON comments.issue_id = issue_threads.issue_id
GROUP BY issue_threads.issue_id, issue_threads.project_name) t
LEFT JOIN project_commits ON project_commits.project_name = t.project_name AND project_commits.verified_date < t.start_date
GROUP BY t.issue_id, t.project_name, t.start_date


#Double query for calculating both half year commits and alltime commits before issue start
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
GROUP BY t2.issue_id, t2.project_name, t2.start_date, t2.half_year_before, t2.commits_before


#Query for calculating per distinct user that has posted comments how many commits they have in the project
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
GROUP BY t2.issue_id, t2.project_name, t2.user_id, t2.start_issue, t2.half_year_before, t2.commitamount_last_half


