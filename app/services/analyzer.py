class RequestAnalyzer:
    def extract_resource(self, path: str) -> str:
        """Extract resource name from path"""
        # /api/v1/users/123 -> users
        pass

    def is_collection(self, path: str) -> bool:
        """Check if request is for collection"""
        pass

    def get_operation_type(self, method: str, path: str) -> str:
        """GET collection, GET single, POST create, etc."""
        pass