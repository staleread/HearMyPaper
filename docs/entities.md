## Core Entities and Use Cases

1. **Core Entities**
   - **Student**: a user who encrypts and uploads course projects.
   - **Instructor**: a user who has a private key to decrypt and review/listen
     to submissions. Can also view the audit log for their group.
   - **Submission**: an encrypted file (e.g. pdf, txt, zip).
   - **Group / Course**: a unit connecting students and instructors.
   - **Access Token**: a cryptographic marker that ensures authorized access.

2. **Main Use Cases**
   - **Student** installs the client and uploads a submission, which is
     encrypted before sending.
   - **System** accepts and stores the submission in encrypted form.
   - **Instructor** gains access to the submission using their token.
   - The instructor can **read or convert the submission into audio** for
     listening.
   - Access is restricted only to instructors associated with the corresponding
     course/group.

3. **Implementation stages**
   - Implement token-based authentication system for client (Kotlin) and server
     (Python).
   - Implement uploading submissions to the server.
   - Enable submition encryption before uploading.
   - Implement user action audit.
   - Set up a file-to-audio conversion service as a separate microservice.

