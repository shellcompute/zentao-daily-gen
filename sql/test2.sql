SELECT
B.finishedBy AS finished_guy,
C.name AS sprint_title, 
D.name AS module_title, 
GROUP_CONCAT(DISTINCT B.closedBy SEPARATOR ',') AS closed_guy,
SUM(IF(estimate > 0, `estimate`, A.consumed)) AS consumed
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
GROUP BY finished_guy, sprint_title, module_title
