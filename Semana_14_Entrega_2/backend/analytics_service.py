import grpc
from concurrent import futures
import Semana_14_Entrega_2.backend.analytics_pb2 as analytics_pb2
import Semana_14_Entrega_2.backend.analytics_pb2_grpc as analytics_pb2_grpc

class AnalyticsServicer(analytics_pb2_grpc.AnalyticsServiceServicer):
    def LogSale(self, request, context):
        print(f"[gRPC ANALÍTICA] Venta registrada exitosamente -> Pedido #{request.order_id} por ${request.total}")
        return analytics_pb2.SaleResponse(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    analytics_pb2_grpc.add_AnalyticsServiceServicer_to_server(AnalyticsServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Servicio de Analítica gRPC corriendo en el puerto 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()