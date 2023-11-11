
## Phase 1

#### Scope:
- Only Backend REST APIs
  - Customer side
    - View Items
    - Add/View Order
    - View Bill
  - Owner side
    - Add/Remove Items
    - Add/View/Edit/Remove Order
    - Add/Remove Table
    - View Bill
- Session for a table will be maintained through JWT and table OTP


#### Out of Scope
- Frontend is out of scope for phase 1
- Payment of bill is out of scope
- Any analytics on order/item data

### Tech Stack
Python, Flask, MongoDB

#### Database Consideration:

- Data is not considered to be huge
- NoSQL offers some flexibility to us
- Mongo is cheap for low usage