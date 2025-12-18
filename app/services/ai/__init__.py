from typing import Dict, Any, Optional
import json
from datetime import datetime
from faker import Faker

fake = Faker()


class DemoProvider:

    async def generate_response(
        self, method: str, path: str, body: Optional[Dict] = None, context: Optional[list] = None
    ) -> Dict[str, Any]:

        resource = self._extract_resource(path)

        if method == "GET":
            if self._is_collection(path):
                return self._generate_collection(resource)
            else:
                return self._generate_single(resource, path)

        elif method == "POST":
            return self._generate_created(resource, body)

        elif method == "PUT" or method == "PATCH":
            return self._generate_updated(resource, body, path)

        elif method == "DELETE":
            return self._generate_deleted(path)

        return self._generate_fallback()

    def _extract_resource(self, path: str) -> str:
        parts = path.strip("/").split("/")
        for part in parts:
            if not part.isdigit() and part not in ["api", "v1", "v2"]:
                return part
        return "items"

    def _is_collection(self, path: str) -> bool:
        parts = path.strip("/").split("/")
        return not parts[-1].isdigit()

    def _generate_collection(self, resource: str) -> Dict:
        items = [self._generate_item(resource, i) for i in range(3)]

        return {
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {resource: items, "total": len(items), "page": 1, "per_page": 10},
        }

    def _generate_single(self, resource: str, path: str) -> Dict:
        item_id = path.strip("/").split("/")[-1]

        return {
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": self._generate_item(resource, item_id),
        }

    def _generate_created(self, resource: str, body: Optional[Dict]) -> Dict:
        item = self._generate_item(resource, fake.uuid4()[:8])

        if body:
            item.update(body)

        return {"status_code": 201, "headers": {"Content-Type": "application/json"}, "body": item}

    def _generate_updated(self, resource: str, body: Optional[Dict], path: str) -> Dict:
        item_id = path.strip("/").split("/")[-1]
        item = self._generate_item(resource, item_id)

        if body:
            item.update(body)

        item["updated_at"] = datetime.utcnow().isoformat() + "Z"

        return {"status_code": 200, "headers": {"Content-Type": "application/json"}, "body": item}

    def _generate_deleted(self, path: str) -> Dict:
        return {"status_code": 204, "headers": {"Content-Type": "application/json"}, "body": {}}

    def _generate_item(self, resource: str, item_id: Any) -> Dict:
        base = {"id": str(item_id), "created_at": fake.iso8601(), "updated_at": fake.iso8601()}

        if resource in ["users", "user"]:
            base.update({"name": fake.name(), "email": fake.email(), "username": fake.user_name(), "status": "active"})
        elif resource in ["products", "product"]:
            base.update(
                {
                    "name": fake.catch_phrase(),
                    "price": round(fake.random.uniform(10, 1000), 2),
                    "currency": "USD",
                    "in_stock": fake.boolean(),
                }
            )
        elif resource in ["orders", "order"]:
            base.update(
                {
                    "total": round(fake.random.uniform(50, 500), 2),
                    "status": fake.random.choice(["pending", "completed", "cancelled"]),
                    "customer_id": fake.uuid4()[:8],
                }
            )
        else:
            base.update(
                {
                    "name": fake.word().capitalize(),
                    "description": fake.sentence(),
                    "status": fake.random.choice(["active", "inactive"]),
                }
            )

        return base

    def _generate_fallback(self) -> Dict:
        return {
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {"message": "Mock response generated", "timestamp": datetime.utcnow().isoformat() + "Z"},
        }
