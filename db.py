#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Created by yhr at Beijing in june
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
                #host='sh-cynosdbmysql-grp-rqp9kexm.sql.tencentcdb.com',
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

class Frame(Model):
    """
    frame表:包含了
    """
    position = IntegerField()
    timestamp = DoubleField()
    frame_length = IntegerField()
    ip_src = CharField()
    ip_dst = CharField()
    src_mac = CharField()
    dst_mac = CharField()
    app_protocol = CharField()
    net_protocol = CharField()
    transport_protocol = CharField()
    src_port = CharField()
    dst_port = CharField()
    dns_host = CharField()
    dns_query_name = CharField(1024)
    dns_query_name_len = IntegerField()
    dns_query_type  = CharField()
    tcp_seq_raw  = CharField()
    tcp_nxtseq = CharField()
    tcp_ack = CharField()
    tcp_ack_raw = CharField()
    tcp_flag  = CharField()
    http_uri  = CharField(1024)
    http_host = CharField(1024)
    http_user_agent = CharField(1024)
    http_method = CharField()
    flag = CharField()
    Id = AutoField(primary_key = True)
    class Meta:
        database = database



class Frameceil(Model):
    """
    frame表:包含了
    """
    down_time = DoubleField()
    rise_time = DoubleField()
    dev_id = CharField()
    traffic_id = IntegerField()
    timestamp = DoubleField()
    frame_length = IntegerField()
    ip_src = CharField()
    ip_dst = CharField()
    src_mac = CharField()
    dst_mac = CharField()
    app_protocol = CharField()
    net_protocol = CharField()
    transport_protocol = CharField()
    src_port = CharField()
    dst_port = CharField()
    position = IntegerField()
    dns_host = CharField()
    dns_query_name = CharField(1024)
    dns_query_name_len = IntegerField()
    dns_query_type  = CharField()
    tcp_seq_raw  = CharField()
    tcp_nxtseq = CharField()
    tcp_ack = CharField()
    tcp_ack_raw = CharField()
    tcp_flag  = CharField()
    http_uri  = CharField(1024)
    http_host = CharField(1024)
    http_user_agent = CharField(1024)
    http_method = CharField()
    Id = AutoField(primary_key = True)
    class Meta:
        database = database

class Port_feature(Model):
    '''
    port feature表，包含了
    '''
    ip  = CharField( default = "" )
    port = IntegerField( default = 0 )
    status = CharField( default = "rise" )
    dev_id  = CharField( default = "" )
    traffic_id  = CharField( default = "" )
    start_time = DoubleField( default = 0 )
    end_time = DoubleField( default = 0 )

    frame_num  = IntegerField( default = 0 )
    send_frame_num  = IntegerField( default = 0 )
    recv_frame_num  = IntegerField( default = 0 )
    send_frame_length  = BigIntegerField( default = 0 )
    recv_frame_length  = BigIntegerField( default = 0 )
    avr_send_length = FloatField( default = 0 )
    avr_recv_length = FloatField( default = 0 )
    interval  = FloatField( default = 0 )
    send_interval  = FloatField( default = 0 )
    recv_interval  = FloatField( default = 0  )
    send_throughput  = FloatField( default = 0 )
    recv_throughput  = FloatField( default = 0 )
    total_length  = BigIntegerField( default = 0 )
    app_protocol  = CharField( default = "" )
    seq_min  = IntegerField( default = -1 )
    seq_max  = IntegerField( default = -1 )
    windows = IntegerField( default = 0 )
    port_num = IntegerField( default = 0 )
    Id = AutoField(primary_key = True)
    class Meta:
        database = database




class Basic_feature(Model):
    '''
    basic feature表，包含了
    '''
    ip  = CharField( default = "" )
    status = CharField( default = "rise" )
    dev_id  = CharField( default = "" )
    traffic_id  = CharField( default = "" )
    start_time = DoubleField( default = 0 )
    end_time = DoubleField( default = 0 )
    continue_time = DoubleField( default = 0 )
    dst_ip_num = IntegerField( default = 0 )
    local_port_num = IntegerField( default = 0 )
    frame_num  = IntegerField( default = 0 )
    send_frame_num  = IntegerField( default = 0 )
    recv_frame_num  = IntegerField( default = 0 )
    interval  = FloatField( default = 0 )
    send_interval  = FloatField( default = 0 )
    recv_interval  = FloatField( default = 0 )
    local_port_set = CharField( default = "" )
    peer_port_set = CharField( default = "" )
    dst_ip_set = CharField( default = "" )
    windows = IntegerField( default = 0 )
    port_num = IntegerField( default = 0 )
    Id = AutoField(primary_key = True)
    class Meta:
        database = database



class Configure(Model):
    '''
    存储临时配置文件
    '''
    skip_page = IntegerField( default = 0 )
    page_limit = IntegerField( default = 0 )

    class Meta:
        database = database
  
class Similarity(Model):
    '''
    存储相似度计算字段
    '''
    ipa = CharField( default = '' )
    ipb = CharField( default = '' )
    start_time_A = DoubleField( default = 0 )
    end_time_A = DoubleField( default = 0 )
    start_time_B = DoubleField( default = 0 )
    end_time_B = DoubleField( default = 0 )
    dev_id_A = CharField( default = '' )
    traffic_id_A = IntegerField( default = 0 )
    dev_id_B = CharField( default = '' )
    traffic_id_B = IntegerField( default = 0 )
    distance = FloatField( default = 0 )
    d_basic =  FloatField( default = 0 )
    d_peer_port =  FloatField( default = 0 )
    d_dst_ip =  FloatField( default = 0 )
    d_local_port =  FloatField( default = 0 )
    d_ports = FloatField( default = 0 )
    dpp_max_len = IntegerField( default = 0 )
    dpp_repetition_num = IntegerField( default = 0 )
    ddi_max_len = IntegerField( default = 0 )
    ddi_repetition_num = IntegerField( default = 0 )
    dlp_max_len = IntegerField( default = 0 )
    dlp_repetition_num = IntegerField( default = 0 )
    ylabel = IntegerField( default = 0 )
    ypred = IntegerField( default = 0 )
    Id = AutoField(primary_key = True)
    windows = IntegerField( default = 0 )
    port_num = IntegerField( default = 0 )
    class Meta:
         database = database

