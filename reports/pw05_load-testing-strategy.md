# HMP load testing strategy

This document defines the technical plan for load testing HMP using k6 and DigitalOcean (DO) Insights. It focuses on:
- Average-load scenarios (used verbatim for load, soak, and stress tests)
- Spike scenarios around submission deadlines
- Critical endpoints and metrics
- Execution order per Grafana’s load testing guidance
- A pathway for iterative improvements after analyzing results

Links:
- Reference: Types of load testing (Grafana): https://grafana.com/load-testing/types-of-load-testing/

---

## 1) Scope, goals, and success criteria

Goals
- Establish baseline performance and resource consumption on our current minimal DO App Platform environment.
- Validate that the system supports our estimated average usage (10–15 concurrent users) and peak usage (up to 60 concurrent users, especially during the last 30 minutes before a deadline).
- Identify breakpoints, bottlenecks, and regression risks for future optimization (caching, rate limiting, infra scaling).

Primary success criteria (initial, provisional; refine after first run)
- Availability: overall error rate < 1% at average load; < 3% during spikes/stress (transient).
- Latency targets (p99; refine after the first test cycle):
  - Auth (challenge, login): ≤ 400 ms
  - Read-heavy list endpoints (GET /project/, GET /submission/): ≤ 700 ms
  - Read detail endpoints (GET /project/{id}, GET /submission/{id}/hash, content fetch): ≤ 800 ms depending on payload size
  - Pdf-to-audio trigger (POST /pdf-to-audio/execute): ≤ 2s to accept/queue work (not necessarily to complete conversion)
- System health headroom: sustained CPU < 70% and RAM < 80% under average load; brief spikes allowed under stress/spike.

Notes
- These thresholds anchor early decisions; they will be revised based on measured baselines and business priorities.

---

## 2) Test environment and baseline

Environment
- DO App Platform: minimal instance, low CPU, ~0.5 GB RAM
- DB and any backing services: whatever is currently used by the app (assess I/O and connection pool limits)
- Production-like configuration where possible; if not, document deviations here

Measured no-load baseline
- CPU: ~2.3%
- RAM: ~22%

Preconditions and test data (seed or fixture)
- Users:
  - 1–2 instructors
  - 50–100 students (emails, public keys, integrity/confidentiality attributes)
- Projects:
  - 20–30 projects (varied deadlines, instructors)
- Submissions:
  - 200–400 historical submissions to exercise list endpoints (adjust downward if memory-constrained)
- Documents for pdf-to-audio:
  - PDFs of 1–5 MB typical size for conversions

Assumptions and uncertainties
- No historical usage data; we model “average” user behavior deterministically for load/soak/stress.
- Spike scenario introduces a bursty pattern to reflect deadline behavior.
- Caching is not available at present, so no cache-related scenarios are tested.

---

## 3) Critical endpoints and business flows

Critical endpoints (by sensitivity and frequency)
- High frequency read:
  - GET /project/
  - GET /submission/
- CPU/data intensive:
  - POST /pdf-to-audio/execute
- Core flows:
  - Auth: POST /auth/challenge → POST /auth/login
  - Project browsing: GET /project/ → GET /project/{id}
  - Submission upload: POST /submission/ (application/cbor)
  - Submission detail: GET /submission/{id}/hash, GET /submission/{id}/content
  - Audit/logs (as needed): GET /audit/
  - Keys and misc: GET /credentials/public-key, GET /submission/instructor_key

User journeys (used by scenarios)
- Student (S):
  - Login handshake → fetch all projects → read 1–2 project details → optional: upload one submission
- Instructor (I):
  - Login handshake → fetch project list → open 1–2 project details → fetch submission list → open 1–3 submission details → optional: convert a submission to audio

Role distribution
- Average scenario: ~80% Students, ~20% Instructors
- Spike scenario (deadline): ~95% Students (many uploads), ~5% Instructors (some conversions)

---

## 4) Tools, metrics, and observability

Tools
- Generator: Locust (Python-based load testing with Ed25519 and CBOR support)
- Monitoring: DO Insights (CPU, memory, disk/network I/O), plus app logs

