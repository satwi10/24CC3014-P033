import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '15s', target: 10 }, // Stage 1: Ramp up within Provisioned Concurrency
    { duration: '30s', target: 10 }, // Stage 2: Steady state - verify <100ms p99 SLA
    { duration: '15s', target: 30 }, // Stage 3: Burst spike - test spillover & Auto Scaling
  ],
  thresholds: {
    // Project Requirement: Meet a 100 ms p99 latency target
    http_req_duration: ['p(99)<100'],
  },
};

const API_URL = __ENV.API_URL || 'https://your-api-id.execute-api.ap-south-1.amazonaws.com/default/PaymentAuthFunction';

export default function () {
  const payload = JSON.stringify({
    transaction_id: `txn_${__VU}_${__ITER}_${Date.now()}`,
    merchant_id: 'merch_benchmark_01',
    card_token: 'tok_visa_4242',
    amount: 49.99,
    currency: 'USD',
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(API_URL, payload, params);

  check(res, {
    'status is 200 (APPROVED)': (r) => r.status === 200,
    'p99 latency is under 100ms SLA': (r) => r.timings.duration < 100,
  });

  sleep(0.1);
}
