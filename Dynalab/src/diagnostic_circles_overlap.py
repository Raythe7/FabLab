#!/usr/bin/env python
from gettext import gettext as _
import math

import inkex

from lib import dynalab
from lib.dynalab import WARNING


# Test if two bounding boxes overlap
def bbox_overlap(a, b):
    overlap = not (
        a.right < b.left
        or b.right < a.left
        or a.bottom < b.top
        or b.bottom < a.top
    )

    return overlap


# Approximates an ellipse by a polygon with n points
def ellipse_polygon(cx, cy, rx, ry, n=48):
    pts = []
    for k in range(n):
        t = 2.0 * math.pi * k / n
        pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    return pts


# Return the bounding box of a polygon
def polygon_bbox(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]

    xmin = min(xs)
    ymin = min(ys)
    xmax = max(xs)
    ymax = max(ys)

    bbox = inkex.BoundingBox.new_xywh(xmin, ymin, xmax - xmin, ymax - ymin)

    return bbox


# Calculate the orientation of three points
def orient(a, b, c):
    value = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return value


# Test if a point "p" lies on the segment "[a,b]" with a tolerance "eps"
def on_segment(a, b, p, eps):
    on_seg = ( min(a[0], b[0]) - eps <= p[0] <= max(a[0], b[0]) + eps 
              and min(a[1], b[1]) - eps <= p[1] <= max(a[1], b[1]) + eps
              )
    return on_seg


# Determine if two segments "[a,b]" and "[c,d]" intersect
def segments_intersect(a, b, c, d, eps):
    o1 = orient(a, b, c)
    o2 = orient(a, b, d)
    o3 = orient(c, d, a)
    o4 = orient(c, d, b)
    intersect = False

    if (((o1 > eps and o2 < -eps) or (o1 < -eps and o2 > eps))
            and ((o3 > eps and o4 < -eps) or (o3 < -eps and o4 > eps))):
        intersect = True

    if abs(o1) <= eps and on_segment(a, b, c, eps):
        intersect = True

    if abs(o2) <= eps and on_segment(a, b, d, eps):
        intersect = True

    if abs(o3) <= eps and on_segment(c, d, a, eps):
        intersect = True

    if abs(o4) <= eps and on_segment(c, d, b, eps):
        intersect = True

    return intersect


# Test if a point is inside a polygon
def point_in_polygon(pt, poly):
    x, y = pt
    n = len(poly)
    inside = False

    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        if (y1 > y) != (y2 > y):
            xinters = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            
            if x < xinters:
                inside = not inside

    return inside


# Build the transformed polygon of a circle/ellipse
def transformed_shape_polygon(elem, npts):
    poly = None

    if isinstance(elem, inkex.Circle):
        cx = float(elem.get("cx", "0"))
        cy = float(elem.get("cy", "0"))
        r = float(elem.get("r", "0"))
        poly = ellipse_polygon(cx, cy, r, r, n=npts)

    elif isinstance(elem, inkex.Ellipse):
        cx = float(elem.get("cx", "0"))
        cy = float(elem.get("cy", "0"))
        rx = float(elem.get("rx", "0"))
        ry = float(elem.get("ry", "0"))
        poly = ellipse_polygon(cx, cy, rx, ry, n=npts)

    if poly is not None:
        tr = elem.composed_transform()
        transformed = []

        for x, y in poly:
            p = tr.apply_to_point((x, y))
            transformed.append((p.x, p.y))

        poly = transformed

    return poly


class MarkCircleOverlaps(dynalab.Ext):
    """
    detect circle/ellipse overlaps with transforms applied
    """
    name = _("detect circle/ellipse overlaps")

    def add_arguments(self, pars):
        super().add_arguments(pars)

    # Build a table containing transformed shapes
    def build_transformed_shapes(self, npts):
        data = []

        for elem in self.selected_or_all(skip_groups=True):
            if isinstance(elem, (inkex.Circle, inkex.Ellipse)):
                poly = transformed_shape_polygon(elem, npts)

                if poly is not None:
                    bb = polygon_bbox(poly)

                    data.append(
                        {
                            "elem": elem,
                            "id": elem.get_id(),
                            "poly": poly,
                            "bbox": bb,
                        }
                    )

        return data

    # Mark the two objects involved in an overlap
    def mark_overlap(self, bb1, bb2, id1, id2, message_text):
        msg = _(message_text).format(id1=id1, id2=id2)
        self.outline_bounding_box(WARNING, None, bb=bb1, msg=msg)
        self.outline_bounding_box(WARNING, None, bb=bb2, msg=msg)

    def effect(self, clean=True):
        self.message(self.name, verbosity=3)
        self.init_artifact_layer()


        eps = 1e-6
        npts = 48

        data = self.build_transformed_shapes(npts)

        self.message(_("Ellipses found: {n}").format(n=len(data)), verbosity=1)

        found = 0
        m = len(data)

        for i in range(m):
            s1 = data[i]
            id1 = s1["id"]
            bb1 = s1["bbox"]
            p1 = s1["poly"]

            for j in range(i + 1, m):
                s2 = data[j]
                id2 = s2["id"]
                bb2 = s2["bbox"]
                p2 = s2["poly"]

                if not bbox_overlap(bb1, bb2):
                    continue

                inter = 0

                for a in range(len(p1)):
                    a1 = p1[a]
                    a2 = p1[(a + 1) % len(p1)]

                    for b in range(len(p2)):
                        b1 = p2[b]
                        b2 = p2[(b + 1) % len(p2)]

                        if segments_intersect(a1, a2, b1, b2, eps):
                            inter += 1

                            if inter >= 2:
                                break

                    if inter >= 2:
                        break

                if inter >= 2:
                    found += 1
                    self.mark_overlap(
                        bb1,
                        bb2,
                        id1,
                        id2,
                        "Ellipse overlap detected: {id1} and {id2}",
                    )
                    continue

                if point_in_polygon(p1[0], p2) or point_in_polygon(p2[0], p1):
                    found += 1
                    self.mark_overlap(
                        bb1,
                        bb2,
                        id1,
                        id2,
                        "Ellipse overlap detected: {id1} and {id2}",
                    )

        if clean:
            self.clean_artifacts(force=False)

        self.message(_("Overlapping ellipse pairs found: {n}").format(n=found), verbosity=1)


if __name__ == "__main__":
    MarkCircleOverlaps().run()