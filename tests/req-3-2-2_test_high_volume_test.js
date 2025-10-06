import http from 'k6/http';
import { check } from 'k6';

// CONFIGURE: Update with real product_id and customer_id
const BASE_URL = 'http://localhost:8000';
const PRODUCT_ID = 'a1b2c3d4-e5f6-7890-1234-567890abcdef';
const CUSTOMER_ID = '43e8ff2f-5d48-498f-a569-ca2cf9f7fae3';

export const options = {
  scenarios: {
    create_order_load_test: {
      executor: 'constant-arrival-rate',
      rate: 10000, // 1000 requests per second
      timeUnit: '1s',
      duration: '10s',
      preAllocatedVUs: 1000,
      maxVUs: 2000,
    },
  },
  thresholds: {
    http_req_failed: ['rate==0'], // No failed requests
    http_req_duration: ['p(99)<1000'], // Optional: 99% under 1000ms
  },
};

export default function () {
  const url = `${BASE_URL}/api/v1/orders`;

  const payload = JSON.stringify({
    product_id: PRODUCT_ID,
    customer_id: CUSTOMER_ID,
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(url, payload, params);

  check(res, {
    'status is 202': (r) => r.status === 202,
    'order_id returned': (r) => r.json('order_id') !== undefined,
    'status is PENDING': (r) => r.json('status') === 'PENDING',
  });
}
