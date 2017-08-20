from shapely.geometry import Polygon, LineString


class PointRouter(object):
    """
    A Router used for naval navigation.
    Algorithem for routing is inspired by the BGP protocol.
    """

    def __init__(self, router_location, icebergs):
        """
        Iinitlizes a new instance of the router
        :param router_location: The location of the given router.
        :param icebergs: A list of polygons representing icebergs.
        """
        self.location = router_location
        self.routers_available = []
        self.icebergs = icebergs

    def is_router_available(self, router):
        """
        Checks whehter or not this router is available for to this router.
        A router is available if a straight line is available between the two routers, Without hitting an ice block.

        :param router: The router to acheck
        :returns: The distance of the available router if available, None otherwise.
        """
        connecting_line = LineString((self.location, router.location))
        # Only add if line is not connected
        if not any([connecting_line.crosses(iceberg) for iceberg in self.icebergs]):
            return connecting_line.length

    def find_path(self, dest_router, routers_to_use, path_traveled=None):
        """
        Finds the shortest path to a given destination router.

        :param dest_point:
        :param routers_to_use: The set of routers to use
        :return:
        """
        if path_traveled is None:
            path_traveled = [self.location]

        # A straight line is always the shortest, If available - take it.
        if self.is_router_available(dest_router):
            path_traveled.append(dest_router)
            return LineString(path_traveled)

        # TODO: This could be cached for better results,
        # Similar to a router's routing table.
        paths_found = []
        for router in routers_to_use:
            temp_routers_to_use = routers_to_use - router
            paths_found.append(router.find_path(dest_router, temp_routers_to_use, path_traveled))
        return min(paths_found, key=lambda path: path.length)
