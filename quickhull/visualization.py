import plotly.offline as py
from plotly.graph_objs import *
from random import randint
from quickhull import QuickHull, Point

import networkx as nx


class QuickHullAnimator:
    animation_speed = 1000

    def __init__(self, points):
        self.points = points
        self.quick_hull = QuickHull(self.points, self)
        self.temp_edge_trace = self._get_temp_edge_trace()
        self.done_edge_trace = self._get_done_edge_trace()
        self.node_trace = self._get_node_trace()
        self.selected_node_trace = self._get_selected_node_trace()
        self._init_node_trace()
        self.figure = {
            'data': Data([self.temp_edge_trace, self.done_edge_trace, self.node_trace, self.selected_node_trace]),
            'layout': {'showlegend': False}, 'frames': [],
        }
        self.figure['layout']['xaxis'] = {'showgrid': False, 'zeroline': False, 'showticklabels': True}
        self.figure['layout']['yaxis'] = {'showgrid': False, 'zeroline': False, 'showticklabels': True}

        self.sliders_dict = {
            'active': 0,
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 20},
                'prefix': 'Step:',
                'visible': True,
                'xanchor': 'right'
            },
            'transition': {'duration': self.animation_speed, 'easing': 'cubic-in-out'},
            'pad': {'b': 10, 't': 50},
            'len': 0.9,
            'x': 0.1,
            'y': 0,
            'steps': []
        }
        self.figure['layout']['updatemenus'] = [
            {
                'buttons': [
                    {
                        'args': [None, {'frame': {'duration': self.animation_speed, 'redraw': False},
                                        'fromcurrent': True,
                                        'transition': {'duration': self.animation_speed, 'easing': 'quadratic-in-out'}}],
                        'label': 'Play',
                        'method': 'animate'
                    },
                    {
                        'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                                          'transition': {'duration': 0}}],
                        'label': 'Pause',
                        'method': 'animate'
                    }
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 87},
                'showactive': False,
                'type': 'buttons',
                'x': 0.1,
                'xanchor': 'right',
                'y': 0,
                'yanchor': 'top'
            }
        ]
        self.figure['layout']['sliders'] = {
            'args': [
                'transition', {
                    'duration': self.animation_speed,
                    'easing': 'cubic-in-out'
                }
            ],
            'initialValue': '0',
            'plotlycommand': 'animate',
            'visible': True
        }
        self._create_frame("Initializing.")
        self._create_frame("Initializing.")

    def _init_node_trace(self):
        for point in self.points:
            self.node_trace['x'].append(point.x)
            self.node_trace['y'].append(point.y)

    def _get_node_trace(self):
        return Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                size=10,
                color='rgb(142, 63, 56)',
                line=dict(
                    width=2,
                )
            )
        )

    def _get_selected_node_trace(self):
        return Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                size=10,
                color='rgb(77, 124, 213)',
                line=dict(
                    width=6,
                )
            )
        )

    def _get_temp_edge_trace(self):
        return Scatter(
            x=[],
            y=[],
            line=dict(color=('rgb(22, 96, 167)'), width=0.5),
            hoverinfo='none',
            mode='lines')

    def _get_done_edge_trace(self):
        return Scatter(
            x=[],
            y=[],
            line=dict(
                color=('rgb(205, 12, 24)'),
                width=4),
            hoverinfo='none',
            mode='lines')

    def _copy_trace(self, from_trace, to_trace):
        to_trace['x'] = list(from_trace['x'])
        to_trace['y'] = list(from_trace['y'])
        return to_trace

    def _add_temp_edge(self, from_point, to_point, comment):
        self.temp_edge_trace = self._copy_trace(self.temp_edge_trace, self._get_temp_edge_trace())
        self.temp_edge_trace['x'] += [from_point.x, to_point.x, None]
        self.temp_edge_trace['y'] += [from_point.y, to_point.y, None]
        self._create_frame(comment)

    def _remove_line_from_temp_edges(self, from_point, to_point, comment):
        pass
        # self.temp_edge_trace = self._copy_trace(self.temp_edge_trace, self._get_temp_edge_trace())
        # for i in range(0, len(self.temp_edge_trace['x']), 3):
        #     if self.temp_edge_trace['x'][i] == from_point.x and\
        #         self.temp_edge_trace['x'][i + 1] == to_point.x and\
        #         self.temp_edge_trace['y'][i] == from_point.y and\
        #         self.temp_edge_trace['y'][i + 1] == to_point.y:
        #         self.temp_edge_trace['x'] = self.temp_edge_trace['x'][:i] + [None, None, None] + self.temp_edge_trace['x'][i + 3:]
        #         self.temp_edge_trace['y'] = self.temp_edge_trace['y'][:i] + [None, None, None] + self.temp_edge_trace['y'][i + 3:]
        #         self._create_frame(comment)
        #         return

    def _add_done_edge(self, from_point, to_point, comment):
        self.done_edge_trace = self._copy_trace(self.done_edge_trace, self._get_done_edge_trace())
        self.done_edge_trace['x'] += [from_point.x, to_point.x, None]
        self.done_edge_trace['y'] += [from_point.y, to_point.y, None]
        self._create_frame(comment)

    def _create_frame(self, comment):
        self.figure['frames'].append({'data': Data([self.temp_edge_trace, self.done_edge_trace, self.node_trace, self.selected_node_trace]),
                                      'name': len(self.sliders_dict['steps'])})
        slider_step = {
            'args': [
                [len(self.sliders_dict['steps'])],
                {'frame': {'duration': self.animation_speed, 'redraw': False},
                'mode': 'immediate',
                'transition': {'duration': self.animation_speed}}
            ],
            'label': comment,
            'method': 'animate'
        }
        self.sliders_dict['steps'].append(slider_step)

    def draw(self):
        self.figure['layout']['sliders'] = [self.sliders_dict]
        py.plot(self.figure)

    def add_to_hull(self, begin, end):
        self._add_done_edge(begin, end, "Add line to hull.")

    def add_line(self, begin, end, comment):
        self._add_temp_edge(begin, end, comment)

    def remove_line(self, begin, end, comment):
        self._remove_line_from_temp_edges(begin, end, comment)

    def select_points(self, points, comment):
        self.node_trace = self._copy_trace(self.node_trace, self._get_node_trace())
        self.selected_node_trace = self._copy_trace(self.selected_node_trace, self._get_selected_node_trace())
        # node_xs = []
        # node_ys = []
        # for i in range(len(self.node_trace['x'])):
        #     found = False
        #     for j in range(len(points)):
        #         if self.node_trace['x'][i] == points[j].x and self.node_trace['y'][i] == points[j].y:
        #             found = True
        #             break
        #     if not found:
        #         node_xs.append(self.node_trace['x'][i])
        #         node_ys.append(self.node_trace['y'][i])
        #     else:
        #         node_xs.append(0)
        #         node_ys.append(-20000)
        # self.node_trace['x'] = node_xs
        # self.node_trace['y'] = node_ys
        for j in range(len(points)):
            self.selected_node_trace['x'].append(points[j].x)
            self.selected_node_trace['y'].append(points[j].y)
        self._create_frame(comment)

    def deselect_points(self):
        self.selected_node_trace = self._get_selected_node_trace()
        self.node_trace = self._get_node_trace()
        self._init_node_trace()
        self._create_frame("")


points = []
for node in range(100):
    x, y = randint(-10000, 10000), randint(-10000, 10000)
    points.append(Point(x, y))

animator = QuickHullAnimator(points)

animator.quick_hull.calculate()

animator.draw()
