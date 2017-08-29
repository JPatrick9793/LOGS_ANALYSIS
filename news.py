#!/usr/bin/env python3
import psycopg2
import pprint
DBNAME = "news"


def get_query_results(query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


def mostPopularArticle():
    # uses view "logpath"
    query = (
        "SELECT articles.title, logpath.num "
        "FROM articles, logpath "
        "WHERE substring(logpath.path from 10) = articles.slug "
        "ORDER BY num desc "
        "LIMIT 3;")
    result = get_query_results(query)
    print(
        "\nTop three articles of all time, "
        "and corresponding views:")
    for title, views in result:
        print("    {} -- {} views".format(title, views))


def mostPopularAuthor():
    query = (
        "SELECT authors.name, count(*) AS num "
        "FROM articles, authors, log "
        "WHERE articles.author = authors.id "
        "GROUP BY authors.name "
        "ORDER BY num DESC;")
    result = get_query_results(query)
    print(
        "\nMost popular article authors of all time, "
        "and corresponding article views:")
    for name, views in result:
        print("    {} -- {} views".format(name, views))


def percentErrorByDay():
    # joins views "total" and "errors" and calculates a percent
    # (404 entries per day)/(total entries that day)*100 = percent
    query = (
        "SELECT to_char(errors.time::date, 'FMMonth FMDD, YYYY'), "
        "ROUND(errors.x::decimal / total.num::decimal * 100, 2) "
        "FROM errors, total "
        "WHERE errors.time::date = total.time::date "
        "AND (errors.x::float / total.num::float * 100) > 1.0 "
        "ORDER BY errors.time::date;")
    result = get_query_results(query)
    print(
        "\nDays in which more than 1% "
        "of requests led to errors:")
    for date, percent in result:
        print("    {} -- {}%".format(date, percent))


if __name__ == "__main__":
    mostPopularArticle()
    mostPopularAuthor()
    percentErrorByDay()
