# Restaurants

## Functional Requirements

### Customer
A service which allows customers to
- View menu after scanning barcode at the table
- Order items from the webpage (This should allow multiple
users to login and order simultaneously from the same table)
- View ordered items
- Generate bill total
- Pay bill

### Restaurant Owner
This would also support the following for restaurant owners
- Ability to add items and categorize them along with descriptions
- Ability to add/remove tables to the restaurant
- Ability to add/remove items from the menu **ad-hoc** as per item availability
- View the orders received/added from each table
- Manage the orders - add/remove items from each order
- Generate bill total

### Admin
This would allow admins to 
- Create/Delete the restaurant
- Activities listed above

## How to run

To run locally, use the following commands to build and run the docker image

```Shell
# Build docker image with tag 'restaurants' 
# The platform flag used is for apple silicon chips. Remove it or use appropriate for other machines
docker build --platform linux/arm64/v8 -f Dockerfile -t restaurants .
# Run the image with auto reloading code on the container and debug mode on 
docker run -dp 8080:80 -w /app -v "$(pwd):/app" restaurants
```