from typing import List, Any
from node import Node
from alert_db import *
from edge import Edge
from edge import EdgeAttribute
import plotly
import math
import numpy as np
import plotly as gf
import chart_studio
import chart_studio.plotly as py
from plotly.graph_objects import Scatter
import plotly.graph_objects as go


class Graph:

    def __init__(self):
        self.node_dict = {}
        self.edge_list = []
        self.r = 5
        self.X_not_concerned = []
        self.Y_not_concerned = []
        self.X_concerned = []
        self.Y_concerned = []
        self.arrow_dict_list = []
        self.concerned_ip_list = []
        self.node_cordinary_list = []
        self.fig = go.Figure()
        self.edge_drew_list = []
        self.node_drew_dict = {}
        self.max_neighbor = 5

    # The purpose of this function is to calculate the breadth score of a node and iterate over the number of other
    # nodes associated with it
    def get_node_score_breath(self, node: Node, last_hop_ip_list: list):
        score = len(node.next_hop_neighbor)
        return score

    # The purpose of this function is to calculate the depth score of a node and calculate the maximum length in the
    # attack chain associated with it
    def get_node_score_depth(self, node: Node, last_hop_ip_list: list):
        # if node.ip == '202.207.236.4':
        #    print("let's go to capture the exception")
        if node.ip in last_hop_ip_list:
            return 0
        score = 1 if len(node.next_hop_neighbor) != 0 else 0
        for n in node.next_hop_neighbor:
            if n.ip not in last_hop_ip_list:
                last_hop_ip_list.append(n.ip)
                score += self.get_node_score_depth(n, last_hop_ip_list)
        return score

    # The score of the node is calculated, considering the breadth score and depth score, considering that the breadth
    # score of a node is often very large, so the log operation is taken
    def get_node_score(self, node: Node):
        node_ip_list = [node.ip]
        breath_score = self.get_node_score_breath(node, node_ip_list)
        depth_score = self.get_node_score_depth(node, node_ip_list)
        if breath_score != 0:
            breath_score = math.log(breath_score) if math.log(breath_score) < 10 else 10
        return depth_score + breath_score

    # Nodes are sorted from largest to smallest according to their scores
    # return node_list and edge_list after ranking
    def neighbor_rank(self, node_list: list, edge_list: list):
        score_dict = {}
        node_list_best_10: List[Any] = []
        edge_list_best_10: List[Any] = []
        for i in range(len(node_list)):
            node = node_list[i]
            score = self.get_node_score(node)
            score_dict[i] = score
        score_dict_rank_by_score = dict(sorted(score_dict.items(), key=lambda e: e[1], reverse=True))
        key_list = list(score_dict_rank_by_score.keys())
        for i in range(len(key_list)):
            if i >= 3:
                break
            else:
                node_list_best_10.append(node_list[i])
                edge_list_best_10.append(edge_list[i])
        return node_list_best_10, edge_list_best_10

    # Iterate over node_cordinary_list, drawing points and commenting on the diagram
    def draw_node(self):
        for level in range(len(self.node_cordinary_list)):
            x_list_important = list()
            x_list_not_important = list()
            y_list_important = list()
            y_list_not_important = list()
            node_list = self.node_cordinary_list[level]
            for node in node_list:
                if node['important']:
                    x_list_important.append(node['x'])
                    y_list_important.append(node['y'])
                if not node['important']:
                    x_list_not_important.append(node['x'])
                    y_list_not_important.append(node['y'])
                self.fig.add_annotation(
                    x=node['x'],  # arrows' head
                    y=node['y'] - 1,  # arrows' head
                    text=node['ip'],
                    showarrow=False,
                    font=dict(size=8)
                )
            if len(x_list_not_important) != 0:
                trace_not_concerned = go.Scatter(
                    x=x_list_not_important,
                    y=y_list_not_important,
                    mode='markers',
                    marker=dict(
                        size=20,
                        symbol='circle-open'
                    )
                )
                self.fig.add_trace(trace_not_concerned)

            if len(x_list_important) != 0:
                trace_concerned = go.Scatter(
                    x=x_list_important,
                    y=y_list_important,
                    mode='markers',
                    marker=dict(
                        size=20
                    )
                )
                self.fig.add_trace(trace_concerned)

    # Draw edges with arrows on the graph. If there is an alert, the two points are considered to have an edge
    def draw_arrow(self):
        for arrow in self.arrow_dict_list:
            x_start = arrow['x_start']
            y_start = arrow['y_start']
            x_end = arrow['x_end']
            y_end = arrow['y_end']
            msg = 'msg : '
            for e in arrow['edge']:
                msg = msg + e.attribute.msg
            self.fig.add_annotation(
                x=x_end,  # arrows' head
                y=y_end,  # arrows' head
                ax=x_start,  # arrows' tail
                ay=y_start,  # arrows' tail
                xref='x',
                yref='y',
                axref='x',
                ayref='y',
                text='',  # if you want only the arrow
                showarrow=True,
                arrowhead=3,
                arrowsize=1,
                arrowwidth=0.5,
                arrowcolor='black'
            )
            '''
            self.fig.add_annotation(
                x=0.5 * (x_start + x_end),  # arrows' head
                y=0.5 * (y_start + y_end) + 0.5,  # arrows' head
                text=msg,
                textangle=angle,
                showarrow=False
            )
            '''

    # The input is the list of down flow neighbor nodes, the coordinates of the center node, and the initial Angle.
    # The output is the coordinates and angles of the neighbor node
    def get_cordinary_down_flow(self, next_hop_neighbor_list, base_x, base_y, r=5, init_angle=math.pi):
        neighbor_num = len(next_hop_neighbor_list)
        theta = np.linspace(init_angle + 1.5 * math.pi, init_angle + 2.5 * math.pi, neighbor_num, endpoint=False)
        x: list = list(base_x + r * np.cos(theta))
        y: list = list(base_y + r * np.sin(theta))
        return x, y, theta

    # The input is the center node, and the function adds the neighbors of the center node to the graph
    def add_sons_to_graph_down_flow(self, node, r=5, level=1, init_angle=math.pi):
        next_hop_neighbor_list_level1 = node.next_hop_neighbor[:self.max_neighbor]
        self.node_cordinary_list.append([])
        base_x = self.node_drew_dict[node.ip][0]
        base_y = self.node_drew_dict[node.ip][1]
        init_angle = self.node_drew_dict[node.ip][2]
        x_level1, y_level1, theta_level1 = self.get_cordinary_up_flow(next_hop_neighbor_list_level1, base_x, base_y, r,
                                                                      init_angle)
        for i in range(len(next_hop_neighbor_list_level1)):
            neighbor_level1 = next_hop_neighbor_list_level1[i]
            self.node_cordinary_list.append([])
            if neighbor_level1.ip in self.node_drew_dict:
                x_end = self.node_drew_dict[neighbor_level1.ip][0]
                y_end = self.node_drew_dict[neighbor_level1.ip][1]
            else:
                x_end = x_level1[i] + 0.1 * math.cos(theta_level1[i])
                y_end = y_level1[i] + 0.1 * math.sin(theta_level1[i])
                self.node_cordinary_list[level].append(
                    {'x': x_level1[i], 'y': y_level1[i], 'important': neighbor_level1.is_important_node,
                     'ip': neighbor_level1.ip, 'node': neighbor_level1})
                self.node_drew_dict[neighbor_level1.ip] = [x_level1[i], y_level1[i], theta_level1[i]]
            edge_list = node.next_hop_edge_list[i]
            self.arrow_dict_list.append(
                {'x_start': base_x, 'y_start': base_y,
                 'x_end': x_end, 'y_end': y_end,
                 'edge': edge_list, 'angle': 180 * theta_level1[i] / math.pi,
                 'start': node, 'end': neighbor_level1})

    # The input is the initial node, and the function is to add the second-order downstream nodes of that node to
    # the graph
    def add_node_to_graph_down_flow(self, node, base_x=0, base_y=0, r=5):
        if node.ip not in self.node_drew_dict:
            if len(self.node_cordinary_list) >= 1:
                self.node_cordinary_list[0].append({'x': base_x, 'y': base_y, 'important': node.is_important_node,
                                                    'ip': node.ip, 'node': node})
            else:
                self.node_cordinary_list.append([{'x': base_x, 'y': base_y, 'important': node.is_important_node,
                                                  'ip': node.ip, 'node': node}])
        self.node_drew_dict[node.ip] = [base_x, base_y, math.pi]
        self.add_sons_to_graph_down_flow(node, r=5)
        for node_next_level in node.next_hop_neighbor[:self.max_neighbor]:
            if node_next_level.ip not in self.node_drew_dict:
                print(node_next_level.ip)
            init_angle = self.node_drew_dict[node_next_level.ip][2]
            self.add_sons_to_graph_down_flow(node_next_level, r=5, init_angle=init_angle)
        return 1

    # The input is the list of up flow neighbor nodes, the coordinates of the center node, and the initial Angle.
    # The output is the coordinates and angles of the last neighbor node
    def get_cordinary_up_flow(self, last_hop_neighbor_list, base_x, base_y, r=5, init_angle=math.pi):
        neighbor_num = len(last_hop_neighbor_list)
        theta = np.linspace(init_angle - 0.5 * math.pi, init_angle + 0.5 * math.pi, neighbor_num, endpoint=False)
        x: list = list(base_x + r * np.cos(theta))
        y: list = list(base_y + r * np.sin(theta))
        return x, y, theta

    # The input is the center node, and the function adds the last neighbors of the center node to the graph
    def add_fathers_to_graph_up_flow(self, node, r=5, level=1, init_angle=math.pi):
        last_hop_neighbor_list_level1 = node.last_hop_neighbor[:self.max_neighbor]
        self.node_cordinary_list.append([])
        base_x = self.node_drew_dict[node.ip][0]
        base_y = self.node_drew_dict[node.ip][1]
        init_angle = self.node_drew_dict[node.ip][2]
        x_level1, y_level1, theta_level1 = self.get_cordinary_up_flow(last_hop_neighbor_list_level1, base_x, base_y, r,
                                                                      init_angle)
        for i in range(len(last_hop_neighbor_list_level1)):
            neighbor_level1 = last_hop_neighbor_list_level1[i]
            self.node_cordinary_list.append([])
            if neighbor_level1.ip in self.node_drew_dict:
                x_start = self.node_drew_dict[neighbor_level1.ip][0]
                y_start = self.node_drew_dict[neighbor_level1.ip][1]
            else:
                x_start = x_level1[i]
                y_start = y_level1[i]
                self.node_cordinary_list[level].append(
                    {'x': x_level1[i], 'y': y_level1[i], 'important': neighbor_level1.is_important_node,
                     'ip': neighbor_level1.ip, 'node': neighbor_level1})
                #node.pad_coodinary(self.node_cordinary_list[0][-1])
                self.node_drew_dict[neighbor_level1.ip] = [x_level1[i], y_level1[i], theta_level1[i]]
            edge_list = node.last_hop_edge_list[i]
            self.arrow_dict_list.append(
                {'x_start': x_start, 'y_start': y_start,
                 'x_end': base_x, 'y_end': base_y,
                 'edge': edge_list, 'angle': 180 * theta_level1[i] / math.pi,
                 'start': neighbor_level1, 'end': node})

    # The input is the initial node, and the function is to add the second-order upstream nodes of that node to
    # the graph
    def add_node_to_graph_up_flow(self, node, base_x=0, base_y=0, r=5):
        if node.ip not in self.node_drew_dict:
            if len(self.node_cordinary_list) >= 1:
                self.node_cordinary_list[0].append({'x': base_x, 'y': base_y, 'important': node.is_important_node,
                                                    'ip': node.ip})
            else:
                self.node_cordinary_list.append([{'x': base_x, 'y': base_y, 'important': node.is_important_node,
                                                  'ip': node.ip, 'node': node}])
            #node.pad_coodinary(self.node_cordinary_list[0][-1])
        self.node_drew_dict[node.ip] = [base_x, base_y, math.pi]
        self.add_fathers_to_graph_up_flow(node, r=5)
        for node_last_level in node.last_hop_neighbor[:self.max_neighbor]:
            if node_last_level.ip not in self.node_drew_dict:
                print("exception occured node.ip is : %s" % node.ip)
                print("exception occured node_last_level.ip is : %s" % node_last_level.ip)
            init_angle = self.node_drew_dict[node_last_level.ip][2]
            self.add_fathers_to_graph_up_flow(node_last_level, r=5, init_angle=init_angle)
        return 1

    # Input the IP address of the central node to add all nodes associated with the node to the diagram
    def draw_subgraph_with_node(self, ip: str, base_x=0, base_y=0):
        r = 5
        if ip not in self.node_dict:
            return
        else:
            node = self.node_dict[ip]
            if ip in self.node_drew_dict:
                base_x = self.node_drew_dict[ip][0]
                base_y = self.node_drew_dict[ip][1]
            self.add_node_to_graph_down_flow(node, base_x=base_x, base_y=base_y, r=self.r)
            self.add_node_to_graph_up_flow(node, base_x=base_x, base_y=base_y, r=self.r)
            self.draw_node()
            self.draw_arrow()
        return

    # Input the IP address list and add all nodes associated with these nodes to the diagram
    def draw_subgraph_with_nodes(self, ip_list: list):
        base_x = 0
        base_y = 0
        for i in range(len(ip_list)):
            if i < 8:
                step = 4
            else:
                step = 10
            ip = ip_list[i]
            print(ip)
            if i%4 == 0:
                x = base_x
                y = base_y
            if i % 4 == 1:
                x = base_x + step
                y = base_y
            if i % 4 == 2:
                x = base_x
                y = base_y + step
            if i % 4 == 3:
                x = base_x + step
                y = base_y + step
            base_x += 2 * step
            self.draw_subgraph_with_node(ip, x, y)


    # All concerned IP exists in the file, enter the path of the file, read all concerned IP
    def get_concerned_ip(self, path):
        try:
            f = open(path, 'r')
            self.concerned_ip_list = eval(f.read())
            print(self.concerned_ip_list)
        finally:
            if f:
                f.close()

    # Enter an IP address to check whether it is a concerned IP address
    def is_concerned_ip(self, ip: str):
        if ip in self.concerned_ip_list:
            return True
        else:
            return False

    # Read all the alerts from the database and build the attack map
    def construct_graph(self):
        limit = 1000
        page = 0
        try:
            while 1:
                res = Alert.select().paginate(page, limit)
                page += 1
                for alert in res:
                    src_ip = alert.ip_src
                    dst_ip = alert.ip_dst
                    if src_ip in self.node_dict:
                        node_a = self.node_dict[src_ip]
                    else:
                        node_a = Node(src_ip, self.is_concerned_ip(src_ip))
                        self.node_dict[src_ip] = node_a
                    if dst_ip in self.node_dict:
                        node_b = self.node_dict[dst_ip]
                    else:
                        node_b = Node(dst_ip, self.is_concerned_ip(dst_ip))
                        self.node_dict[dst_ip] = node_b
                    if node_b not in node_a.next_hop_neighbor:
                        node_a.add_next_hop_neighbor(node_b)
                    if node_a not in node_b.last_hop_neighbor:
                        node_b.add_last_hop_neighbor(node_a)
                    attribute = EdgeAttribute(alert)
                    edge = Edge(node_a, node_b, attribute)
                    self.edge_drew_list.append(node_a.ip + node_b.ip)
                    node_a.add_next_hop_edge(node_b, edge)
                    node_b.add_last_hop_edge(node_a, edge)
                if len(res) < limit:
                    break
        except Exception as e:
            print("error")
            print(e)

    def find_concerned_ip_in_alert(self):
        concerned_ip_alerts = []
        alert_ip_set = set()
        try:
            res = Alert.select(Alert.ip_src).distinct()
            for alert in res:
                alert_ip_set.add(alert.ip_src)
            res = Alert.select(Alert.ip_dst).distinct()
            for alert in res:
                alert_ip_set.add(alert.ip_src)
            for ip in self.concerned_ip_list:
                if ip in alert_ip_set:
                    concerned_ip_alerts.append(ip)
            print("#########print concerned ip with alerts, total num is %d######" % len(concerned_ip_alerts))
            print(concerned_ip_alerts)
            return concerned_ip_alerts
        except Exception as e:
            print(e)

    def adjust(self):
        for key,node in self.node_dict.items():
            if node.is_lonely_son():
                son = node.next_hop_neighbor[0]

                node.adjust_coodinary(son)

if __name__ == "__main__":
    graph = Graph()
    graph.get_concerned_ip("concerned_ip")
    concerned_ip_alerts = graph.find_concerned_ip_in_alert()
    graph.construct_graph()
    #graph.draw_subgraph_with_nodes(concerned_ip_alerts[:10])
    graph.draw_subgraph_with_nodes(["98.7.212.253", "68.42.224.172", "45.60.58.189", "113.13.230.10",
                                    "2408:8406:1860:5344:20a8:1fce:2c8e:b53f",
                                    "2408:8406:1860:5344:44f9:2b5a:7ea9:1921", "125.222.107.71", "146.121.155.227",
                                    "59.150.192.68", "10.9.53.54"])
    #gf.offline.plot(graph.fig)
    plotly.io.write_image(graph.fig, 'output_file.pdf', format='pdf')
