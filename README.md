# Xin

A pydantic powered universal ORM wrapper for databases.

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/proafxin/xin/develop.svg)](https://results.pre-commit.ci/latest/github/proafxin/xin/develop)
[![Build, Test and Publish](https://github.com/proafxin/xin/actions/workflows/cicd.yaml/badge.svg)](https://github.com/proafxin/xin/actions/workflows/cicd.yaml)
[![codecov](https://codecov.io/gh/proafxin/xin/graph/badge.svg?token=p2cOg8tQMb)](https://codecov.io/gh/proafxin/xin)
[![Documentation Status](https://readthedocs.org/projects/xin/badge/?version=latest)](https://xin.readthedocs.io/en/latest/?badge=latest)

## Features

* Execute queries on a database.
* Read a database table as a dataframe.
* Write a dataframe to a database table (still under development).
* Flatten and normalize a dataframe with nested structure.
* Serialize a dataframe as a list of pydantic models.
* Deserialize a list of pydantic models as a dataframe.

The primary backend for parsing dataframes is [polars](https://pola.rs/) due to it's superior [performance](https://pola.rs/_astro/perf-illustration.jHjw6PiD_165TDG.svg). `Xin` supports pandas dataframes as well, however, they are internally converted to polars dataframes first to not compromise performance.

The backend  for interacting with SQL databases is [sqlalchemy](https://www.sqlalchemy.org/) because it supports async features and is the de-facto standard for communicating with SQL databases.

## Databases Supported

* MySQL
* PostgreSQL
* SQL Server
* Mongodb

## Async Drivers Supported

`Xin` is async first. It means that if an async driver is available for a database dialect, it will leverage the async driver for better performance when  applicable. SQL Server driver PyMSSQL does not have an async variation yet.

* Motor for Mongodb
* Asyncpg for PostgreSQL
* AioMySQL for MySQL

## Plan for Future Database Support

* Scylladb
* Apache Cassandra
