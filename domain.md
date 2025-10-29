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

