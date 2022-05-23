from eudplib import *
from operator import itemgetter
from heapq import heappush, heappop
from math import gcd, cos, sin, radians, pi, sqrt
from functools import reduce


def ScannerImage(image):
    try:
        return SetMemoryX(0x666458, SetTo, EncodeImage(image), 65535)
    except NameError:
        return SetMemoryX(0x666458, SetTo, image, 65535)


def Loc(location):
    if Painter._loc is None:
        Painter._loc = EncodeLocation(location)
    else:
        raise EPError("draw.Loc(TrgLocation) 은 1번만 지정할 수 있습니다")


def coprime(a, b):
    return gcd(a, b) == 1


def rotate(x, y, theta):
    return x * cos(theta) - y * sin(theta), x * sin(theta) + y * cos(theta)


def _try(x, f):
    if isinstance(x, str):
        return x
    try:
        return f(x)
    except TypeError:
        return x


def _lcmlen(*args):
    def trylen(x):
        if isinstance(x, str):
            return 1
        try:
            return len(x)
        except TypeError:
            return 1

    def lcm(a, b):
        return trylen(a) * trylen(b) // gcd(trylen(a), trylen(b))

    return reduce(lcm, args)


def _key(*args):
    return tuple(map(lambda x: _try(x, tuple), args))


def _wrap(i, *args):
    return tuple(_try(x, lambda a: a[i % len(a)]) for x in args)


def _create_unit(unit, loc, player, properties=None):
    unit, loc, player = EncodeUnit(unit), EncodeLocation(loc), EncodePlayer(player)
    ep_assert(all(IsConstExpr(arg) for arg in (unit, loc, player)))
    if properties is None:
        return CreateUnit(1, unit, loc, player)
    return CreateUnitWithProperties(1, unit, loc, player, properties)


def _move_loc(actions, location, *pairs):
    ep_assert(IsConstExpr(location))
    epd = EPD(0x58DC4C) + 5 * location
    for offset, value in pairs:
        if value > 0:
            actions.append(SetMemoryEPD(epd + offset, Add, value))
        elif value < 0:
            actions.append(SetMemoryEPD(epd + offset, Subtract, -value))


class LinePath:
    def __init__(self, *points, closed=False, rotation=0):
        self.points = [rotate(*xy, radians(rotation)) for xy in points]
        if closed:
            self.points.append(self.points[0])
        self.lengths = [0.0]
        length = 0
        for i in range(len(self.points) - 1):
            x0, y0, x, y = *self.points[i], *self.points[i + 1]
            length += sqrt((x - x0) ** 2 + (y - y0) ** 2)
            self.lengths.append(length)

    def interpolate(self, length):
        if not (0 <= length < self.lengths[-1]):
            raise ValueError(
                f"Interpolate length ({length}) must be less than line length ({self.lengths[-1]})"
            )
        n = next((i - 1 for i, x in enumerate(self.lengths) if length < x), 0)
        x0, y0, x1, y1 = *self.points[n], *self.points[n + 1]
        length -= self.lengths[n]
        total_length = self.lengths[n + 1] - self.lengths[n]
        x = x0 + length * (x1 - x0) / total_length
        y = y0 + length * (y1 - y0) / total_length
        return (int(round(x)), int(round(y)))


