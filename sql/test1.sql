SELECT A.task AS task_id, 
C.name AS sprint_title, 
D.name AS module_title, 
B.name AS task_title, 
B.story,
B.finishedBy,
B.closedBy,
B.finishedDate,
B.closedDate,
B.estimate,
A.consumed, 
B.left
FROM (
	SELECT task, account, ROUND(SUM(consumed),1) AS consumed
	FROM zt_taskestimate
	WHERE date >= '2019-01-07' AND date <= '2019-01-13'
	AND account IN ('Kurri', 'Stan', 'Shyer', 'Jarvis', 'Mike', 'Bell', 'Lethe',
	'Alan', 'Rookey', 'Nicholas', 'Billy')
	GROUP BY task, account
) A
LEFT JOIN zt_task B ON A.task = B.id
LEFT JOIN zt_project C ON B.project = C.id
LEFT JOIN zt_module D ON B.module = D.id
WHERE B.status = 'closed'
ORDER BY A.task ASC

