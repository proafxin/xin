from enum import Enum


class SQLDatabaseDialect(str, Enum):
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    SQLSERVER = "mssql"


class SQLDatabaseDriver(str, Enum):
    AIOMYSQL = "aiomysql"
    ASYNCPG = "asyncpg"
    PYMSSQL = "pymssql"


class NoSQLDatabaseDialect(str, Enum):
    MONGODB = "mongodb"
    SCYLLADB = "scylladb"
    CASSANDRA = "cassandra"


class NoSQLDatabaseDriver(Enum):
    MOTOR = "motor"


SQL_DRIVERS = {
    SQLDatabaseDialect.MYSQL.value: SQLDatabaseDriver.AIOMYSQL.value,
    SQLDatabaseDialect.POSTGRESQL.value: SQLDatabaseDriver.ASYNCPG.value,
    SQLDatabaseDialect.SQLSERVER.value: SQLDatabaseDriver.PYMSSQL.value,
}

NOSQL_DRIVERS = {NoSQLDatabaseDialect.MONGODB.value: NoSQLDatabaseDriver.MOTOR.value}
