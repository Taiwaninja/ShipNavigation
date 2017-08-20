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
        :returns: Whether or not a straight line is available between the two routers.
        """
        connecting_line = LineString([self.location, router.location])
        # Only add if line is not connected
        if not any([connecting_line.crosses(iceberg) for iceberg in self.icebergs]):
            return True
        return False

    def find_path(self, dest_router, routers_to_use, path_traveled=None):
        """
        Finds the shortest path to a given destination router.

        :param dest_point: The destination point we are aiming to reach.
        :param routers_to_use: The set of routers to use
        :return: The shortest path to the destination if found, None otherwise.
        """
        if path_traveled is None:
            path_traveled = []

        # Append self to path traveled
        path_traveled = path_traveled + [self.location]

        # A straight line is always the shortest, If available - take it.
        if self.is_router_available(dest_router):
            path_traveled.append(dest_router.location)
            return LineString(path_traveled)

        # TODO: This could be cached for better results,
        # Similar to a router's routing table.
        paths_found = []
        temp_routers_to_use = routers_to_use
        for router in routers_to_use:
            # We can't use a non available router - Ignore it.
            if not self.is_router_available(router):
                continue
            # Remove every router we check from current, And further mapping.
            # This is because all connections are by geographic distance, And the shortest path is a straight line
            # So we will never fight a shortest path to a given router then the straight line -
            # No point in including it any further.
            temp_routers_to_use = temp_routers_to_use - {router}
            path_found = router.find_path(dest_router, temp_routers_to_use, path_traveled)
            if path_found is not None:
                paths_found.append(path_found)
        if not paths_found:
            return None
        return min(paths_found, key=lambda path: path.length)
