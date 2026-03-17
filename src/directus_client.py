# src/directus_client.py
from directus import Directus
from pydantic import BaseModel
from typing import Optional, Dict, Any

class DirectusClient:
    """A client for interacting with Directus."""

    def __init__(self, url: str, email: str, password: str):
        self.client = Directus(url)
        self.client.auth.login(email=email, password=password)

    def log_data(self, collection: str, data: Dict[str, Any]) -> Optional[Dict]:
        """Log data to a Directus collection."""
        return self.client.items(collection).create(data)

    def query_data(self, collection: str, query: Dict = None) -> list:
        """Query data from a Directus collection."""
        return self.client.items(collection).read(query or {})

    def close(self):
        """Close the Directus client."""
        self.client.auth.logout()

# Example usage:
# client = DirectusClient("http://localhost:8055", "admin@example.com", "admin")
# client.log_data("flight_logs", {"altitude": 1000, "airspeed": 150})
# data = client.query_data("flight_logs", {"filter": {"altitude": {"_gt": 500}}})
# client.close()
