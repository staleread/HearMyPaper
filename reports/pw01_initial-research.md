## Initial Research of the Domain

1. **Analysis of Existing Solutions**
   - Currently, platforms exist for uploading and reviewing student works
     (e.g., Moodle, Google Classroom).
   - However, most of them store files in a non-secure way or use minimal
     security measures.
   - None of the popular systems provide a convenient cryptographic protection
     mechanism where only instructors can unlock the work.
   - There is also no feature for automatic conversion of student submissions
     into audio for on-the-go accessibility.

2. **Potential Required Functionality**
   - **Client-side encryption of submissions**: students upload files in an
     encrypted form.
   - **Token-based authentication**: only instructors with a valid token can
     access the files.
   - **PDF / text-to-audio conversion**: instructors can listen to student
     submissions.
   - **Cross-platform clients**: Python server and Kotlin clients for desktop
     and mobile systems.
   - **Group-based access control**: students submit to their course, and only
     course instructors can access submissions.

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