class Painter:
    _loc = None

    def __init__(self, center, radius, rotation=0, translation=(0, 0), **kwargs):
        self.center = EncodeLocation(center)
        self.radius, self.rotation = float(radius), float(rotation)
        if len(translation) != 2:
            raise ValueError(f"translation ({translation}) must be (x, y) pair")
        self.translation = tuple(map(float, translation))
        self._items = None
        self._draw_to_dict = {}
        self.dotno = 0
        if kwargs:
            self.update(kwargs)
        else:  # FIXME: better default kwargs
            self.update({"spacing": 32})

    def perimeter(self):
        raise NotImplementedError

    def path(self):
        raise NotImplementedError

    def key(self):
        return (self.radius, self.rotation, self.spacing, self.dotno)

    def update(self, props):
        """Update painter's properties from the dict *props*.

        Args:
            props (dict)
        """
        for k, v in props.items():
            func = getattr(self, f"set_{k}", None)
            if not callable(func):
                raise AttributeError(
                    f"{type(self).__name__!r} object has no property {k!r}"
                )
            func(v)

    def set_dots(self, dots):
        if not isinstance(dots, int):
            raise TypeError(f"dots must be int, not {type(dots)}")
        if dots < 1:
            raise ValueError(f"dots ({dots}) must be positive int")
        self.dots = dots
        self.spacing = self.perimeter() / dots

    def set_spacing(self, spacing):
        if spacing <= 0:
            raise ValueError(f"spacing ({spacing}) must be positive float")
        if spacing >= self.perimeter():
            raise ValueError(
                f"spacing ({spacing}) must be less than perimeter ({self.perimeter()})"
            )
        self.dots = int(self.perimeter() / spacing)
        self.spacing = spacing

    def set_dotno(self, dotno):
        if not isinstance(dots, int):
            raise TypeError(f"dotno must be int, not {type(dotno)}")
        if dotno < 0:
            raise ValueError(f"dotno ({dotno}) must be zero or positive int")
        self.dotno = dotno

    def _get_items(self):
        if self._items is None:
            path = self.path()
            x, y = list(), list()
            length = 0
            xmask, ymask = 0, 0
            ox, oy = self.translation
            while length < self.perimeter():
                tx, ty = path.interpolate(length)
                tx += ox
                ty += oy
                xmask |= tx & 0xFFFFFFFF
                ymask |= ty & 0xFFFFFFFF
                x.append(tx & 0xFFFFFFFF)
                y.append(ty & 0xFFFFFFFF)
            vx, vy = EUDArray(x), EUDArray(y)
            self._items = (x, y, vx, vy, xmask, ymask)
        return self._items

    def __getitem__(self, index):
        xlist, ylist, vx, vy, xmask, ymask = self._get_items()
        if IsEUDVariable(index):
            Trigger(index.AtLeast(self.dots), index.SetNumber(self.dots - 1))
            x = f_maskread_epd(EPD(vx) + index, xmask)
            y = f_maskread_epd(EPD(vy) + index, ymask)
        else:
            if index >= self.dots:
                raise ValueError(
                    f"index ({index}) must be less than dots ({self.dots})"
                )
            x, y = xlist[index], ylist[index]
        return (x, y)

    def _fastmoveloc(self, offset, points, v1, v2, nv, dv):
        # action count optimization...
        # 4 borders of location must be within radius
        border = max(self.radius, 450)
        if -border <= v1 + 2 * dv:
            return v1 + 2 * dv, v2, ((offset, 2 * dv),)
        if -border <= v2 + 2 * dv:
            return v1, v2 + 2 * dv, ((offset + 2, 2 * dv),)
        if points and -border <= 2 * nv - points[0][offset]:
            xv = points[0][offset]
            return xv, 2 * nv - xv, ((offset, xv - v1), (offset + 2, 2 * nv - xv - v2))
        if not points and -border <= 2 * nv:
            return 0, 2 * nv, ((offset, -v1), (offset + 2, 2 * nv - v2))
        return nv, nv, ((offset, nv - v1), (offset + 2, nv - v2))

    def draw(self, unit="Scanner Sweep", player=P8, properties=None):
        """모양대로 유닛으로 그립니다.

        Args:
            unit (TrgUnit or lambda, optional): 유닛, 기본 Scanner Sweep
            player (TrgPlayer or lambda, optional): 플레이어, 기본 P8
            properties (UnitProperty or lambda, optional): 유닛 프로퍼티
        """

        def _to_callable(f):
            if callable(f):
                return f
            return lambda _: f

        unitf = _to_callable(unit)
        playerf = _to_callable(player)
        propf = _to_callable(properties)
        actions, points = list(), list()
        path = self.path()
        length = 0
        ox, oy = self.translation
        for i in range(self.dots):
            x, y = path.interpolate(i * self.spacing)
            heappush(
                points,
                (x + ox, y + oy, unitf(i), playerf(i), propf(i)),
            )
        moveloc = lambda *pairs: _move_loc(actions, self.center, *pairs)

        x0, y0 = 0, 0
        l, u, r, d = 0, 0, 0, 0
        for i in range(len(points)):
            x, y, unit, player, properties = heappop(points)
            if x == x0 and y == y0:
                continue
            dx, dy = x - x0, y - y0
            l, r, pairs = self._fastmoveloc(0, points, l, r, x, dx)
            moveloc(*pairs)
            u, d, pairs = self._fastmoveloc(1, points, u, d, y, dy)
            moveloc(*pairs)
            actions.append(_create_unit(unit, self.center, player, properties))
            x0, y0 = x, y
        moveloc((0, -l), (1, -u), (2, -r), (3, -d))
        DoActions(actions)


