import re
from typing import Optional


class RequestAnalyzer:
    def __init__(self):
        self.ignored_segments = {"api", "v1", "v2", "v3", "rest", "json"}

    def extract_resource(self, path: str) -> str:
        segments = [s for s in path.strip("/").split("/") if s]

        clean_segments = []
        for segment in segments:
            if segment.lower() in self.ignored_segments:
                continue
            if self._looks_like_id(segment):
                continue
            clean_segments.append(segment)

        return clean_segments[-1] if clean_segments else "root"

    def is_collection(self, path: str) -> bool:
        segments = [s for s in path.strip("/").split("/") if s]
        if not segments:
            return False

        last_segment = segments[-1]
        return not self._looks_like_id(last_segment)

    def get_operation_type(self, method: str, path: str) -> str:
        is_col = self.is_collection(path)
        method = method.upper()

        if method == "GET":
            return "LIST_ITEMS" if is_col else "GET_ITEM"
        elif method == "POST":
            return "CREATE_ITEM"
        elif method in ["PUT", "PATCH"]:
            return "UPDATE_ITEM"
        elif method == "DELETE":
            return "DELETE_ITEM"
        return "UNKNOWN"

    def _looks_like_id(self, segment: str) -> bool:
        if segment.isdigit():
            return True
        if re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}", segment):
            return True
        if re.match(r"^[a-z]+_\w+", segment) and any(c.isdigit() for c in segment):
            return True
        return False


request_analyzer = RequestAnalyzer()
