import psycopg2
import pprint
DBNAME = "news"


def mostPopularArticle():
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    # created view "logpath" and aggregate count
    # by path (article)
    c.execute(
        "CREATE VIEW  logpath AS "
        "SELECT path, count(*) AS num "
        "FROM log "
        "WHERE path LIKE '/article%' "
        "GROUP BY path "
        "ORDER BY num desc LIMIT 10;")
    # combined "logpath" with "articles" where the
    # slug was similiar to log.path
    c.execute(
        "SELECT articles.title, logpath.num "
        "FROM articles, logpath "
        "WHERE substring(logpath.path from 10) LIKE articles.slug "
        "LIMIT 3;")
    print(
        "\nTop three articles of all time, "
        "and corresponding views:")
    pprint.pprint(c.fetchall())
    db.close()


def mostPopularAuthor():
    # initialize database
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    c.execute(
        "SELECT authors.name, count(*) AS num "
        "FROM articles, authors, log "
        "WHERE substring(log.path from 10) LIKE articles.slug "
        "AND articles.author = authors.id "
        "GROUP BY authors.name "
        "ORDER BY num DESC;")
    print(
        "\nMost popular article authors of all time, "
        "and corresponding article views:")
    pprint.pprint(c.fetchall())
    db.close()


def percentErrorByDay():
    # initialize database
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    # created view "total" that does an aggregate count of all entries
    # grouped by day
    c.execute(
        "CREATE VIEW total AS "
        "SELECT time::date, count(*) AS num "
        "FROM log "
        "GROUP BY time::date;")
    # create another view "errors" which gives the aggregate count
    # of all log entries with status code containing 404, grouped by day
    c.execute(
        "CREATE VIEW errors AS "
        "SELECT time::date, status, count(time::date) AS x "
        "FROM log "
        "WHERE status LIKE '%404%' "
        "GROUP BY time::date, status "
        "ORDER BY time::date;")
    # joins views "total" and "errors" and calculates a percent
    # (404 entries per day)/(total entries that day)*100 = percent
    c.execute(
        "SELECT errors.time::date, "
        "errors.x::float / total.num::float * 100 "
        "FROM errors, total "
        "WHERE errors.time::date = total.time::date "
        "AND (errors.x::float / total.num::float * 100) > 1.0;")
    print(
        "\nDays in which more than 1% "
        "of requests led to errors:")
    pprint.pprint(c.fetchall())
    db.close()


mostPopularArticle()
mostPopularAuthor()
percentErrorByDay()
