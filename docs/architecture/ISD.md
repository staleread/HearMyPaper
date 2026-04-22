# ISD — Infrastructure Specification Document

## Deployment Environment

The system is deployed using Docker (containerization) and Kubernetes (orchestration).

The target cloud environment is **DigitalOcean** (managed Kubernetes cluster). Local testing uses Minikube or equivalent solutions.

Environment separation:

| Environment | Purpose |
| ----------- | ------- |
| **staging** | Testing and validating changes |
| **production** | Stable operation |

## Infrastructure Components

### Kubernetes Cluster

System components are deployed as Kubernetes Deployment resources:

| Component | Deployment type |
| --------- | --------------- |
| Leader Service | Deployment |
| PDF-to-Audio Converter | Deployment |
| PostgreSQL | Helm chart |
| RabbitMQ | Helm chart |
| MinIO (Object Storage) | Deployment |

A declarative approach is used throughout (YAML / Helm).

### Containerization

Each component is packaged as a Docker image and published to **Docker Hub**. This ensures environment reproducibility, simplifies delivery, and standardizes service startup.

### Object Storage (MinIO)

S3-compatible storage for:

- PDF files
- Audio files
- Intermediate processing results

## CI/CD

### Continuous Integration

CI is implemented via **GitHub Actions**. Every push triggers:

- Unit tests
- Linter (ruff)
- Type checking (mypy)
- Automated security audit (Bandit)

Bandit runs on every push to `main` and daily on a cron schedule. Results are stored as security issues visible only to collaborators.

### Continuous Delivery — Backend

1. GitHub Actions builds Docker images
2. Images are published to Docker Hub
3. A DigitalOcean CLI command triggers deployment
4. The system pulls the new image and updates running services

| Branch | Environment |
| ------ | ----------- |
| `main` | staging |
| `release` | production |

### Continuous Delivery — Client

Tag-based release approach:

- Creating a Git tag triggers a release
- Packages are automatically built for:
    - Windows (`.msi`)
    - Linux Ubuntu/Debian (`.deb`)
    - Arch Linux

## Scaling

| Component | Strategy |
| --------- | -------- |
| PDF-to-Audio Converter | Horizontal scaling based on processing load |
| Leader Service | Single-instance or multi-instance |
| RabbitMQ | Load balancing across workers via queues |

## Infrastructure Security

- Service isolation within the Kubernetes cluster
- PDF-to-Audio Converter is not accessible from outside the cluster
- Sensitive data stored in GitHub Secrets and Kubernetes Secrets
- JWT sessions stored only in client memory
- User action audit logging

### Authentication Flow

1. Server generates a challenge payload
2. Client signs it with the token's private key
3. Server verifies the signature using the public key
4. On success, a session token is issued
