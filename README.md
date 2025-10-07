# System Architecture Overview

The following diagram illustrates the high-level architecture of the e-commerce order processing system. It highlights the asynchronous flow between the API, message queue, background workers, and database.

## Order Request Lifecycle

![api_lifecycle](lifecycle.png)

**Flow Summary:**
1. FastAPI receives the order request.
2. The request is placed in a durable message queue (Redis/RabbitMQ).
3. A Celery worker consumes tasks from the queue asynchronously.
4. The worker updates MySQL atomically (stock, wallet, and order status).
5. This ensures resilience, concurrency safety, and no data loss on restart.


## Resource Utilization During High-Load Test

To evaluate system efficiency under the 10,000-order load test (REQ-3.2.2), resource usage was monitored using docker stats.

The following table shows the system while idle:

| Service      | CPU    | Memory Usage          | Memory % | Network I/O (Rx / Tx) | Block I/O        | PIDs |
|--------------|--------|-----------------------|---------:|-----------------------|------------------|-----:|
| FastAPI App  | 2.28%  | 907.7 MiB / 7.65 GiB  | 11.6%    | 520 kB / 559 kB       | 0 B / 16.4 kB    | 23   |
| Redis Broker | 0.93%  | 10.3 MiB / 7.65 GiB   | 0.13%    | 525 kB / 491 kB       | 0 B / 0 B        | 6    |
| MySQL DB     | 0.80%  | 386.7 MiB / 7.65 GiB  | 4.9%     | 34 kB / 60.4 kB       | 115 kB / 15.7 MB | 43   |

The following table shows average container utilization while processing ~1000 RPS (high-load):

| Container          | CPU %    | Mem Usage / Limit     | Mem %  | Net I/O (Rx / Tx)  | Block I/O        | PIDs |
|--------------------|----------|------------------------|-------:|--------------------|------------------|-----:|
| ecommerce-app      | 853.95%  | 1.261 GiB / 7.654 GiB  | 16.48% | 5.12 MB / 6.11 MB  | 0 B / 20.5 kB    | 472  |
| ecommerce-redis    | 33.37%   | 17.19 MiB / 7.654 GiB  | 0.22%  | 4.07 MB / 1.74 MB  | 0 B / 12.3 kB    | 6    |
| ecommerce-mysql    | 138.32%  | 421.4 MiB / 7.654 GiB  | 5.38%  | 166 kB / 226 kB    | 115 kB / 16.9 MB | 50   |

Key deltas (Idle → High-Load):

| Service   | CPU Idle | CPU Load | Δ CPU     | Mem Idle    | Mem Load     | Δ Mem (Approx) |
|-----------|----------|----------|-----------|-------------|--------------|----------------|
| FastAPI   | 2.28%    | 853.95%  | +851.67%  | 907.7 MiB   | 1.261 GiB    | +~384 MiB      |
| Redis     | 0.93%    | 33.37%   | +32.44%   | 10.3 MiB    | 17.19 MiB    | +~6.9 MiB      |
| MySQL     | 0.80%    | 138.32%  | +137.52%  | 386.7 MiB   | 421.4 MiB    | +~34.7 MiB     |



## Q&A:

**Q: During the high-volume test (REQ-3.2.2), how is total resource usage of all system components excluding the API, workers, and database measured and monitored?**  
A: By aggregating docker stats for the remaining infrastructure containers (e.g., Redis broker; others if present).
```
docker stats --no-stream --format '{{.Name}},{{.CPUPerc}},{{.MemUsage}}' \
  | grep -v -E '(ecommerce-app|mysql|worker)'
```
If additional services exist (e.g., reverse proxy, cache, messaging, monitoring), sum their CPU % and memory. For continuous tracking, cAdvisor + Prometheus can scrape and aggregate these container metrics automatically.
