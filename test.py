import plotly as gf
import chart_studio
import chart_studio.plotly as py
from plotly.graph_objects import Scatter
import plotly.graph_objects as go

import numpy as np

a = {'hello':2, 'word':3}
b = dict(sorted(a.items(), key=lambda e: e[1], reverse=True))
print(b)

chart_studio.tools.set_credentials_file(
    username='xiaofeichai',       # 账户名
    api_key='U4fqhGcM0emaE1ynQsxv'              # api key
)


trace1=go.Scatter(
    x=[],
    y=[],
    mode='markers'
)

trace2=go.Scatter(
    x=[5,6,7,8],
    y=[5,6,7,8],
    mode='markers'
)

trace3=go.Scatter(
    x=[9,10],
    y=[5,6],
    mode='markers'
)

data = [trace1, trace2]

data = data + [trace3]

fig = go.Figure()
fig.add_trace(trace1)
fig.add_trace(trace2)

fig.add_annotation(
  x=1, # arrows' head
  y=1,  # arrows' head
  ax=2,  # arrows' tail
  ay=2,  # arrows' tail
  xref='x',
  yref='y',
  axref='x',
  ayref='y',
  text='nihao',  # if you want only the arrow
  showarrow=True,
  arrowhead=3,
  arrowsize=1,
  arrowwidth=1,
  arrowcolor='black'
)
fig.add_annotation(
  x=2, # arrows' head
  y=2,  # arrows' head
  ax=3,  # arrows' tail
  ay=3,  # arrows' tail
  xref='x',
  yref='y',
  axref='x',
  ayref='y',
  text='world',  # if you want only the arrow
  showarrow=True,
  arrowhead=3,
  arrowsize=1,
  arrowwidth=1,
  arrowcolor='black'
)

'''
def add_node_to_graph_up_flow(self, node, base_x=0, base_y=0, r=5, level=0, last_ip_list=[]):
    if node.ip not in self.node_drew_dict:
        if level == 0 or len(self.node_cordinary_list) <= level:
            self.node_cordinary_list.append(
                [{'x': base_x, 'y': base_y, 'important': node.is_important_node, 'ip': node.ip}])
        else:
            self.node_cordinary_list[level].append(
                {'x': base_x, 'y': base_y, 'important': node.is_important_node, 'ip': node.ip})
        self.node_drew_dict[node.ip] = [base_x, base_y]
    #print("############node ip is %s##############" % node.ip)
    last_hop_neighbor_list = node.last_hop_neighbor[:3]
    if len(last_hop_neighbor_list) == 0:
        return 0
    neighbor_num = len(last_hop_neighbor_list)
    theta = np.linspace(0.5 * math.pi, 1.5 * math.pi, neighbor_num, endpoint=False) if level == 0 else np.linspace(0.5 * math.pi,
                                                                                                   1.5 * math.pi,
                                                                                                   neighbor_num)
    x: list = list(base_x + r * np.cos(theta))
    y: list = list(base_y + r * np.sin(theta))
    level_next = level + 1
    for i in range(len(last_hop_neighbor_list)):
        n = last_hop_neighbor_list[i]
        edge_list = node.last_hop_edge_list[i]
        if n.ip in last_ip_list:
            continue
        last_ip_list.append(n.ip)
        self.add_node_to_graph_up_flow(n, x[i], y[i], 5, level=level_next, last_ip_list=last_ip_list)
        if n.ip in self.node_drew_dict:
            x_start = self.node_drew_dict[n.ip][0]
            y_start = self.node_drew_dict[n.ip][1]
        else:
            x_start = x[i] + 0.1 * math.cos(theta[i])
            y_start = y[i] + 0.1 * math.sin(theta[i])
        self.arrow_dict_list.append(
            {'x_start': x_start, 'y_start': y_start,
             'x_end': base_x - 0.1 * math.cos(theta[i]), 'y_end': base_y - 0.1 * math.sin(theta[i]),
             'edge': edge_list, 'angle': 180 * theta[i]/math.pi})
    return 1
    
        def add_node_to_graph_down_flow(self, node, base_x=0, base_y=0, r=5, level=0, last_ip_list: list = []):
        if r < 1:
            r = 1
        if node.ip not in self.node_drew_dict:
            if level == 0 or len(self.node_cordinary_list) <= level:
                self.node_cordinary_list.append(
                    [{'x': base_x, 'y': base_y, 'important': node.is_important_node, 'ip': node.ip}])
            else:
                self.node_cordinary_list[level].append(
                    {'x': base_x, 'y': base_y, 'important': node.is_important_node, 'ip': node.ip})
            self.node_drew_dict[node.ip] = [base_x, base_y]
        #print("############node ip is %s##############" % node.ip)
        next_hop_neighbor_list = node.next_hop_neighbor
        if len(next_hop_neighbor_list) == 0:
            return 0
        edge_list = node.next_hop_edge_list
        neighbor_list_best_10, edge_list_best_10 = self.neighbor_rank(next_hop_neighbor_list, edge_list)
        neighbor_num = len(neighbor_list_best_10)
        theta = np.linspace(0, 2 * math.pi, neighbor_num, endpoint=False) if level == 0 else np.linspace(-0.5 * math.pi,
                                                                                                       0.5 * math.pi,
                                                                                                       neighbor_num)
        x: list = list(base_x + r * np.cos(theta))
        y: list = list(base_y + r * np.sin(theta))
        level_next = level + 1
        for i in range(len(neighbor_list_best_10)):
            n = neighbor_list_best_10[i]
            if n.ip in last_ip_list:
                continue
            last_ip_list.append(n.ip)
            self.add_node_to_graph_down_flow(n, x[i], y[i], 5, level=level_next, last_ip_list=last_ip_list)
            if n.ip in self.node_drew_dict:
                x_end = self.node_drew_dict[n.ip][0]
                y_end = self.node_drew_dict[n.ip][1]
            else:
                x_end = x[i]
                y_end = y[i]
            self.arrow_dict_list.append(
                {'x_start': base_x + 0.1 * math.cos(theta[i]), 'y_start': base_y + 0.1 * math.sin(theta[i]),
                 'x_end': x_end - 0.1 * math.cos(theta[i]), 'y_end': y_end - 0.1 * math.sin(theta[i]),
                 'edge': edge_list_best_10[i], 'angle': 180 * theta[i]/math.pi})
        return 1
'''

gf.offline.plot(fig)

