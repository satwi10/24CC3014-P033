# 24CC3014-P033: AWS Lambda with Provisioned Concurrency for Latency SLA

## Project Overview
This project builds and benchmarks a serverless **payments authorisation endpoint** designed to meet a strict **100 ms p99 latency target** using **AWS Lambda Provisioned Concurrency**.

## Use Cases
* Meet a **100 ms p99 latency target**
* Serve a **payments authorisation endpoint** (`POST /authorize`)

## Key Bottlenecks Addressed
1. **Provisioned concurrency cost negates serverless savings:** Addressed via Scheduled Auto Scaling and AWS Lambda Power Tuning.
2. **Cold starts still occur beyond provisioned capacity:** Addressed via Target Tracking Auto Scaling at 70% utilization.

## Repository Structure
* `/docs` - Architecture diagrams and Phase 1 Proposal Document
* `/src` - AWS Lambda payment authorization source code (Phase 2)
* `/load-tests` - k6 load testing scripts for p99 latency verification (Phase 2 & 3)
