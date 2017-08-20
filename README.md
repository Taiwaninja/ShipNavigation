# ShipNavigation
A simple ship navigation exercise

# About the algorithm:
This solution is much inspired by Network routing protocols, With some assumptions that are relevant in our case:

# Assumptions:
1) We assume a straight line is the fastest route between any two points, If available.
2) We assume there is no reason to turn if no iceberg is in the way,
    This is true because
    a) If no iceberg is in the way - we can take a straight line.
    b) If an iceberg IS in the way, the shortest path around is is through one of the vertices. Because:
        * For a turning point that is not on the iceberg - We can find a less curved way through one of the vertices.
        * For a point on the iceberg that is not a vertex -
          We either cant get around the iceberg in 1 straight line(And we will be blocked, Rather go through a vertex)
          or, Could have a less curved way through one.

# The algorithm:
1) If we can take a straight line - We take it!
2) Start with a given set of potential routers
3) For each router that we can connect to in a straight line:
    3.1) Connect there, And exclude it from potential routers to connect
    3.2) Repeat stage 2 with path already made, to get all potential paths.
    (P.s. We exclude a router permanently from same sub route because a->b will always be shorter than a->c->b,
    Straight line is always the fastest!)
    3.3) Choose shortest path and return it!

# Notes:
The program could be improved by introducing a caching algorithm if more than 1 decision is needed.
This is not the case and there may be an algorithm that for 1 run reaches the same conclusion with less computations.
This is chosen to be implemented this way because it's more extensible.