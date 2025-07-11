import pymysql
from contextlib import contextmanager

import yaml


#获取数据库信息
@contextmanager
def get_data_context(path):
    config = {}
    try:
        with open(path, 'r') as stream:
            config = yaml.safe_load(stream)
            yield config
    except FileNotFoundError:
        print(f"配置文件{path}未找到")
        yield {}
    except yaml.YAMLError as exc:
        print(f'Yaml解析失败{path}')
        yield {}



#配置数据库连接
#@contextmanger允许你更简单方式来实现with的语句，支持的功能，
@contextmanager
def get_db():
    conn = None
    with get_data_context('./config.yaml') as config:
        db = config.get('database',{})
    try:
        conn = pymysql.connect(
            user= db.get('user'),
            password= db.get('password'),
            host= db.get('host'),
            database= db.get('name'),
            port=db.get('port'),
            charset= db.get('charset'),
            cursorclass = pymysql.cursors.DictCursor,
            autocommit=True
        )
        yield conn
    except pymysql.MySQLError as e:
        print(f"数据库无法连接{e}")
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                print(f"数据库关闭失败 {e}")

if __name__ == '__main__':
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("select * from machinepower")
            result = cursor.fetchall()
            print(result)