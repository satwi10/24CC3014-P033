# Project Proposal: AWS Lambda with Provisioned Concurrency for Latency SLA

## 1. Problem Statement & Objective
![System Architecture](diagram.png)
In modern financial technology, payment authorization systems must be near-instantaneous to prevent checkout abandonment and meet banking standards. This project designs, benchmarks, and optimizes a serverless payment authorization endpoint that strictly satisfies a **100 ms p99 latency target**.

Standard serverless architectures (AWS Lambda) suffer from container initialization latency known as **cold starts** (often ranging from 300 ms to 1,000+ ms). This project implements **AWS Lambda Provisioned Concurrency** to maintain pre-warmed execution environments and evaluates strategies to resolve its associated cost and spillover bottlenecks.

## 2. API Contract & Data Model
* **Endpoint:** `POST /authorize`
* **Request Payload:**
```json
{
  "transaction_id": "txn_10928374",
  "merchant_id": "merch_99",
  "card_token": "tok_visa_4242",
  "amount": 49.99,
  "currency": "USD"
}
