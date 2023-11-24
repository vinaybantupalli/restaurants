## Tasks

### Done
- ~~Add DB skeleton~~
    - ~~Add model for Restaurant Table~~
    - ~~Connect this with Restaurant API~~
    - ~~Dockerize DB and add instructions in Readme~~
- ~~Implement Users (model and schema and resources)~~
- ~~Get and Delete user access control~~
- ~~Restaurant API access control~~
- ~~Items Implementation~~
- ~~Club UserType in jwt claim and remove the db call to get user in each API call~~
- ~~Verify whether multiple people are able to log in simultaneously from same table~~
- ~~Make jwt session longer (default is 15 minutes)~~
- ~~- Orders Implementation~~
- ~~Populate schemas.py more elaborately~~
    - ~~Fix the schema jumble created for users API~~
- ~~Implement closing table session (when bill is locked)~~
- ~~Implement Bill API~~
### Next up
- Mongo make data models rich. Add cascading, etc
- Mongo tables indexing
- Documentation of access control flow 
- Verbose in code for swagger doc
- Use repeatable key from config for JWT secret key
- Add symmetric key encryption for table otp
- How to handle adding items images (s3 and store image links?)
- Extra handling for identifying who in the table ordered what
  - Might be useful for splitting bill among themselves
- Handle env variables properly (for local and prod versions)
- How to handle early bird offers and discounts?
- Explore migrating from marshmallow to pydantic
---
## Infra

- Read about gunicorn and use it properly in docker
- Add required k8s scripts 
- Figure out the setup to deploy (load balancer, reverse proxy, etc.)
- Add logging to all APIs
- Add unit tests for the APIs
- Figure out and implement telemetry
- Explore and implement github actions for build, push, deploy, etc.
- Explore how to profile the APIs