Metrics to capture
- Per endpoint: latency p50/p90/p99, throughput (req/s), error rate, timeouts
- System: CPU, memory, network I/O, disk I/O (from DO Insights)
- App logs: response codes, slow requests, internal errors, queue delays (if any)

Locust outputs and thresholds
- Export Locust summary JSON and HTML reports per run
- Define endpoint-specific thresholds aligned with provisional SLOs
- Record and store artifacts per run (results JSON/HTML, DO Insight screenshots)

---

## 5) Scenarios

The “Average Scenario” is reused for Load, Stress, and Soak tests. Spike has a dedicated pattern.

5.1 Average Scenario (for Load, Stress, Soak)
- Users: 10-15 concurrent users
- User mix: 80% S, 20% I
- Student action weights per session:
  - Login handshake: 1x
  - GET /project/: 1x
  - GET /project/{id}: 1–2x
  - POST /submission/: 0.2x (20% of student sessions perform one upload)
- Instructor action weights per session:
  - Login handshake: 1x
  - GET /project/: 1x
  - GET /project/{id}: 1–2x
  - GET /submission/: 1x
  - GET /submission/{id}/content or hash: 1–3x
  - POST /pdf-to-audio/execute: 0.2x (20% of instructor sessions trigger one conversion)

5.2 Spike Scenario (deadline window)
- Users: 60 concurrent users
- User mix: 95% S, 5% I
- Student action weights per session:
  - Login handshake: 1x
  - GET /project/: 1x
  - POST /submission/: 1x (most sessions upload)
- Instructor action weights per session:
  - Login handshake: 1x
  - GET /project/: 1x
  - GET /submission/: 1x
  - GET /submission/{id}/content: 1–2x
  - POST /pdf-to-audio/execute: 0.5x (some conversions occur during spike)
- Burst shape:
  - Sudden ramp to 60 active VUs within 1 minute
  - Hold 3 minutes to emulate deadline crunch
  - Optional micro-bursts: ±10% VUs jitter every 30–60s

---

## 6) Test types and execution algorithm

We follow the recommended test sequence from Grafana's load testing guidance. Each test type has specific parameters and serves a distinct purpose in validating system behavior.

### Test Definitions

**1. Smoke Test**
- Purpose: Verify all endpoints work correctly under minimal load
- Users: 5 users
- Duration: 2 minutes
- Pattern: Immediate ramp to 5 users, hold for 2 min, ramp down
- Success criteria: 0 errors, all endpoints respond

**2. Load Test (Average)**
- Purpose: Establish baseline performance and resource usage under typical load
- Users: 10 users → 15 users
- Duration: 25 minutes
- Pattern: 2m ramp to 10 users → 9m hold → 2m ramp to 15 users → 10m hold → 2m ramp down
- User distribution: 80% students, 20% instructors
- Success criteria: Error rate < 1%, p99 latencies within SLOs, CPU < 70%, RAM < 80%

**3. Stress Test**
- Purpose: Test system behavior under prolonged higher-than-average load
- Users: 30 users
- Duration: 35 minutes
- Pattern: 4m ramp to 30 users → 29m hold → 2m ramp down
- User distribution: 80% students, 20% instructors
- Success criteria: Error rate < 2%, graceful degradation, no crashes
- Note: This resembles average load but with higher sustained load and proportionally longer ramp-up

**4. Spike Test**
- Purpose: Validate burst resilience and recovery during deadline submissions
- Users: 60 users
- Duration: 5 minutes
- Pattern: 1m ramp to 60 users → 3m hold → 1m ramp down
- User distribution: 95% students (heavy submission activity), 5% instructors
- Success criteria: Error rate < 3%, system recovers gracefully, no data loss

**5. Breakpoint Test**
- Purpose: Find the breaking point by gradually increasing load until failure
- Users: 10 → 20 → 40 → 60 → 80 → 100 → 120 → 140 → 160 → 180 → 200 users
- Duration: 57 minutes
- Pattern: 2m ramp per step, 3m hold at each level until failure or completion
- User distribution: 80% students, 20% instructors
- Success criteria: Identify maximum sustainable load and failure modes

**6. Soak Test**
- Purpose: Detect memory leaks and resource drift over extended periods
- Users: 8 users
- Duration: 180 minutes (3 hours)
- Pattern: 2m ramp to 8 users → 176m hold → 2m ramp down
- User distribution: 80% students, 20% instructors
- Success criteria: No memory leaks, stable performance, error rate < 1%

