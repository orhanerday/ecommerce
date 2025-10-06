import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

const URL = 'http://localhost:8000/api/v1/orders/';
const HEADERS = { 'Content-Type': 'application/json' };

const PAYLOAD = JSON.stringify({
  customer_id: '43e8ff2f-5d48-498f-a569-ca2cf9f7fae3',
  product_id: 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
});

export let options = {
  vus: 100, // virtual users (you can tweak this)
  iterations: 100, // total number of requests
};

export default function () {
  const res = http.post(URL, PAYLOAD, { headers: HEADERS });

  const contentType = res.headers['Content-Type'] || '';
  let body = contentType.includes('application/json') ? res.json() : { raw: res.body };

  const ok = check(res, {
    'Status is 202': (r) => r.status === 202,
    'Body status is PENDING': () => body.status === 'PENDING',
  });

  // console.log(`[VU ${__VU}] Status: ${res.status} | Response: ${JSON.stringify(body)}`);

  sleep(0.1); // optional slight delay to simulate real-world pacing
}