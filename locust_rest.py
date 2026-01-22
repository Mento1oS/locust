from locust import HttpUser, task, between
import random, string

class GlossaryRestUser(HttpUser):
    wait_time = between(0.5, 2)
    host = "http://localhost:8000"  # адрес твоего REST сервера

    @task(3)
    def list_terms(self):
        self.client.get("/terms")

    @task(1)
    def create_term(self):
        keyword = ''.join(random.choices(string.ascii_lowercase, k=8))
        self.client.post("/terms", json={
            "keyword": keyword,
            "definition": "Load test definition",
            "source": "locust"
        })