### Execution Algorithm

```
EXECUTE test_sequence:
  INPUT: environment (server_url, admin_credentials)
  
  STEP 1: Setup
    CALL test-env.py up WITH credentials, host
    VERIFY test_data.json created
  
  STEP 2: Smoke Test
    RUN smoke-test.py
    IF errors > 0 THEN
      ABORT "Functional issues detected"
    END IF
  
  STEP 3: Load Test (Average)
    RUN average-test.py
    IF error_rate > 1% OR p99_latencies exceed SLOs THEN
      FLAG "Baseline performance insufficient"
      RECOMMEND optimizations (caching, indexes, pagination)
    END IF
    RECORD baseline metrics
  
  STEP 4: Stress Test
    RUN stress-test.py
    IF system crashes OR error_rate > 5% THEN
      FLAG "System unstable under higher sustained load"
      RECOMMEND infrastructure scaling or rate limiting
    END IF
    RECORD stress behavior
  
  STEP 5: Spike Test
    RUN spike-test.py
    IF error_rate > 3% OR recovery_time > 5m THEN
      FLAG "Poor burst handling"
      RECOMMEND async queues, circuit breakers, autoscaling
    END IF
    RECORD spike behavior
  
  STEP 6: Breakpoint Test (conditional)
    RUN breakpoint-test.py
    RECORD max_users_before_failure
    RECORD failure_mode (CPU, memory, timeouts, etc.)
    ANALYZE bottleneck
  
  STEP 7: Soak Test (conditional)
    IF all previous tests passed THEN
      RUN soak-test.py
      IF memory_growth > 10% OR performance_degradation > 15% THEN
        FLAG "Long-term stability issues"
        RECOMMEND memory profiling and leak detection
      END IF
    ELSE
      SKIP "Prerequisites not met"
    END IF
  
  STEP 8: Teardown
    CALL test-env.py down WITH credentials, host
    VERIFY test data removed
  
  STEP 9: Report Generation
    AGGREGATE metrics from all tests
    EXPORT Locust JSON/HTML reports
    CAPTURE DO Insights screenshots
    GENERATE summary with recommendations
  
  RETURN test_results
```

### On order of execution

The execution order is designed to progressively stress the system while gathering actionable insights:

1. **Smoke** catches functional bugs before resource-intensive tests
2. **Load** establishes performance baselines needed to evaluate other tests
3. **Stress** validates behavior under sustained higher load (distinguishes from breakpoint testing)
4. **Spike** tests burst resilience using real-world deadline scenario
5. **Breakpoint** identifies absolute limits and failure modes
6. **Soak** confirms long-term stability (only after passing foundational tests)

Each test builds on knowledge from previous tests, allowing early termination if critical issues are found.

---

## 7) Immediate actions if results are “not good enough”

### Possible Ways for Improvements (with indicative cost)

- **Low-cost (code changes):**
  - Introduce/optimize caching for read-heavy list endpoints (GET /project/, GET /submission/)
  - Add rate limiting and circuit breakers on heavy endpoints (especially POST /pdf-to-audio/execute and POST /submission/)
  - Make pdf-to-audio asynchronous with a job queue and idempotent triggers; return 202 Accept with job id
  - Apply pagination consistently and lower default page sizes
  - Optimize DB access: indexes, N+1 elimination, connection pooling
  - Stream uploads/downloads; limit payload sizes; compress responses where appropriate
  - Add server-side request timeouts and backpressure to protect the app under overload

- **High-cost (infrastructure):**
  - Scale vCPU/RAM; enable autoscaling where cost-effective
  - Introduce Redis for cache/session/queues
  - Separate workers for CPU-bound audio conversion (dedicated service/container)
  - Consider object storage for submissions and audio artifacts
  - Tune Postgres (work_mem, shared_buffers), or managed DB sizing
  - Add CDN or edge cache for static or frequently accessed assets/content

Process
- Automate test runs as part of release hardening
- Track performance budgets and regressions over time

---

This strategy will evolve after the first cycle of runs. We will tighten or relax thresholds, refine user behavior models, and prioritize improvements based on the highest impact per unit effort observed in the results.
