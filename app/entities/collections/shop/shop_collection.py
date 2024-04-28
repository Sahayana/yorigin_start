from dataclasses import asdict
from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection

from app.entities.category.category_codes import CategoryCode
from app.entities.collections.geo_json import GeoJsonPoint, GeoJsonPolygon
from app.entities.collections.shop.shop_document import (
    ShopDeliveryAreaSubDocument,
    ShopDocument,
)
from app.utils.mongo import db


class ShopCollection:
    _collection = AsyncIOMotorCollection(db, "shops")

    @classmethod
    async def point_intersects(cls, point: GeoJsonPoint) -> list[ShopDocument]:
        """특정 GeoJSON Object에서 겹치는 데이터 (polygon & point)를 select"""
        return [
            cls._parse(result)
            for result in await cls._collection.find(
                {
                    "delivery_areas.poly": {
                        "$geoIntersects": {"$geometry": asdict(point)}
                    }
                }
            ).to_list(length=None)
        ]

    @classmethod
    async def insert_one(
        cls,
        name: str,
        category_codes: list[CategoryCode],
        delivery_areas: list[ShopDeliveryAreaSubDocument],
    ) -> ShopDocument:
        result = await cls._collection.insert_one(
            {
                "name": name,
                "category_codes": category_codes,
                "delivery_areas": [
                    asdict(delivery_area) for delivery_area in delivery_areas
                ],
            }
        )
        return ShopDocument(
            _id=result.inserted_id,
            name=name,
            category_codes=category_codes,
            delivery_areas=delivery_areas,
        )

    @classmethod
    def _parse(cls, result: dict[Any, Any]) -> ShopDocument:
        """
        dict을 쓰지 않고 dto로 굳이 parsing하는 이유

         - dict에는 메서드를 추가할 수 없음 (로직 캡슐화 불가능)
         - 실행하지 않고 dict 안에 무엇이 있는지 알 수 없음
         - dict은 정적 타이핑의 도움을 받을 수 없음
        """
        return ShopDocument(
            _id=result["_id"],
            name=result["name"],
            delivery_areas=[
                ShopDeliveryAreaSubDocument(
                    poly=GeoJsonPolygon(
                        coordinates=delivery_area["poly"]["coordinates"]
                    )
                )
                for delivery_area in result["delivery_areas"]
            ],
            category_codes=[
                CategoryCode(category_code)
                for category_code in result["category_codes"]
            ],
        )