class NNSimilarity(Model):
    '''
    存储相似度计算字段
    '''
    ipa = CharField( default = '' )
    ipb = CharField( default = '' )
    start_time_A = DoubleField( default = 0 )
    end_time_A = DoubleField( default = 0 )
    start_time_B = DoubleField( default = 0 )
    end_time_B = DoubleField( default = 0 )
    dev_id_A = CharField( default = '' )
    traffic_id_A = IntegerField( default = 0 )
    dev_id_B = CharField( default = '' )
    traffic_id_B = IntegerField( default = 0 )
    distance = FloatField( default = 0 )
    d_basic =  FloatField( default = 0 )
    d_peer_port =  FloatField( default = 0 )
    d_dst_ip =  FloatField( default = 0 )
    d_local_port =  FloatField( default = 0 )
    d_ports = FloatField( default = 0 )
    dpp_max_len = IntegerField( default = 0 )
    dpp_repetition_num = IntegerField( default = 0 )
    ddi_max_len = IntegerField( default = 0 )
    ddi_repetition_num = IntegerField( default = 0 )
    dlp_max_len = IntegerField( default = 0 )
    dlp_repetition_num = IntegerField( default = 0 )
    ylabel = IntegerField( default = 0 )
    ypred = FloatField( default = 0 )
    Id = IntegerField(primary_key = True)
    windows = IntegerField( default = 0 )
    port_num = IntegerField( default = 0 )

    class Meta:
         database = database

class Test_Result(Model):
    '''
    存储相似度计算字段
    '''
    ipa = CharField( default = '' )
    ipb = CharField( default = '' )
    start_time_A = DoubleField( default = 0 )
    end_time_A = DoubleField( default = 0 )
    start_time_B = DoubleField( default = 0 )
    end_time_B = DoubleField( default = 0 )
    dev_id_A = CharField( default = '' )
    traffic_id_A = IntegerField( default = 0 )
    dev_id_B = CharField( default = '' )
    traffic_id_B = IntegerField( default = 0 )
    distance = FloatField( default = 0 )
    d_basic =  FloatField( default = 0 )
    d_peer_port =  FloatField( default = 0 )
    d_dst_ip =  FloatField( default = 0 )
    d_local_port =  FloatField( default = 0 )
    d_ports = FloatField( default = 0 )
    dpp_max_len = IntegerField( default = 0 )
    dpp_repetition_num = IntegerField( default = 0 )
    ddi_max_len = IntegerField( default = 0 )
    ddi_repetition_num = IntegerField( default = 0 )
    dlp_max_len = IntegerField( default = 0 )
    dlp_repetition_num = IntegerField( default = 0 )
    ylabel = IntegerField( default = 0 )
    ypred = FloatField( default = 0 )
    Id = IntegerField(primary_key = True)
    class Meta:
         database = database


    class Meta:
        database = database

class MultiSonMac(Model):
    '''
    映射到多个IP的MAC
    '''

    ip = CharField( default = '' )
    dev_id = CharField( default = '' )
    Id = AutoField(primary_key = True)
    class Meta:
         database = database


class Dev(Model):
    '''
    ip 和dev_id对应
    '''

    ip = CharField( default = '' )
    dev_id = CharField( default = '' )
    Id = AutoField(primary_key = True)
    class Meta:
         database = database

class Evaluation_result(Model):
    '''
    评估结果
    '''
    date = DateTimeField()
    keep_alive = IntegerField(default=0)
    continue_time = IntegerField(default=0)
    tao = IntegerField( default=0)
    AUC = FloatField( default=0)
    Precision = FloatField( default=0)
    F1 = FloatField( default=0)
    Recall = FloatField( default=0)
    FPR = FloatField(default=0)
    TPR = FloatField(default=0)
    ACC = FloatField(default=0)
    threshold = FloatField(default=0)
    port_num = IntegerField(default=0)
    model = CharField(default='decision tree')
    ceil_rate = FloatField(default=0)
    class Meta:
        database = database

class Dup_event(Model):
    
    sid = IntegerField()
    cid  = IntegerField()
    signature  = IntegerField()
    timestamp = DateTimeField()
    ip_src  = IntegerField()
    ip_dst  = IntegerField()
    ip_ver  = IntegerField()
    ip_hlen  = IntegerField()
    ip_tos  = IntegerField()
    ip_len  = IntegerField()
    ip_id  = IntegerField()
    ip_flags  = IntegerField()
    ip_off  = IntegerField()
    ip_ttl  = IntegerField()
    ip_proto  = IntegerField()
    ip_csum  = IntegerField()
    dev_id = CharField()
    Id = AutoField(primary_key = True)
    class Meta:
         database = database


 
if __name__ == "__main__":
    #Frameceil.create_table()
    #Frame.create_table()
    try:
        Test_Result()
    except Exception as e:
        print(e)
    #Port_feature.create_table()
    #Basic_feature.create_table() 
    #Configure.create_table()
    #MultiSonMac.create_table()
    #Dev.create_table()
    #Evaluation_result.create_table()
    #Dup_event.create_table()
