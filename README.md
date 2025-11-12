## E Commerce API 

The E Commerce API (Application Programming Interface) provides backend CRUD (Create, Read, Update, Delete) functionality for a generic internet based commercial sales application. It includes a relational database for storage of product, order, and user information through Microsoft's MySQL database and integration with Python and the Python Flask framework to enable manipulation of the data stored in the database. 

The API allows users to retrieve data from the database (Read), insert new data into the database (Create), change existing data stored in the database (Update), and permanantly remove data from the database (Delete). The API utilitzes HTTP (HyperText Transfer Protocol) and its GET (to retreive/Read data), PUT (to changeUupdate existing data), POST (to insert/Create new data), and DELETE (self explanatory) methods in order to provide its functionality.

Each of the APIs operations is carried out through its own "route." A route is simply a URL (Uniform Resource Locator) which accesses the functionality specified by the URL behind the scenes. In the case where an operation requires certain data in order to carry out its functionality, the required data will be provided in JSON (JavaScript Object Notation) format. For example, if a new product is to be inserted into the databse, then the user must provide the name and other details of the product to be added. Also, if a product is to be deleted, then the user must indicate which product to delete. 

Following is a list of all of the routes included in the API, the functionality associated with each of the routes, and the data to be sent to the route, if any, in order to carry out its function. Of course, not all routes require data. For example, retrieving a list of all products stored in the database does not require any data from the user at all. In the parlence of an API, the routes are called endpoints.

The E Commerce API consists of the following 15 endpoints grouped first by CRUD operation and then by commercial operation:

### GET Endpoints:

#### 1. '/users' 

> Retrieves all users, or customers currently stored in the database. This route requires no data
> in order to carry out its functionality.

#### 2. '/users/<id>'

> where <id> is the id number of a specific user/customer stored in the database. This route      requires no additional data in order to carry out its functionality.

#### 3. /products'

> Retrieves all products currently stored in the database. No additional data required.

#### 4. /product/<id>'

> where <id> is the id number of a specific product stored in the database, returns all the information about the product stored in the database. No additional data required.

#### 5. '/orders/user/<user id>'

> where <user id> is the id number of a specific user, returns all orders belonging to the user/customer currently stored in the database.

#### 6. '/orders/<order id>/products'

> where <order id> represents the id number of a specific order stored in the database, returns all of the information/details about the order currently stored in the database.

### POST Endpoints:

#### 7. '/new_user'

> Adds a new user to the database. Requires a JSON formatted object including all non-optional user/customer information to be stored in the database. 

#### 8. '/products'

> Adds a new product to the database. Requires a JSON formatted object including all non-optional product information to be stored in the database.

#### 9. '/orders/<user id>'

> where <user id> represents the id number of a user/customer currently stored in the database, adds the customer to the database. Requires a JSON formatted object including all non-optional user/customer information to be stored in the database.

### PUT Endpoints:

#### 10. '/users/<user id>'

> where <user id> represents the id number of a user/customer currently stored in the database, updates (replaces) any information stored in the database about the user which is sent to the endpoint with the request in the form of a JSON formatted (customer) object.

#### 11. '/products/<product id>'

> where <product id> represents the id number of a product currently stored in the databse, updates(replaces) any information stored in the database about the product which is sent to the endpoint with the request in the form of a JSON formatted (product) object.

#### 12. '/orders/<order id>/products/<product id>'

> where <order id> represents the id number of an order currently stored in the databse and <product id> represents the id number of a product currently stored in the database, adds the product to the order. No additional data is required for this endpoint.

#### 13. '/orders/<order id>/remove_product/<product id>'

> same as above except that the product with the id number <product id> is removed from the order specified by the <order id>. No additional data is required for this endpoint.

### DELETE Endpoints:

#### 14. '/product/<product id>'

> The product specified by the <product id> is removed (deleted) from the database. No additional data is required for this endpoint.

#### 15. '/users/<user id>'

> The user/customer specified by the <user id> is removed (deleted) from the database. No additional data is required for this endpoint.

### JSON Formats for Database Objects

> Following are the three object types which can be stored and or updated in the database and their corresponding JSON formats with data types for their properties. 

#### User/Customer

```
{
    id: integer type (system generated)
    name: string type (up to 30 character, required)
    address: string type (up to 255 characters)
    email: string type (up to 255 characters, required)
}

```
#### Order

```
{
    id: integer type (system generated)
    order date: (MM/DD/YYYY)
    user_id: integer type (required)
}

```

### Product

```
{
    id: integer type (system generated)
    product_name: (up to 255 characters, required)
    price: floating (decimal) type, required
}

```
