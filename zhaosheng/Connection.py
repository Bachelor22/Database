import pyodbc

class DBConnection:
    @staticmethod
    def get_connection():
        # 配置 SQL Server 连接字符串
        connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=keshe;'  # 你的数据库名称
            'UID=sa;'           # SQL Server 用户名
            'PWD=123456'        # SQL Server 密码
        )
        connection = pyodbc.connect(connection_string)
        return connection
