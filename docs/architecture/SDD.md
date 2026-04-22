# SDD — Software Design Document

## Overall Architecture

**HearMyPaper** follows a microservices architecture with distinct client and server sides.

The defining characteristic is a security-first orientation:

- The client is implemented as a desktop application
- All cryptographic operations run on the client side
- Plaintext data never leaves the user's device
- The server minimizes handling of unencrypted data

## Components

### Desktop Application (Client)

A Python desktop app — a full-featured component, not a thin client.

Responsibilities:

- Cryptographic operations (encryption / decryption)
- File system access
- Authentication via hardware token
- HTTPS communication with the server
- Certificate pinning to protect against MITM attacks

### Leader Service (Core Backend)

The primary server component containing business logic.

Responsibilities:

- Handling client requests
- User and access management
- Document management
- Initiating processing tasks (conversion)
- Coordinating inter-service communication

Implemented in Python for compatibility with cryptographic libraries.

### PDF-to-Audio Converter Service

A dedicated microservice for converting PDFs to audio.

Characteristics:

- Isolated from external access (not reachable from the internet)
- Operates exclusively within the cluster
- Local processing tools (no third-party cloud TTS APIs)
- Independent horizontal scaling

Separated into its own component due to: high computational cost, need for independent scaling, and security requirements.

### Message Broker (RabbitMQ)

Handles asynchronous communication between services:

- Event passing between Leader Service and PDF-to-Audio Converter
- Event-driven architecture
- Load resilience

Large files are not transmitted through the broker.

### Object Storage (MinIO)

Stores:

- PDF files
- Conversion results (audio)
- Intermediate processing data

### Database (PostgreSQL)

Core data:

- Users
- Projects (courses)
- Document metadata
- Audit logs

### Key-Value Storage (Redis)

- Request caching
- Rate limiting

## Component Interactions

### Primary Flow — Submitting Work

1. Client encrypts the document with the instructor's public key
2. Client sends the encrypted file to Leader Service over HTTPS
3. Leader Service stores the file in Object Storage
4. Metadata is written to the database

### PDF-to-Audio Conversion Flow

1. Instructor decrypts the document locally
2. For conversion:
    - Server generates a temporary key
    - Client encrypts the PDF with that key
    - The key is encrypted with the instructor's public key
3. Data is transmitted to the server in protected form
4. Leader Service dispatches the task via RabbitMQ
5. PDF-to-Audio Converter retrieves the file from Object Storage, converts locally, stores the result
6. Intermediate data is deleted after processing completes

## Security in the Architecture

| Mechanism | Description |
| --------- | ----------- |
| End-to-end encryption | Data is never transmitted in plaintext |
| Certificate Pinning | Protection against MITM attacks |
| Service isolation | Critical components are unreachable from outside |
| Minimal data access | The server does not permanently store plaintext |
| Temporary storage | Plaintext exists only during active processing |

The architecture aligns with Zero Trust principles: no implicit network trust, every request verified, minimal resource access.
