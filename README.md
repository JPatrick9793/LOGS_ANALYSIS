CREATED BY JOHN CONWAY, AS PART OF THE UDACITY FULLSTACK NANODEGREE PROGRAM

This is a python program acts as an internal reporting tool and will print the results of PostgreSQL queries designed to answer three questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


In order to use this program, you must have Python (v 3.5.2 current) and PostgreSQL (v 9.5.8 current). Previous versions may not be compatible:
    Python: https://www.python.org/downloads/
    PostgreSQL: https://www.postgresql.org/download/


This program was designed on Vagrant (linux-operating system VM), installed using VirtualBox; both can be installed following these URIs:
    Vagrant: https://www.vagrantup.com/
    VirtualBox: https://www.virtualbox.org/wiki/Downloads


This program also uses a file "newsdata.sql" which can be downloaded from the following link. Unzip this file after downloading it (and place into the vagrant directory, if using vagrant):
    https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

    
To load the database, enter the following command:
    $ psql -d news -f newsdata.sql


This program is run from the command line; place all files within the same directory and from the command line, type the command: 
	$ python3 news.py


The following views are to be created once the database is loaded:

	    CREATE VIEW  logpath AS
        	SELECT path, count(*) AS num
        	FROM log
        	WHERE path LIKE '/article%'
            AND status = '200 OK'
            GROUP BY path;

	    CREATE VIEW total AS
            SELECT time::date, count(*) AS num
            FROM log
            GROUP BY time::date;

        CREATE VIEW errors AS
            SELECT time::date, count(time::date) AS x
            FROM log
            WHERE status LIKE '%404%'
            GROUP BY time::date;
