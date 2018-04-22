import logging

import numpy as np
from polytree.xy import Coord

LOGGER = logging.getLogger("label.py")

def label_location(start, end, distance=0.1):
    """
    Instead of figuring out where the line is in space, we bring the line
    to very regular rescaled coordinates. Then we add the label there, where
    it's easy to figure out, and we rotate it back to wherever it started.
    """
    (xa, ya) = start.as_tuple()
    (xb, yb) = end.as_tuple()

    # Three dimensions so we use "homogeneous coordinates."
    columnar = np.matrix([
        [xa, xb],
        [ya, yb],
        [ 1,  1]
        ])
    LOGGER.debug(f"initial a, b\n{columnar}")
    # This transformation matrix is a translation matrix.
    x_to_zero = np.matrix([
        [1, 0, -xa],
        [0, 1, -ya],
        [0, 0,   1]
        ])
    at_zero = np.matmul(x_to_zero, columnar)
    LOGGER.debug(f"translated\n{at_zero}")
    LOGGER.debug(f"translated a {at_zero[:, 0].T}")
    assert np.allclose(at_zero[:, 0].T, [[0, 0, 1]])

    bx, by = at_zero[0, 1], at_zero[1, 1]
    LOGGER.debug(f"bx {bx} by {by}")
    r = np.sqrt(bx**2 + by**2)
    # This transformation matrix is a rotation matrix.
    rotate_to_x_axis = np.matrix([
        [ bx / r,  by / r, 0],
        [-by / r,  bx / r, 0],
        [       0,      0, 1]
        ])
    LOGGER.debug(f"rot matrix\n{rotate_to_x_axis}")
    
    on_axis = np.matmul(rotate_to_x_axis, np.array([bx, by, 1]))
    LOGGER.debug(f"on_axis {on_axis}")
    assert np.allclose(on_axis[0, 0], r)
    assert np.allclose(on_axis[0, 1], 0)

    label_scaled = np.matrix([[0.5 * r, distance, 1]]).T
    LOGGER.debug(f"place label\n{label_scaled}")

    # inverse is the transpose of the matrix, which means "undo."
    rotated_back = np.matmul(
            np.linalg.inv(rotate_to_x_axis),
            label_scaled
            )
    LOGGER.debug(f"rotated back\n{rotated_back}")

    label_absolute = np.matmul(
        np.linalg.inv(x_to_zero),
        rotated_back
        )
    LOGGER.debug(f"label_abs\n{label_absolute}")

    return label_absolute[0, 0], label_absolute[1, 0]

def label_loc_xy(start, end, distance=0.1):
    #TODO should be doing the single-default thing
    x, y = label_location(start, end, distance)

    #HELP which method?
    return Coord(int(round(x)), round(float(y)))

def test_label():
    assert np.allclose(label_location(Coord(0, 0), Coord(1, 0)), (0.5, 0.1))
    assert np.allclose(label_location(Coord(0, 1), Coord(1, 1)), (0.5, 1.1))
    assert np.allclose(label_location(Coord(0, 1), Coord(0, 2)), (-0.1, 1.5))
    assert np.allclose(label_location(Coord(1, 1), Coord(0, 1)), (0.5, 0.9))
    assert np.allclose(label_location(Coord(0, 0), Coord(2, 0)), (1, 0.1))
    print(label_location(Coord(23, 89), Coord(45, 187), 10))
    print()
    print(label_location(Coord(23, 89), Coord(45, 187), -10))
    print(label_location(Coord(45, 187),Coord(23,89)))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_label()
