## Todo

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
---
### Next up
- Mongo make data models rich. Add cascading, etc
- Mongo tables indexing
- Documentation of access control flow 
- Verbose in code for swagger doc
- Implement closing table session (when bill is generated)
- How to handle adding items images (s3 and store image links?)
- Extra handling for identifying who in the table ordered what
  - Might be useful for splitting bill among themselves
- Handle env variables properly (for local and prod versions)
- Read about gunicorn and use it properly in docker
- How to handle early bird offers and discounts?