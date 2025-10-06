# HearMyPaper

Secure your course project, and only let the instructor listen!

## Roadmap
- [ ] Audit (server)
  - [ ] Repository + Service @staleread
  - [ ] `@audit` decorator @K1ngston1
- [ ] Audit (client) @K1ngston1
  - [ ] "Audit" resource on home catalog
  - [ ] Audit catalog
- [ ] Project students assignment (client) @staleread
- [ ] Student's work submission @K1ngston1
  - [ ] "Submit" action on project overview screen
  - [ ] "Submissions" resource on home catalog
  - [ ] Submissions catalog
  - [ ] Submission overview screen
    - Submitted at
    - Status ("On time", "Late")
    - "Download" action
- [ ] PDF-to-audio submission @staleread
  - [ ] Add `session_id` to JWT payload
  - [ ] Mechanism for submitting encrypted PDF, so server can decrypt it
  - [ ] PDF-to-audio service
  - [ ] Action for submission overview page
