import math
import random

from edge import Edge


class Node:

    def __init__(self, ip: str, is_important_node: bool = False):
        self.ip = ip
        self.next_hop_edge_list = []
        self.last_hop_edge_list = []
        self.next_hop_neighbor = []
        self.last_hop_neighbor = []
        self.is_important_node = is_important_node
        self.coodinary = {}

    def pad_coodinary(self, a):
        self.coodinary = a
        print("$$$$$$$$$$$$$$$$4")
        print(self.coodinary)

    # This is a poor father who has no son, but he has a single parent
    def is_lonely_father(self):
        if len(self.next_hop_neighbor) == 0:
            if len(self.last_hop_neighbor) == 1:
                return self.last_hop_neighbor[0]

    def adjust_coodinary(self, son):
        base_x, base_y = son.get_coodinary()
        theta = random.randint(0, 360)
        self.coodinary['x'] = base_x + 5 * math.cos(theta)
        self.coodinary['y'] = base_y + 5 * math.sin(theta)

    def get_coodinary(self):
        print(self.coodinary)
        return self.coodinary['x'], self.coodinary['y']
    # This is a poor son who has no father, but he has a single son
    def is_lonely_son(self):
        if len(self.last_hop_neighbor) == 0:
            if len(self.next_hop_neighbor) == 1:
                return True

    def add_edge(self, edge: Edge):
        self.edge_list.append(edge)

    def add_next_hop_neighbor(self, node: object):
        self.next_hop_neighbor.append(node)
        self.next_hop_edge_list.append([])

    def add_last_hop_neighbor(self, node: object):
        self.last_hop_neighbor.append(node)
        self.last_hop_edge_list.append([])

    def add_next_hop_edge(self, node: object, edge: object):
        if node not in self.next_hop_neighbor:
            self.next_hop_edge_list.append([edge])
        else:
            index = self.next_hop_neighbor.index(node)
            self.next_hop_edge_list[index].append(edge)

    def add_last_hop_edge(self, node: object, edge: object):
        if node not in self.last_hop_neighbor:
            self.last_hop_edge_list.append([edge])
        else:
            index = self.last_hop_neighbor.index(node)
            self.last_hop_edge_list[index].append(edge)

    def print_node(self):
        print("IP is : %s" % self.ip)
        print("len of next hop edge_list is %d" % len(self.next_hop_edge_list))
        print("len of last hop edge_list is %d" % len(self.last_hop_edge_list))
        print("len of next hop neighbor is %d" % len(self.next_hop_neighbor))
        print("len of last hop neighbor is %d" % len(self.last_hop_neighbor))
        print("is important_node : ", self.is_important_node)
