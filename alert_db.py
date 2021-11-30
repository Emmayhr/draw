# -*- coding: utf-8 -*-
# @Author   :   kk
# @File     :   db.py
# @Time     :   2021/11/12

import os
import sys
from peewee import *
import datetime
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))


#### 这个是10.10.103.85数据库的表模型文件
# 连接数据库
class RetryMySQLDatabase2(ReconnectMixin, PooledMySQLDatabase):
    _instance = None

    @staticmethod
    def get_db_instance():
        if not RetryMySQLDatabase2._instance:
            RetryMySQLDatabase2._instance = RetryMySQLDatabase2(
                'multislice',
                max_connections=300,
                stale_timeout=300,
                user='root',
                password="mm123456",
                host="10.10.103.150",
                # host='sh-cynosdbmysql-grp-rqp9kexm.sql.tencentcdb.com',
                port=3306,
            )
        return RetryMySQLDatabase2._instance


database = RetryMySQLDatabase2.get_db_instance()


# database = PooledMySQLDatabase(
#             '5gesp_backend_database',
#             max_connections=100,
#             stale_timeout=300,
#             user='root',
#             password="mm123456",
#             host='10.10.103.85',
#             port=3306,
#             ping=1
#             )

class Alert(Model):
    """
    alert表:包含了
    """
    timestamp = DateTimeField(default=datetime.datetime.now)
    sig_id = IntegerField()
    msg = CharField(1024)
    category = CharField()
    severity = IntegerField()

    '''--- trans_layer ---'''
    transport_protocol = CharField()
    ip_src = CharField()
    src_port = IntegerField()
    ip_dst = CharField()
    dst_port = IntegerField()

    icmp_type = IntegerField()
    icmp_code = IntegerField()

    '''--- flow ---'''
    flow_id = CharField()
    pkts_toserver = IntegerField()
    pkts_toclient = IntegerField()
    bytes_toserver = IntegerField()
    bytes_toclient = IntegerField()

    '''--- app_layer ---'''
    app_proto = CharField()

    smtp_helo = CharField()

    http_host_name = CharField()
    http_url = CharField(1024)
    http_user_agent = CharField()
    http_content_type = CharField()
    http_refer = CharField()
    http_method = CharField()
    http_proto = CharField()
    http_status = IntegerField()
    http_length = IntegerField()

    dns_type = CharField()
    dns_id = IntegerField()
    dns_rrname = CharField()
    dns_rrtype = CharField()
    dns_tx_id = CharField()

    dns_answer_flags = CharField()
    dns_answer_qr = BooleanField()
    dns_answer_rd = BooleanField()
    dns_answer_ra = BooleanField()
    dns_answer_rcode = CharField()
    dns_answer_ttl = IntegerField()
    dns_answer_rdata = CharField()

    ftp_data_filename = CharField()
    ftp_data_command = CharField()

    smb_id = IntegerField()
    smb_dialect = CharField()
    smb_command = CharField()
    smb_status = CharField()
    smb_status_code = CharField()
    smb_session_id = IntegerField()
    smb_tree_id = IntegerField()
    smb_client_dialects = CharField(1024)
    smb_server_guid = CharField()

    ssh_client_proto_version = CharField()
    ssh_client_software_version = CharField()
    ssh_server_proto_version = CharField()
    ssh_server_software_version = CharField()

    tls_subject = CharField(1024)
    tls_issuer = CharField(1024)
    tls_serial = CharField(1024)
    tls_fingerprint = CharField(1024)
    tls_version = CharField()
    tls_notbefore = DateTimeField()
    tls_notafter = DateTimeField()
    tls_ja3_hash = CharField()
    tls_ja3_string = CharField(1024)
    tls_ja3s_hash = CharField()
    tls_ja3s_string = CharField(1024)

    dataset = CharField()

    class Meta:
        database = database
        table_name = "homemade_bomb_copy1"


if __name__ == "__main__":
    Alert.create_table()
    print("table alert has been created successfully")
