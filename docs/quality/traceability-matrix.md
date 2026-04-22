# Traceability Matrix

Maps system requirements to their corresponding tests.

## Matrix

| ID | Requirement | Description | Test |
| -- | ----------- | ----------- | ---- |
| FR-01 | Work submission | Student can upload a PDF submission | TC-01 Unit / Integration |
| FR-02 | Work review | Instructor can view assigned submissions | TC-02 Access Control Test |
| FR-03 | Encryption | System encrypts documents before transmission | TC-03 Security Test |
| FR-04 | Project creation | User can create a project (course) | TC-04 Functional Test |
| FR-05 | Student management | Curator can add students to a course | TC-05 Functional Test |
| FR-06 | Conversion | Instructor can initiate PDF-to-audio conversion | TC-06 Integration Test |
| NFR-01 | Spike load | System handles sudden traffic surges | TC-07 Load (Spike Test) |
| NFR-02 | Response time | Average response time ≤ 300 ms | TC-08 Load Test |
| NFR-03 | Availability | System availability ≥ 99.9% | TC-09 Reliability Test |
| SEC-01 | Access control | Cross-level data access is forbidden | TC-10 Access Control |
| SEC-02 | Transmission security | Data is only transmitted in encrypted form | TC-11 Security Test |

## Summary

System quality is ensured through a combination of functional testing, load testing, and security verification. The key focus is validation of the Bell–LaPadula access model and cryptographic security.
