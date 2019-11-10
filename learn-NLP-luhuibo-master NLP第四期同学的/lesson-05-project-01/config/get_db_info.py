#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/9/3 10:44
@Desc   ：读取数据库配置yaml文件
=================================================='''

import logging
import logging.config
import os
import yaml


class GetConfParams:
    # 这里填下同一文件夹下的.conf文件
    log_path = os.path.join(os.path.dirname(__file__) + '/logging.ini')
    logging.config.fileConfig(log_path)

    def __init__(self):
        # 这里填下同一文件夹下的.yaml文件
        yaml_path = os.path.join(os.path.dirname(__file__) + '/databases.yaml')

        # 打开yaml文件
        stream = open(yaml_path, 'r', encoding='utf-8')
        params = yaml.load(stream, Loader=yaml.FullLoader)

        # 设置日志
        self.logger = logging.getLogger('root')

        # 设置数据库的连接地址、端口号、数据库名、用户名、密码
        self.user = params['database_conf']['user']
        self.password = params['database_conf']['password']
        self.host = params['database_conf']['host']
        self.port = params['database_conf']['port']

        # 设置charset为中文，有时候读取到的数据是乱码
        self.charset = params['database_conf']['charset']

        # 连接的数据库
        self.db_name = params['database_conf']['db_name']
        # 连接的表
        self.table_name = params['database_conf']['table_name']


if __name__ == "__main__":
    # 对上面代码进行测试
    get_db = GetConfParams()
    print(get_db.user)
    print(get_db.password)
    print(get_db.host)
    print(get_db.port)
    print(get_db.user)
    print(get_db.charset)
    print(get_db.db_name)
    print(get_db.table_name)