def RegularPolygon(center, vertices, radius, rotation=0, translation=(0, 0), **kwargs):
    """정다각형

    Args:
        center (TrgLocation or (x, y) pair): 중심 로케이션 또는 좌표
        vertices (int): 꼭짓점의 개수
        radius (float): 중심과 꼭짓점 사이 거리
        rotation (float, optional): 회전 각도 (360도)
        translation (pair of float, optional): 평행이동
        **kwargs
            dots (int): 점의 개수
            spacing (float): 간격. 기본=32
    """
    return RegularStar(center, vertices, 1, radius, rotation, translation, **kwargs)


class CirclePath:
    def __init__(self, radius, rotation):
        self.radius, self.rotation = radius, rotation
        self.perimeter = 2 * pi * radius

    def interpolate(self, length):
        if not (0 <= length < self.perimeter):
            raise ValueError(
                f"arc length ({length}) must be less than perimeter ({self.perimeter})"
            )
        x, y = rotate(0, -self.radius, length / self.radius + self.rotation)
        return (int(round(x)), int(round(y)))


class Circle(Painter):
    """원

    Args:
        center (TrgLocation or (x, y) pair): 중심 로케이션 또는 좌표
        radius (float): 중심과 꼭짓점 사이 거리
        rotation (float, optional): 회전 각도 (360도)
        translation (pair of float, optional): 평행이동
        **kwargs
            dots (int): 점의 개수
            spacing (float): 간격. 기본=32
    """

    def __init__(self, center, radius, rotation=0, translation=(0, 0), **kwargs):
        super().__init__(center, radius, rotation, translation, **kwargs)

    def perimeter(self):
        return 2 * pi * self.radius

    def path(self):
        return CirclePath(self.radius, self.rotation)


class RegularStar(Painter):
    """정다각별

    Args:
        center (TrgLocation or (x, y) pair): 중심 로케이션 또는 좌표
        vertices (int): 꼭짓점의 개수
        density (int): 밀도, 꼭짓점과 서로소
        radius (float): 중심과 꼭짓점 사이 거리
        rotation (float, optional): 회전 각도 (360도)
        translation (pair of float, optional): 평행이동
        **kwargs
            dots (int): 점의 개수
            spacing (float): 간격. 기본=32
    """

    def __init__(
        self,
        center,
        vertices,
        density,
        radius,
        rotation=0,
        translation=(0, 0),
        **kwargs,
    ):
        if vertices <= 2 * density:
            raise ValueError(
                f"density ({density}) must be less than half of vertices ({vertices})"
            )
        self.vertices = vertices
        self.density = density
        super().__init__(center, radius, rotation, translation, **kwargs)

    def side_length(self):
        p, q = self.vertices, self.density
        return self.radius * sin(2 * q / p * pi) / sin((p - 2 * q) / (2 * p) * pi)

    def perimeter(self):
        return self.vertices * self.side_length()

    def path(self):
        points = list()
        x0, y0 = 0, -self.radius
        angle = radians(360 * self.density / self.vertices)
        for n in range(self.vertices):
            points.append(rotate(x0, y0, n * angle))
        return LinePath(*points, closed=True, rotation=self.rotation)

    def key(self):
        return (self.vertices, self.density) + super().key()

    def draw(self, unit="Scanner Sweep", player=P8, properties=None):
        """별 모양대로 유닛을 그립니다.

        Args:
            unit (TrgUnit or lambda, optional): 유닛, 기본 Scanner Sweep
            player (TrgPlayer or lambda, optional): 플레이어, 기본 P8
            properties (UnitProperty or lambda, optional): 유닛 프로퍼티
        """
        if coprime(self.vertices, self.density):
            return super().draw(unit, player, properties)

        def substar(n):
            return RegularStar(
                self.center,
                self.vertices // gcd(self.vertices, self.density),
                self.density // gcd(self.vertices, self.density),
                self.radius,
                self.rotation + n * 360 / self.vertices,
                self.translation,
                spacing=self.spacing,
            )

        for n in range(self.density):
            substar(n).draw(unit, player, properties)


