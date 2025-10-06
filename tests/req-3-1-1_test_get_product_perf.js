// tests/req-3-1-1_test_get_product_perf.js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    rps1000: {
      executor: 'constant-arrival-rate',
      rate: 1000,              // 1000 requests per second
      timeUnit: '1s',
      duration: '10s',
      preAllocatedVUs: 1000,
      maxVUs: 2000,
    },
  },
  thresholds: {
    http_req_duration: ['p(99)<100'], // <— requirement
  },
};

const PRODUCT_ID = 'a1b2c3d4-e5f6-7890-1234-567890abcdef';
export default function () {
  const res = http.get(`http://localhost:8000/api/v1/products/${PRODUCT_ID}`);
  check(res, {'status is 200': (r) => r.status === 200});
}