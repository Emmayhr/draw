# When there is an Alert between two entities, we think there is an edge between the two nodes.
# This class defines the attributes of the edge
# By yhr in November

#from node import Node

class EdgeAttribute:
    def __init__(self, alert):
        self.id = alert.id
        self.timestamp = alert.timestamp
        self.msg = alert.msg
        self.category = alert.category
        self.severity = alert.severity
        self.transport_protocol = alert.transport_protocol
        self.ip_src = alert.ip_src
        self.src_port = alert.src_port
        self.ip_dst = alert.ip_dst
        self.dst_port = alert.dst_port



class Edge:
    def __init__(self, endpoint_a:object, endpoint_b:object, attribute:EdgeAttribute):
        self.endpoint_a = endpoint_a
        self.endpoint_b = endpoint_b
        self.attribute = attribute
