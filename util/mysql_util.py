# -*- coding: utf-8 -*-
"""
@File    : mysql_util.py
@Time    : 2022/12/28 22:44
@Author  : 欧振宇
"""
import pymysql


class MySqlUtil:

    def __init__(self, host, port, database, charset, user, password):

        self.conn = pymysql.connect(host=host,
                                    port=port,
                                    database=database,
                                    charset=charset,
                                    user=user,
                                    password=password)
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        self.cur.close()
        self.conn.close()

    # 查询SQL
    def select_db(self, sql):
        self.cur.execute(sql)
        datas = self.cur.fetchall()
        return datas

    # 更新SQL
    def update_db(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print("操作出现错误:{}".format(e))
            self.conn.rollback()

    # 插入SQL
    def insert_db(self, sql, val):
        try:
            self.cur.executemany(sql, val)
            self.conn.commit()
        except Exception as e:
            print("操作出现错误:{}".format(e))
            self.conn.rollback()
        # finally:
        #     self.cur.close()
        #     self.conn.close()
