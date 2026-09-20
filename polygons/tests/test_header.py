from polygons import write_polys as WP
from polygons.polysmeta import Point, Box, Header


def test_point():
    p = Point.from_args(10.1, 20.2)
    assert str(p) == "Point(x=10.1, y=20.2)"


def test_box():
    b = Box.from_args(Point.from_args(10.1, 20.2), Point.from_args(10.1, 20.2))
    assert str(b) == "Box(p1=Point(x=10.1, y=20.2), p2=Point(x=10.1, y=20.2))"


def test_header():
    h0 = WP.Header.default()
    b0 = h0.box
    h = Header.from_args(
        h0.magic,
        Box.from_args(
            Point.from_args(b0.p1.x, b0.p1.y), Point.from_args(b0.p2.x, b0.p2.y)
        ),
        h0.num_polys,
    )
    assert str(h) == (
        "Header(magic=4660, "
        "box=Box(p1=Point(x=0.5, y=0.5), p2=Point(x=7.0, y=9.2)), "
        "num_polys=3)"
    )
