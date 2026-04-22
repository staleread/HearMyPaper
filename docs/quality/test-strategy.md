# Test Strategy

## Approach

**HearMyPaper** uses a multi-level testing approach covering both functional and non-functional verification. The primary focus is on access control model validation and cryptographic security.

## Testing Levels

### Unit Testing

Verification of individual components:

- Server services (Leader Service)
- Cryptographic modules
- Document processing logic
- Client-side components

### Access Control Testing

A critical test class for this security-focused system:

- Verification of the access control model (Bell–LaPadula)
- Instructors can only access documents assigned to them
- Access level isolation between roles (student / curator / instructor / administrator)

### Integration Testing

Verification of inter-component communication:

- Leader Service ↔ RabbitMQ
- Leader Service ↔ PDF-to-Audio Converter
- Client ↔ server over HTTPS
- Object Storage operations

### Load Testing

Tool: **Locust**. A CLI tool was built to simulate real clients using a test dataset (~30 instructors, ~70 students).

| Test type | Goal |
| --------- | ---- |
| Smoke | Basic functionality verification |
| Average Load | Typical operating conditions |
| Stress | Behavior under high load |
| Spike | Sudden traffic bursts (pre-deadline periods) |
| Breakpoint | Finding the failure threshold |
| Soak | Long-duration stability |

Test scenarios simulate: PDF submission, course browsing, student list checks, and PDF-to-audio conversion.

## Security Testing

- Cryptographic encryption verification
- Certificate pinning verification
- Token-based authentication verification
- Verification that data cannot be accessed outside the allowed access level
- Rate limiting (Redis) verification to prevent abuse
