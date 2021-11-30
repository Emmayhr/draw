from edge import Edge


class Node:

    def __init__(self, ip: str, is_important_node: bool = False):
        self.ip = ip
        self.next_hop_edge_list = []
        self.last_hop_edge_list = []
        self.next_hop_neighbor = []
        self.last_hop_neighbor = []
        self.is_important_node = is_important_node

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
