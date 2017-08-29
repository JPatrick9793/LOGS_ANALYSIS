CREATED BY JOHN CONWAY, AS PART OF THE UDACITY FULLSTACK NANODEGREE PROGRAM

This is a python program acts as an internal reporting tool and will print the results of PostgreSQL queries designed to answer three questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

This program is run from the command line; place all files within the same directory and from the command line, type the command: 
	$ python3 news.py

The following views are created (within the program itself), but are re-written here for clarity:

		CREATE VIEW  logpath AS
        	SELECT path, count(*) AS num
        	FROM log
        	WHERE path LIKE '/article%'
        	GROUP BY path
        	ORDER BY num desc LIMIT 10;

		CREATE VIEW total AS
        	SELECT time::date, count(*) AS num
        	FROM log
        	GROUP BY time::date;

        CREATE VIEW errors AS "
        	SELECT time::date, status, count(time::date) AS x
        	FROM log
        	WHERE status LIKE '%404%'
        	GROUP BY time::date, status
        	ORDER BY time::date;
