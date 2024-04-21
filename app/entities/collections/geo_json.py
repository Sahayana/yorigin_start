import dataclasses
from typing import Literal, Sequence


# 배달 구역을 지도 위에 그리는데 사용
@dataclasses.dataclass(kw_only=True)
class GeoJsonPolygon:
    coordinates: Sequence[Sequence[Sequence[float]]]
    type: Literal["Polygon"] = "Polygon"


# 유저의 위치를 지도 위에 그리는데 사용
@dataclasses.dataclass(kw_only=True)
class GeoJsonPoint:
    coordinates: Sequence[float]
    type: Literal["Point"] = "Point"
