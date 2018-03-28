#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 2017/08/27
# Email：
import xlwt
import pymysql
import time


class MysqlOperation(object):
    def __init__(self, mysql_servers_ip, mysql_user, mysql_passwd, mysql_port, mysql_db_name):
        self.mysql_servers_ip = mysql_servers_ip
        self.mysql_user = mysql_user
        self.mysql_passwd = mysql_passwd
        self.mysql_port = mysql_port
        self.mysql_db_name = mysql_db_name

    def mysql_connet(self):
        """
            数据库连接
            : return: 连接实例
        """
        try:
            db = pymysql.connect(self.mysql_servers_ip,
                                 self.mysql_user,
                                 self.mysql_passwd,
                                 self.mysql_db_name,
                                 port=self.mysql_port,
                                 charset='utf8')
            return db
        except Exception as e:
            print(e)

    def mysql_select_tabel(self, opet_sql, opet_result="name"):
        """
            数据库查询操作
            : param opet_sql: 需要查询的sql语句
            : opet_result: one 代表通过fetchone方法（默认）， all 代表fetchall方法 , name 代表查询表名
            : return: 查询结果 或 False
        """
        # fetchone 方法获取下一个查询结果集。结果集是一个对象
        # fetchall 方法接收全部的返回结果行
        # rowcount 方法是一个只读属性，并返回执行execute()方法后影响的行数
        results = False
        db = self.mysql_connet()
        cursor = db.cursor()
        try:
            # print "查询到的行数: ", cursor.execute(opet_sql)
            cursor.execute(opet_sql)
            # 来重置游标的位置 absolute：绝对位置  relative：相对位置
            cursor.scroll(0, mode='absolute')
            if opet_result == "all":
                results = cursor.fetchall()
            elif opet_result == "name":
                # 获取MYSQL里面的数据字段名称,不要加()
                results = cursor.description
            else:
                results = cursor.fetchone()
        except Exception as e:
            print(e)
        db.close()
        return results

    def mysql_opet_table(self, opet_sql, opet=""):
        """
            创建数据库表
            : param opet_sql: 创建表的sql语句
            : param opet: 对应操作,如 create、insert、update、drop
            : return: True or False
        """
        result = False
        db = self.mysql_connet()
        cursor = db.cursor()
        if opet == "create":
            try:
                cursor.execute("DROP TABLE IF EXISTS %s" % (opet_sql[13:opet_sql.index("(") - 1]))
                cursor.execute(opet_sql)
                result = True
            except Exception as e:
                print(e)
        else:
            try:
                cursor.execute(opet_sql)
                db.commit()
                result = True
            except Exception as e:
                print(e)
                db.rollback()
        db.close()
        return result


class ExcelOperation(object):
    def __init__(self, excel_sheet_name, excel_save_path):
        self.excel_sheet_name = excel_sheet_name
        self.excel_save_path = excel_save_path

    def excel_insert(self, excel_column_name, excel_content):
        """
            保存内容为excel，临时
            : param excel_column_name: 列名
            : param excel_content: 需要保存的内容
            : return: False or True
        """
        result = False
        try:
            workbook = xlwt.Workbook(encoding='utf-8')  # workbook是sheet赖以生存的载体。
            sheet = workbook.add_sheet(self.excel_sheet_name, cell_overwrite_ok=True)
            # 第一行写上名称
            for field in range(0, len(excel_column_name)):
                sheet.write(0, field, excel_column_name[field][0])
            # 获取并写入数据段信息
            row = 1
            col = 0
            for row in range(1, len(excel_content) + 1):
                for col in range(0, len(excel_content)):
                    sheet.write(row, col, u'%s' % excel_content[row - 1][col])
            workbook.save(self.excel_save_path)
            result = True
        except Exception as e:
            print(e)
        return result


# 主函数
if __name__ == "__main__":
    SERVERS_IP = "192.168.78.135"
    MYSQL_USER = "root"
    MYSQL_PASSWD = "123456"
    MYSQL_PORT = 3306
    MYSQL_DB_NAME = "xh"
    sql = "select * from user_copy;"
    sql1 = "show create table user;"
    insertsql = "insert into user(name,passwd,phone,remark) values('test2','afdas','sadfe','ewrfasc');"
    # excel 文件相关参数
    # excel 工作表名称
    sheet_name = "sheetName" + time.strftime("%Y-%m-%d")
    out_path = 'D:\\project2\\file\\' + time.strftime("%Y-%m-%d") + '.xls'

    print("主程序开始")
    # export()

    my = MysqlOperation(SERVERS_IP, MYSQL_USER, MYSQL_PASSWD, MYSQL_PORT, MYSQL_DB_NAME)
    one = my.mysql_select_tabel(sql, "one")
    if one:
        print("数据查询成功")
        # 获取表名
        name = my.mysql_select_tabel(sql, "name")
        # 获取全部数据
        all_result = my.mysql_select_tabel(sql, "all")
        print(len(all_result))
        # 实例化excel
        excel = ExcelOperation(sheet_name, out_path)
        # 写入数据
        print("开始保存数据")
        e = excel.excel_insert(name, all_result)
        if e:
            print("保存数据成功")
        else:
            print("保存数据失败")
    else:
        print("数据查询失败")

    # print r
    # for i in range(1, 10000):
    #     insertsql = "insert into user(name,passwd,phone,remark) values('test%d','afdas','sadfe','ewrfasc');" % i
    #     r = my.mysql_opet_table(insertsql, "insert")
    #     if r:
    #         print "插入数据成功, %d" %i
    #     else:
    #         print "失败 %d" %i




