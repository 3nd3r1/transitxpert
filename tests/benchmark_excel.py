# pylint: disable-all
import xlsxwriter
import random
import time

from soteriareitti.core.map import Map

from soteriareitti.algorithms.dijkstra import Dijkstra
from soteriareitti.algorithms.ida_star import IdaStar

from soteriareitti.utils.geo import GeoUtils
from soteriareitti.utils.file_reader import get_data
from soteriareitti.utils.logging import configure_logging


def random_node(graph):
    return random.choice(graph.get_nodes())


average_speed = None

ida_results = []
dijkstra_results = []

dp = {}


def heuristic(node, target_node) -> float:
    """ Minutes to travel from node to target node """
    if dp.get(node.id, False):
        return dp.get(node.id)

    dp[node.id] = GeoUtils.calculate_time(node.location,
                                          target_node.location, average_speed).minutes
    return dp[node.id]


def run_test(map: Map, place: str):
    global average_speed
    global dp
    map.load_place(place)
    dp = {}
    graph = map._graph
    average_speed = map._average_speed

    source = random_node(graph)
    target = random_node(graph)

    time_before = time.time()
    path_ida = IdaStar.get_shortest_path(graph, heuristic, source, target, delta=0.1)
    time_ida = time.time()-time_before

    time_before = time.time()
    path_dijkstra = Dijkstra.get_shortest_path(graph, source, target)
    time_dijkstra = time.time()-time_before

    if path_ida and path_dijkstra:
        ida_results.append([len(path_ida), time_ida, path_ida.cost])
        dijkstra_results.append([len(path_dijkstra), time_dijkstra, path_dijkstra.cost])


if __name__ == "__main__":
    configure_logging(True)
    map = Map()

    for _ in range(20):
        # Tests in Paloheinä (small)
        run_test(map, "Paloheinä")

        # Tests in Töölö (small)
        run_test(map, "Töölö")

        # Tests in Helsinki (large)
        run_test(map, "Helsinki")

    workbook = xlsxwriter.Workbook(get_data("benchmark.xlsx"))
    worksheet = workbook.add_worksheet()
    for row_num, row_data in enumerate(ida_results):
        worksheet.write(row_num, 0, row_data[0])
        worksheet.write(row_num, 1, row_data[1])
        worksheet.write(row_num, 2, row_data[2])
    for row_num, row_data in enumerate(dijkstra_results):
        worksheet.write(row_num, 4, row_data[0])
        worksheet.write(row_num, 5, row_data[1])
        worksheet.write(row_num, 6, row_data[2])
    workbook.close()