class ConcaveStar(Painter):
    """오목별

    Args:
        center (TrgLocation or (x, y) pair): 중심 로케이션 또는 좌표
        vertices (int): 꼭짓점의 개수
        density (int): 밀도, 꼭짓점과 서로소
        radius (float): 중심과 꼭짓점 사이 거리
        rotation (float, optional): 회전 각도 (360도)
        translation (pair of float, optional): 평행이동
        **kwargs
            dots (int): 점의 개수
            spacing (float): 간격. 기본=32
    """

    def __init__(
        self,
        center,
        vertices,
        density,
        radius,
        rotation=0,
        translation=(0, 0),
        **kwargs,
    ):
        if vertices <= 2 * density:
            raise ValueError(
                f"density ({density}) must be less than half of vertices ({vertices})"
            )
        self.vertices = vertices
        self.density = density
        super().__init__(center, radius, rotation, translation, **kwargs)

    def side_length(self):
        n, d = self.vertices, self.density
        return self.radius * sin(pi / n) / sin(radians(90 + 180 * d / n - 180 / n))

    def perimeter(self):
        return 2 * self.vertices * self.side_length()

    def path(self):
        n, d = self.vertices, self.density
        points = list()
        angle = radians(360 / n)
        t = (
            self.radius
            * sin(radians(90 * (n - 2 * d) / n))
            / sin(radians(180 * (n - 1) / n - 90 * (n - 2 * d) / n))
        )
        x0, y0 = 0, -self.radius
        x1, y1 = rotate(0, -t, pi / n)
        for n in range(n):
            points.append(rotate(x0, y0, n * angle))
            points.append(rotate(x1, y1, n * angle))
        return LinePath(*points, closed=True, rotation=self.rotation)


def process_points(points, scale):
    radius = 0
    npoints = []
    for x, y in points:
        nx, ny = x * scale, -y * scale
        npoints.append((nx, ny))
        if radius < abs(nx):
            radius = abs(nx)
        if radius < abs(ny):
            radius = abs(ny)
    return npoints, radius


class Line(Painter):
    """꺾은선

    Args:
        center (TrgLocation or (x, y) pair): 중심 로케이션 또는 좌표
        *points (pair of float):
        scale (float, optional): 배율
        rotation (float, optional): 회전 각도 (360도)
        translation (pair of float, optional): 평행이동
        **kwargs
            dots (int): 점의 개수
            spacing (float): 간격. 기본=32
    """

    def __init__(
        self, center, *points, scale=1, rotation=0, translation=(0, 0), **kwargs
    ):
        self.points, radius = process_points(points, scale)
        super().__init__(center, radius, rotation, translation, **kwargs)

    def path(self):
        return LinePath(
            *self.points,
            closed=False,
            rotation=self.rotation,
        )

    def perimeter(self):
        return self.path().lengths[-1]


class Polygon(Painter):
    """다각형

    Args:
        center (TrgLocation): 중심 로케이션
        *points (pair of float):
        scale (float, optional): 배율
        rotation (float, optional): 회전 각도 (360도)
        translation (pair of float, optional): 평행이동
        **kwargs
            dots (int): 점의 개수
            spacing (float): 간격. 기본=32
    """

    def __init__(
        self, center, *points, scale=1, rotation=0, translation=(0, 0), **kwargs
    ):
        self.points, radius = process_points(points, scale)
        super().__init__(center, radius, rotation, translation, **kwargs)

    def path(self):
        return LinePath(*self.points, closed=True, rotation=self.rotation)

    def perimeter(self):
        return self.path().lengths[-1]
