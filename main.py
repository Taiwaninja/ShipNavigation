import consts
import json
from PointRouter import PointRouter
from shapely.geometry import Polygon


def main():
    start_router, end_router, routers = initialize_map()
    shortest_path = start_router.find_path(end_router, routers)
    save_results(shortest_path)


def initialize_map():
    """
    Initializes map from Input file
    :return: The start point, End point, And the routers to be used as a tuple.
    """
    icebergs = []
    with open(consts.INPUT_FILE_NAME, "r") as input_file:
        input_file = json.load(input_file)

    # We have to init icebergs before initing routers.
    # Redundant input "Iceberg count" We will ignore it
    # Might later be used for input validation.
    for iceberg in input_file[consts.ICEBERGS_FIELD]:
        icebergs.append(Polygon(iceberg))

    routers = {PointRouter(point, icebergs) for iceberg in input_file[consts.ICEBERGS_FIELD]
               for point in iceberg}
    start_router = PointRouter(input_file[consts.START_POINT_FIELD], icebergs)
    end_router = PointRouter(input_file[consts.END_POINT_FIELD], icebergs)
    return start_router, end_router, routers


def save_results(path):
    """
    Saves given result to the output file in JSON format.

    :param path: The path to save,
    :type: LineString
    """
    path_coordinates = zip(*path.xy)
    formated_dict = {consts.PATH_FIELD: path_coordinates}
    # Format was not specified - Hope json is fine.
    with open(consts.OUTPUT_FILE_NAME, "w") as output_file:
        json.dump(formated_dict, output_file)


if __name__ == "__main__":
    main()
