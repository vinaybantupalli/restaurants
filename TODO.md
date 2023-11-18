## Todo

### Done
- ~~Add DB skeleton~~
    - ~~Add model for Restaurant Table~~
    - ~~Connect this with Restaurant API~~
    - ~~Dockerize DB and add instructions in Readme~~
- ~~Implement Users (model and schema and resources)~~
- ~~Get and Delete user access control~~
- ~~Restaurant API access control~~

---
### Next up
- Items Implementation
- Orders Implementation
- Populate schemas.py more elaborately
    - Fix the schema jumble created for users API
- Mongo make data models rich. Add cascading, etc
- Mongo indexing
- Documentation of access control flow 
- Verbose in code for swagger doc - some of the responses aren’t coming up
- Verify whether multiple people are able to log in simultaneously from same table
- Implement closing table session (when bill is generated)
- Make jwt session longer (default is 15 mins)
- How to handle adding items images (s3 and store image links?)
- How to handle early bird offers and discounts? 
- Extra handling for identifying who in the table ordered what
  - Might be useful for splitting bill among themselves
- Handle env variables properly (for local and prod versions)
- Read about gunicorn and use it properly in docker
- Club UserType in jwt claim and remove the db call to get user in each API call
