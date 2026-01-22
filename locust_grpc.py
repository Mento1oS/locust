from locust import User, task, between
import grpc, random, string, time
from proto import glossary_pb2, glossary_pb2_grpc
from google.protobuf import empty_pb2

class GrpcGlossaryUser(User):
    wait_time = between(0.5, 2)

    def on_start(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = glossary_pb2_grpc.GlossaryStub(self.channel)

    @task(3)
    def list_terms(self):
        start = time.time()
        try:
            self.stub.ListTerms(empty_pb2.Empty())
            self.environment.events.request.fire(
                request_type="gRPC",
                name="ListTerms",
                response_time=int((time.time()-start)*1000),
                response_length=0,
                exception=None
            )
        except Exception as e:
            self.environment.events.request.fire(
                request_type="gRPC",
                name="ListTerms",
                response_time=0,
                response_length=0,
                exception=e
            )

    @task(1)
    def create_term(self):
        keyword = ''.join(random.choices(string.ascii_lowercase, k=8))
        req = glossary_pb2.CreateTermRequest(
            keyword=keyword,
            definition="Load test definition",
            source="locust"
        )
        start = time.time()
        try:
            self.stub.CreateTerm(req)
            self.environment.events.request.fire(
                request_type="gRPC",
                name="CreateTerm",
                response_time=int((time.time()-start)*1000),
                response_length=0,
                exception=None
            )
        except Exception as e:
            self.environment.events.request.fire(
                request_type="gRPC",
                name="CreateTerm",
                response_time=0,
                response_length=0,
                exception=e
            )
