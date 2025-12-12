"""
Demo AI Provider - Template-based mock generation
No API key required, generates realistic responses using Faker
"""

from typing import Dict, Any, Optional
import json
from datetime import datetime
from faker import Faker

fake = Faker()


class DemoProvider:
    """
    Template-based AI provider that generates realistic mock responses
    without requiring external AI APIs. Perfect for development and testing.
    """

    def __init__(self):
        self.fake = Faker()
        self._entity_cache = {}

    async def generate_response(
            self,
            method: str,
            path: str,
            body: Optional[Dict] = None,
            context: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Generate mock API response based on HTTP method and path

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            path: Request path (e.g., /api/v1/users)
            body: Request body (for POST/PUT/PATCH)
            context: Previous requests context for consistency

        Returns:
            Dict with status_code, headers, and body
        """
        resource = self._extract_resource(path)

        if method == "GET":
            if self._is_collection(path):
                return self._generate_collection(resource, context)
            else:
                return self._generate_single(resource, path, context)

        elif method == "POST":
            return self._generate_created(resource, body, context)

        elif method in ["PUT", "PATCH"]:
            return self._generate_updated(resource, body, path, context)

        elif method == "DELETE":
            return self._generate_deleted(path)

        return self._generate_fallback()

    def _extract_resource(self, path: str) -> str:
        """
        Extract resource name from path
        /api/v1/users/123 -> users
        /orders -> orders
        """
        parts = path.strip("/").split("/")

        filtered_parts = [
            part for part in parts
            if part not in ["api", "v1", "v2", "v3"] and not part.isdigit()
        ]

        return filtered_parts[-1] if filtered_parts else "items"

    def _is_collection(self, path: str) -> bool:
        """
        Check if path points to collection or single resource
        /users -> True (collection)
        /users/123 -> False (single)
        """
        parts = path.strip("/").split("/")
        return not parts[-1].isdigit() and not self._looks_like_id(parts[-1])

    def _looks_like_id(self, part: str) -> bool:
        """Check if string looks like an ID (uuid, short id, etc)"""
        if part.isdigit():
            return True
        if len(part) > 20 and "-" in part:
            return True
        if "_" in part and len(part) > 5:
            return True
        return False

    def _generate_collection(self, resource: str, context: Optional[list] = None) -> Dict:
        """Generate response for collection GET request"""

        created_items = self._get_created_from_context(resource, context)

        if created_items:
            items = created_items
        else:
            count = self.fake.random_int(min=3, max=5)
            items = [self._generate_item(resource, i) for i in range(count)]

        return {
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {
                resource: items,
                "total": len(items),
                "page": 1,
                "per_page": 10,
                "has_more": False
            }
        }

    def _generate_single(self, resource: str, path: str, context: Optional[list] = None) -> Dict:
        """Generate response for single resource GET request"""
        item_id = path.strip("/").split("/")[-1]

        if context:
            for req in reversed(context):
                if req.get("method") == "POST" and resource in req.get("path", ""):
                    response_body = req.get("response", {}).get("body", {})
                    if response_body.get("id") == item_id:
                        return {
                            "status_code": 200,
                            "headers": {"Content-Type": "application/json"},
                            "body": response_body
                        }

        return {
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": self._generate_item(resource, item_id)
        }

    def _generate_created(self, resource: str, body: Optional[Dict], context: Optional[list] = None) -> Dict:
        """Generate response for POST (create) request"""
        item = self._generate_item(resource, self.fake.uuid4()[:8])

        if body:
            generated_fields = {
                "id": item["id"],
                "created_at": item["created_at"],
                "updated_at": item["updated_at"]
            }
            item = {**body, **generated_fields}

        return {
            "status_code": 201,
            "headers": {
                "Content-Type": "application/json",
                "Location": f"/{resource}/{item['id']}"
            },
            "body": item
        }

    def _generate_updated(self, resource: str, body: Optional[Dict], path: str, context: Optional[list] = None) -> Dict:
        """Generate response for PUT/PATCH (update) request"""
        item_id = path.strip("/").split("/")[-1]

        existing_item = None
        if context:
            for req in reversed(context):
                if req.get("method") in ["POST", "GET"] and item_id in req.get("path", ""):
                    existing_item = req.get("response", {}).get("body", {})
                    break

        if existing_item:
            item = existing_item.copy()
        else:
            item = self._generate_item(resource, item_id)

        if body:
            item.update(body)

        item["updated_at"] = datetime.utcnow().isoformat() + "Z"

        return {
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": item
        }

    def _generate_deleted(self, path: str) -> Dict:
        """Generate response for DELETE request"""
        return {
            "status_code": 204,
            "headers": {"Content-Type": "application/json"},
            "body": {}
        }

    def _generate_item(self, resource: str, item_id: Any) -> Dict:
        """
        Generate a single item based on resource type
        Uses realistic data based on common resource patterns
        """
        base = {
            "id": str(item_id),
            "created_at": self.fake.iso8601(),
            "updated_at": self.fake.iso8601()
        }

        if resource in ["users", "user", "accounts", "profiles"]:
            base.update({
                "name": self.fake.name(),
                "email": self.fake.email(),
                "username": self.fake.user_name(),
                "avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={item_id}",
                "status": self.fake.random_element(["active", "inactive", "pending"]),
                "role": self.fake.random_element(["admin", "user", "moderator"])
            })

        elif resource in ["products", "product", "items", "goods"]:
            base.update({
                "name": self.fake.catch_phrase(),
                "description": self.fake.text(max_nb_chars=100),
                "price": round(self.fake.random.uniform(10, 1000), 2),
                "currency": "USD",
                "sku": self.fake.bothify(text='???-########'),
                "in_stock": self.fake.boolean(chance_of_getting_true=80),
                "stock_quantity": self.fake.random_int(min=0, max=100),
                "category": self.fake.random_element(["Electronics", "Clothing", "Food", "Books"])
            })

        elif resource in ["orders", "order", "purchases"]:
            base.update({
                "order_number": self.fake.bothify(text='ORD-########'),
                "total": round(self.fake.random.uniform(50, 500), 2),
                "currency": "USD",
                "status": self.fake.random_element(["pending", "processing", "completed", "cancelled"]),
                "customer_id": f"usr_{self.fake.uuid4()[:8]}",
                "items_count": self.fake.random_int(min=1, max=5),
                "shipping_address": {
                    "street": self.fake.street_address(),
                    "city": self.fake.city(),
                    "country": self.fake.country()
                }
            })

        elif resource in ["posts", "post", "articles", "blog"]:
            base.update({
                "title": self.fake.sentence(nb_words=6),
                "content": self.fake.text(max_nb_chars=500),
                "author": self.fake.name(),
                "author_id": f"usr_{self.fake.uuid4()[:8]}",
                "slug": self.fake.slug(),
                "published": self.fake.boolean(chance_of_getting_true=70),
                "views": self.fake.random_int(min=0, max=10000),
                "likes": self.fake.random_int(min=0, max=1000)
            })

        elif resource in ["comments", "comment", "reviews"]:
            base.update({
                "text": self.fake.text(max_nb_chars=200),
                "author": self.fake.name(),
                "author_id": f"usr_{self.fake.uuid4()[:8]}",
                "rating": self.fake.random_int(min=1, max=5),
                "likes": self.fake.random_int(min=0, max=100)
            })

        elif resource in ["tasks", "task", "todos", "todo"]:
            base.update({
                "title": self.fake.sentence(nb_words=5),
                "description": self.fake.text(max_nb_chars=150),
                "status": self.fake.random_element(["todo", "in_progress", "done"]),
                "priority": self.fake.random_element(["low", "medium", "high", "urgent"]),
                "assigned_to": f"usr_{self.fake.uuid4()[:8]}",
                "due_date": self.fake.future_date(end_date="+30d").isoformat()
            })

        elif resource in ["events", "event", "meetings"]:
            base.update({
                "title": self.fake.sentence(nb_words=4),
                "description": self.fake.text(max_nb_chars=200),
                "start_time": self.fake.future_datetime(end_date="+30d").isoformat() + "Z",
                "end_time": self.fake.future_datetime(end_date="+30d").isoformat() + "Z",
                "location": self.fake.address(),
                "organizer": self.fake.name(),
                "attendees_count": self.fake.random_int(min=1, max=100)
            })

        elif resource in ["companies", "company", "organizations"]:
            base.update({
                "name": self.fake.company(),
                "industry": self.fake.random_element(["Technology", "Finance", "Healthcare", "Retail"]),
                "employees_count": self.fake.random_int(min=10, max=10000),
                "website": self.fake.url(),
                "email": self.fake.company_email(),
                "phone": self.fake.phone_number(),
                "address": {
                    "street": self.fake.street_address(),
                    "city": self.fake.city(),
                    "country": self.fake.country()
                }
            })

        else:
            base.update({
                "name": self.fake.word().capitalize(),
                "description": self.fake.sentence(),
                "status": self.fake.random_element(["active", "inactive", "pending"]),
                "type": resource.rstrip('s'),
                "value": round(self.fake.random.uniform(1, 100), 2)
            })

        return base

    def _generate_fallback(self) -> Dict:
        """Generate generic fallback response"""
        return {
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {
                "message": "Mock response generated by Helix",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "provider": "demo"
            }
        }

    def _get_created_from_context(self, resource: str, context: Optional[list]) -> list:
        """Extract created items from context for consistency"""
        if not context:
            return []

        created_items = []
        for req in context:
            if req.get("method") == "POST" and resource in req.get("path", ""):
                response_body = req.get("response", {}).get("body", {})
                if response_body and isinstance(response_body, dict):
                    created_items.append(response_body)

        return created_items