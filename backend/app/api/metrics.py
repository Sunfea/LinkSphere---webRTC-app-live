from fastapi import APIRouter
try:
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram, Gauge
    PROMETHEUS_AVAILABLE = True
except ImportError:
    # Mock the imports if prometheus_client is not available
    class MockMetric:
        def __init__(self, *args, **kwargs):
            pass
        
        def labels(self, *args, **kwargs):
            return self
            
        def inc(self, *args, **kwargs):
            pass
            
        def observe(self, *args, **kwargs):
            pass
    
    generate_latest = lambda: b""
    CONTENT_TYPE_LATEST = "text/plain"
    Counter = MockMetric
    Histogram = MockMetric
    Gauge = MockMetric
    PROMETHEUS_AVAILABLE = False

import time

router = APIRouter()

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])
ACTIVE_CONNECTIONS = Gauge('active_websocket_connections', 'Number of active WebSocket connections')
ACTIVE_ROOMS = Gauge('active_rooms', 'Number of active rooms')
ONLINE_USERS = Gauge('online_users', 'Number of online users')

@router.get("/metrics")
async def metrics_endpoint():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Middleware to track request metrics
async def track_request_metrics(request, call_next):
    method = request.method
    endpoint = request.url.path
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=response.status_code).inc()
    REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
    
    return response