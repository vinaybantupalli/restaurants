
## Phase 1

#### Scope:
- Only Backend REST APIs
  - Customer API
    - View Items
    - Add/View Order
    - View Bill
  - Owner API
    - Add/Remove Items
    - Add/View/Edit/Remove Order
    - Add/Remove Table
    - View Bill
  - Admin API
    - Add/Edit/Remove Restaurants
- Session for a table will be maintained through JWT and table OTP
- All APIs need to be access managed 
  - admin can access all
  - restaurant owners can access their own restaurant
  - customer can only access their table


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