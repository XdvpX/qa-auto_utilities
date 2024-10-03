import cx_Oracle
import pyodbc
from cx_Oracle import SessionPool
from pymysql import Error
from pymysql.constants import CLIENT
from pymysqlpool import ConnectionPool
from psycopg_pool import ConnectionPool as PstgConnectionPool


class DatabaseHelper:
    """
    Utility class for performing database operations on SQL Server, MySQL, Oracle, and PostgreSQL databases.

    Example:
        To access results:

        >>> results = run_oracle_query('query', SessionPool(), False)
        >>> results[0]
        First row of results

        >>> results[0][0]
        First row, first column of the results

        >>> results[2][3]
        Third row, fourth column of the results
    """

    @classmethod
    def setup_mysql_pool(cls, username: str, pwd: str, host_url: str):
        """
        Initializes MySQL connection pool.

        Args:
            username: MySQL username
            pwd: MySQL password
            host_url: Host for the database

        Returns:
            Connection pool object for MySQL
        """
        cls.mysql_pool = ConnectionPool(
            user=username,
            password=pwd,
            host=host_url,
            size=2,
            maxsize=4,
            client_flag=CLIENT.MULTI_STATEMENTS,
            autocommit=True
        )
        return cls.mysql_pool

    @classmethod
    def setup_oracle_pool(cls, username: str, pwd: str, dsn_string: str):
        """
        Initializes Oracle connection pool.

        Args:
            username: Oracle username
            pwd: Oracle password
            dsn_string: Oracle connection string (DSN)

        Returns:
            Oracle connection pool
        """
        cls.oracle_pool = SessionPool(
            user=username,
            password=pwd,
            dsn=dsn_string,
            min=1,
            max=4,
            increment=1
        )
        return cls.oracle_pool

    @classmethod
    def setup_postgres_pool(cls, username: str, pwd: str, host_url: str, dbname: str, port_num: str):
        """
        Initializes PostgreSQL connection pool.

        Args:
            username: PostgreSQL username
            pwd: PostgreSQL password
            host_url: Hostname for the PostgreSQL server
            dbname: Database name
            port_num: Port number

        Returns:
            PostgreSQL connection pool
        """
        connection_info = f"user={username} password={pwd} host={host_url} dbname={dbname} port={port_num}"
        cls.postgres_pool = PstgConnectionPool(
            conninfo=connection_info,
            min_size=1,
            max_size=4
        )
        return cls.postgres_pool

    @classmethod
    def run_mysql_query(cls, query: str, pool: ConnectionPool, apply_commit: bool = False):
        """
        Executes a query on MySQL using connection pool.

        Args:
            query: SQL query to execute
            pool: MySQL connection pool object
            apply_commit: If set, commits the transaction

        Returns:
            Query result or row count based on `apply_commit` flag
        """
        conn = None
        cur = None
        try:
            conn = pool.get_connection()
            cur = conn.cursor()
            cur.execute(query)

            if apply_commit:
                conn.commit()
                return cur.rowcount
            else:
                return cur.fetchall()
        except Error as e:
            print("MySQL Pool Error: ", e)
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def run_oracle_query(cls, query: str, pool: SessionPool, apply_commit: bool = False):
        """
        Executes a query on Oracle using connection pool.

        Args:
            query: SQL query to execute
            pool: Oracle connection pool object
            apply_commit: If set, commits the transaction

        Returns:
            Query result or row count based on `apply_commit` flag
        """
        conn = None
        cur = None
        try:
            conn = pool.acquire()
            cur = conn.cursor()

            conn.outputtypehandler = cls.__oracle_data_handler

            cur.execute(query)
            if apply_commit:
                conn.commit()
                return cur.rowcount
            else:
                return cur.fetchall()
        except cx_Oracle.Error as e:
            print("Oracle Pool Error: ", e)
        finally:
            if cur:
                cur.close()
            if conn:
                pool.release(conn)

    @classmethod
    def run_sql_server_query(cls, query: str, username: str, pwd: str, srv_name: str, db_name: str, apply_commit: bool = False):
        """
        Executes a query on SQL Server.

        Args:
            query: SQL query to execute
            username: SQL Server username
            pwd: SQL Server password
            srv_name: Server name
            db_name: Database name
            apply_commit: If set, commits the transaction

        Returns:
            Query result or row count based on `apply_commit` flag
        """
        conn = None
        cur = None
        try:
            conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={srv_name};DATABASE={db_name};UID={username};PWD={pwd}')
            cur = conn.cursor()
            cur.execute(query)

            if apply_commit:
                conn.commit()
                return cur.rowcount
            else:
                return cur.fetchall()
        except pyodbc.Error as e:
            print("SQL Server Error: ", e)
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def run_postgres_query(cls, query: str, pool: PstgConnectionPool, apply_commit: bool = False):
        """
        Executes a query on PostgreSQL using connection pool.

        Args:
            query: SQL query to execute
            pool: PostgreSQL connection pool object
            apply_commit: If set, commits the transaction

        Returns:
            Query result or row count based on `apply_commit` flag
        """
        conn = None
        cur = None
        try:
            conn = pool.getconn()
            cur = conn.cursor()
            cur.execute(query)

            if apply_commit:
                conn.commit()
                return cur.rowcount
            else:
                return cur.fetchall()
        except Exception as e:
            print(f'PostgreSQL Pool Error: {e}')
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def __oracle_data_handler(cls, cur, name, default_type, size, precision, scale):
        """
        Custom output type handler for Oracle CLOB/BLOB data types.
        """
        if default_type == cx_Oracle.CLOB:
            return cur.var(cx_Oracle.LONG_STRING, arraysize=cur.arraysize)
        elif default_type == cx_Oracle.BLOB:
            return cur.var(cx_Oracle.LONG_BINARY, arraysize=cur.arraysize)
