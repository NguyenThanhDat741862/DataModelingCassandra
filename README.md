# Sparkify Cassandra ETL

## Table of Contents

- [Introduction](#introduction)
- [Context](#context)
- [Questions](#questions)
- [Structure](#structure)
- [Usage](#usage)
- [Result](#result)

## Introduction

This project is based on the second project in [Udacity Data Engineering Nanodegree Program](https://www.udacity.com/course/data-engineer-nanodegree--nd027) course.

The aims of this project are:

- Practice using CQL to query with Cassandra.

- Learn how to build a simple ETL pipeline using Python.

- Learn how to setup simple Cassandra Cluster in Docker containers.

- Learn how to use Makefile in Python project.

## Context

Complete an ETL pipeline that transfers data from a set of CSV files to Cassandra Cluster using Python.

Create queries to ask the following three questions of the data.

## Questions

- Question 1

```
  Find the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession = 4
```

- Question 2

```
  Find only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182
```

- Question 3

```
  Find every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'
```

## Structure

```
📦DataModelingCassandra
 ┣ 📂project
 ┃ ┣ 📂config
 ┃ ┃ ┣ 📜config.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂db
 ┃ ┃ ┣ 📜db.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂etl
 ┃ ┃ ┣ 📜etl.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂helper
 ┃ ┃ ┣ 📜helper.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂logger
 ┃ ┃ ┣ 📜logger.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂logs
 ┃ ┃ ┣ 📜DB.log
 ┃ ┃ ┣ 📜ETL.log
 ┃ ┃ ┗ 📜TASK.log
 ┃ ┣ 📂resources
 ┃ ┃ ┗ 📂data
 ┃ ┣ 📂results
 ┃ ┃ ┣ 📜Task_01.csv
 ┃ ┃ ┣ 📜Task_02.csv
 ┃ ┃ ┗ 📜Task_03.csv
 ┃ ┣ 📂task
 ┃ ┃ ┣ 📜task.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂temp
 ┃ ┃ ┗ 📜staging.csv
 ┃ ┣ 📜config.ini
 ┃ ┣ 📜config.template.ini
 ┃ ┣ 📜main.py
 ┃ ┗ 📜Pipfile
 ┣ 📂setup
 ┃ ┣ 📂docker
 ┃ ┃ ┣ 📂config
 ┃ ┃ ┃ ┗ 📜cassandra.yml
 ┃ ┃ ┗ 📂volumes
 ┃ ┃ ┃ ┣ 📂cassandra_data_node
 ┃ ┃ ┃ ┗ 📂cassandra_data_seed
 ┃ ┗ 📜docker-compose.yml
 ┣ 📜.gitignore
 ┣ 📜Makefile
 ┗ 📜README.md
```

## Usage

1. Clone repository

```
  git clone 
```

2. Run Cassandra cluster in Docker containers

```
  make start-cluster
```

3. Setup virtual env for project

```
  make setup-env
```

4. Run project

```
  make run
```

## Result

- Can be found in result folder ( ./project/result ).
