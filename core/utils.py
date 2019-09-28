from core.models import *
import math 


X_N = 'latitude'
Y_N = 'longitude'

TEN_MINUTE = 0.05


def compute_score_for_measure(measure):
    return 1


def get_signal_map(operator, network, left_down_p, right_up_p,
                   resolution=500):
    left_down_p[X_N] = float(left_down_p[X_N])
    left_down_p[Y_N] = float(left_down_p[Y_N])
    right_up_p[Y_N] = float(right_up_p[Y_N])
    right_up_p[X_N] = float(right_up_p[X_N])

    map = get_zeros_signal_map(left_down_p, right_up_p, resolution)
    coverages = get_coverages_intersected_with_rect(operator,
                                                    network,
                                                    left_down_p,
                                                    right_up_p
                                                    )
    n = len(coverages)
    print(f'coverages count: {n}')
    apply_coverages_on_map(map, coverages)
    measures = get_measures_in_rectangle(operator, network, left_down_p, right_up_p)
    n = len(measures)
    print(f'measures count = {n}; {left_down_p[X_N]}; {left_down_p[Y_N]} - {right_up_p[X_N]} ; {right_up_p[Y_N]}')
    apply_measures_on_map(map, measures, TEN_MINUTE)
    return map
    


def get_measures_in_rectangle(operator, network, left_down_p, right_up_p):
    return Measure.\
                objects.\
                filter(
                       latitude__gte=left_down_p[X_N],
                       latitude__lte=right_up_p[X_N],
                       longitude__gte=left_down_p[Y_N],
                       longitude__lte=right_up_p[Y_N],
                       operator_id=operator,
                       network_id=network
                       )


def get_coverages_intersected_with_rect(operator, network, left_down_p, right_up_p):
    return Coverage.\
            objects.\
            filter(
                   center_latitude__gte=left_down_p[X_N],
                   center_latitude__lte=right_up_p[X_N],
                   center_longitude__gte=left_down_p[Y_N],
                   center_longitude__lte=right_up_p[Y_N],
                   operator_id=operator,
                   network_id=network
                   )


def get_zeros_signal_map(left_down_p, right_up_p, resolution):
    map = []
    x = left_down_p[X_N]
    y = left_down_p[Y_N]
    x_step = (right_up_p[X_N] - left_down_p[X_N]) / resolution
    y_step = (right_up_p[Y_N] - left_down_p[Y_N]) / resolution
    while x <= right_up_p[X_N]:
        while y <= right_up_p[Y_N]:
            y += y_step
            map.append({'Points': [x, y],
                        'Reliability': 0,
                        'Signal': 0})
        x += x_step
    return map


def apply_coverages_on_map(map, coverages):
    for cover in coverages:
        points = CoveragePoints.\
                    objects.\
                    filter(coverage_id=cover).\
                    order_by(X_N, Y_N)
                
        n = len(points)
        print(f'coverage points: {n}')
        if (n != 2):
            continue
        left_p = points[0]
        right_p = points[1]
        for map_point in map:
            if map_point['Reliability'] > cover.reliability:
                continue            
            if is_point_inside(map_point, left_p, right_p):
                if map_point['Reliability'] < cover.reliability or\
                        map_point['Signal'] < cover.signal:
                    map_point['Signal'] = cover.signal
                

def apply_measures_on_map(map, measures, reliability_range):
    for measure in measures:
        map_len = len(map)
        print(f'maplen = {map_len}')
        for map_point in map:
            dist = dist_between_points(map_point['Points'],
                                       [measure.latitude,
                                        measure.longitude
                                        ]
                                       )
            reliability = 1 - dist / reliability_range
            if reliability > map_point['Reliability']:
                map_point['Signal'] = measure.signal
                map_point['Reliability'] = reliability
                # todo: update by time 


                    


def is_point_inside(map_point, left_p, right_p):
    return map_point['Points'][0] >= left_p.latitude and\
            map_point['Points'][0] <= right_p.latitude and\
            map_point['Points'][1] >= left_p.longitude and\
            map_point['Points'][1] <= right_p.longitude


def dist_between_points(point1, point2):
    cathet_x = point2[0] - point1[0]
    cathet_y = point2[1] - point1[1]
    return math.sqrt(cathet_x**2 + cathet_y**2)