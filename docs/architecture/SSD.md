# SSD — System Specification Document

## Purpose

**HearMyPaper** is designed for secure interaction between students, instructors, and administrative staff during the exchange of academic materials.

The primary goal is to guarantee the confidentiality of student work through cryptographic mechanisms and a Bell–LaPadula access control model. The system ensures that only an authorized instructor can access submitted materials.

## Core Functions by Role

### Student

- View project (course) information, including syllabi and materials
- Create and upload completed work (PDF and other formats)
- Submit work to an instructor
- Automatic encryption of submissions using the instructor's public key

### Curator

- Create and manage projects (courses)
- Add students to projects
- Assign instructors to courses
- Edit and publish course materials (syllabi)

### Instructor

- View information about assigned courses
- Receive and decrypt student submissions using a private key
- Download work
- Initiate document processing (PDF-to-audio conversion)

### Administrator

- Create and manage user accounts
- Generate and issue authentication tokens
- Monitor user activity via the audit log
- Manage system access

## Constraints and Assumptions

- The system requires a hardware or external storage device (USB) for storing the authentication token.
- Access is only possible with both the token and the password to decrypt it.
- Users are identified by email address.
- A strict access control model is enforced: curators do not have access to instructor-level information.
- The system maintains an audit log of all key actions.

## Non-Functional Requirements

### Security

- Asymmetric encryption for data protection
- Data stored in encrypted form
- Access control based on confidentiality levels
- Secure authentication via cryptographic tokens
- Audit of all critical operations

### Performance

- Real-time request processing
- Asynchronous PDF-to-audio conversion
- Scalability support for large volumes of documents

### Reliability and Availability

- Stable operation under high load
- Data preservation during failures
- Recovery from errors

### Scalability

- Independent scaling of microservices
- Message queues for load balancing
- Support for containerization and orchestration (Kubernetes)
