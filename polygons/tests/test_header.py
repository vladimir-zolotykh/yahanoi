import sys
import subprocess
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


def run_polysmeta(*args):
    return subprocess.run(
        args,
        text=True,
        check=True,
        capture_output=True,
    ).stdout


def test_polysmeta():
    assert (
        run_polysmeta(sys.executable, "polysmeta.py", "--iter-as", "<dd")
        == """\
magic=4660, box=Box(p1=Point(x=0.5, y=0.5), p2=Point(x=7.0, y=9.2)), num_polys=3
(1.0, 2.5)
(3.5, 4.0)
(2.5, 1.5)
(7.0, 1.2)
(5.1, 3.0)
(0.5, 7.5)
(0.8, 9.0)
(3.4, 6.3)
(1.2, 0.5)
(4.6, 9.2)
"""
    )

    assert (
        run_polysmeta(sys.executable, "polysmeta.py", "--iter-as", "Point")
        == """\
magic=4660, box=Box(p1=Point(x=0.5, y=0.5), p2=Point(x=7.0, y=9.2)), num_polys=3
Point(x=1.0, y=2.5)
Point(x=3.5, y=4.0)
Point(x=2.5, y=1.5)
Point(x=7.0, y=1.2)
Point(x=5.1, y=3.0)
Point(x=0.5, y=7.5)
Point(x=0.8, y=9.0)
Point(x=3.4, y=6.3)
Point(x=1.2, y=0.5)
Point(x=4.6, y=9.2)
"""
    )
