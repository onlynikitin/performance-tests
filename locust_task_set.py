from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task(4)
    def get_home(self):
        return self.client.get("/home")

    @task(1)
    def get_dashboard(self):
        return self.client.get("/dashboard")
