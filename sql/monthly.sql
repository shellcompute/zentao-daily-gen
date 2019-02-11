-- 统计某产品本月份完成需求消耗的时间
SELECT ROUND(SUM(A.consumed),1) AS consumed 
FROM zt_taskestimate AS A
LEFT JOIN zt_task AS B
ON A.task = B.id
LEFT JOIN zt_story AS C
ON B.story = C.id
WHERE A.date >= '2019-01-01' AND A.date <= '2019-01-31'
AND A.account IN (
'Leon', 'Mark', 'Drew', 'Acker', 'Linugy', 'Harrison', 'Abby',
'Jay', 'Hum', 'Anna', 'Amanda',
'Fly', 'John', 'Eddie', 'Aimee', 'Jerry'
)
AND C.product = 3 
-- 统计某迭代本月份修复BUG消耗的时间
SELECT ROUND(SUM(A.consumed),1) AS consumed 
FROM zt_taskestimate AS A
LEFT JOIN zt_task AS B
ON A.task = B.id
LEFT JOIN zt_bug AS C
ON B.fromBug = C.id 
WHERE A.date >= '2019-01-01' AND A.date <= '2019-01-31'
AND C.product = 1
--统计某产品本月份修复的BUG个数
SELECT COUNT(*)
FROM zt_bug
WHERE resolvedDate >= '2019-01-01' AND resolvedDate <= '2019-01-31'
AND resolvedBy IN (
'Leon', 'Mark', 'Drew', 'Acker', 'Linugy', 'Harrison', 'Abby',
'Jay', 'Hum', 'Anna', 'Amanda',
'Fly', 'John', 'Eddie', 'Aimee', 'Jerry'
)
AND product = 1
-- 统计其他项目本月份完成需求消耗的时间
SELECT ROUND(SUM(A.consumed),1) AS consumed 
FROM zt_taskestimate AS A
LEFT JOIN zt_task AS B
ON A.task = B.id
LEFT JOIN zt_story AS C
ON B.story = C.id
WHERE A.date >= '2019-01-01' AND A.date <= '2019-01-31'
AND A.account IN (
'Leon', 'Mark', 'Drew', 'Acker', 'Linugy', 'Harrison', 'Abby',
'Jay', 'Hum', 'Anna', 'Amanda',
'Fly', 'John', 'Eddie', 'Aimee', 'Jerry'
)
AND C.product NOT IN (1, 3, 5, 17, 26, 32, 40, 47, 53)