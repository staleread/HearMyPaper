# HearMyPaper — Documentation

## System Overview

**HearMyPaper** is a software system for secure exchange of academic materials between students and instructors. Its primary goal is to protect the confidentiality of student work (lab assignments, course projects, etc.) using cryptographic mechanisms — specifically asymmetric encryption.

The system allows students to submit work as PDF documents that can only be accessed by authorized instructors. Functionality is organized around **projects** (courses), each involving students, curators, and instructors.

Additionally, the system supports converting PDF documents to audio format for convenient content consumption by instructors.

Technically, the system consists of:

- **Desktop application** (client-side)
- **Leader Service** — core backend (business logic, authorization, document management)
- **PDF-to-Audio Converter** — a dedicated microservice for document processing

Infrastructure: PostgreSQL, Object Storage (MinIO), RabbitMQ, Redis, Kubernetes.

## Target Audience

| Role | How they use the documentation |
| ---- | ------------------------------ |
| **Developers** | Architecture, API, microservice interactions |
| **QA Engineers** | Test scenarios, functional and non-functional requirements, security |
| **DevOps** | Deployment, Kubernetes, integration with PostgreSQL / RabbitMQ / Object Storage |
| **Business / Stakeholders** | System capabilities, purpose, and limitations |

## Documentation Structure

| Type | Document | Description |
| ---- | -------- | ----------- |
| **Product** | [SSD](architecture/SSD.md) | Functionality, system boundaries, non-functional requirements |
| **Product** | [SDD](architecture/SDD.md) | Architecture, components, and their interactions |
| **Product** | [ISD](architecture/ISD.md) | Infrastructure, deployment environment, CI/CD |
| **Quality** | [Test Strategy](quality/test-strategy.md) | Testing approach, levels, and scenarios |
| **Quality** | [Traceability Matrix](quality/traceability-matrix.md) | Mapping between requirements and tests |
| **Process** | [Onboarding](developer/onboarding.md) | Quick-start guide for developers |
