# api-s-python
## General description
This repo presents results of online course ["Design RESTful APIs"] on Udacity.

Author of the course: https://github.com/lobrown


Starter code also has been taken from Udacity course, except the final project, because there was no a starter code. The final project is called "Meet and Eat" (currently in progress). Its requirements can be found [here].

## Projects and types of api implementations
**Note:** All projects can be run simple by command `python views.py`, except projects with numbers 5 and 6. For them you can find details in a specific project.

### 1) Puppies
**Description:** Simple rest api without any authentification

**Methods:**

  `/puppies/`: 

      - GET (return list of puppies)
      - POST (create puppy) 
            Params: 
                - name (string)
                - description (string)
                        
  `/puppies/<id>/`:
  
      - GET (return puppy by id)
      - PUT (modify puppy)
            Params: 
                - name (string)
                - description (string)
      - DELETE (remove puppy)

### 2) Bagel shop
**Description:** Authentification through a password and a username

**Methods:**
  
  `/users/`: 
          
      - POST (create user)
                Params: 
                    - username (string)
                    - password (string)
                        
  `/bagels/`: 
          
      Auth: {usenrmae: <username>, password: <password>}
      - GET (return list of products)
      - POST (create product)
                Params: 
                    - name (string)
                    - description (string)
                    - picture (string)
                    - price (string)

### 3) Regal tree foods
**Description:** Authentification through token 

**Methods:** 
  
  `/users/`: 
          
      - POST (create user)
                Params: 
                    - username (string)
                    - password (string)
                        
  `/products/`: 
           
       Auth: {usenrmae: <username>, password: <password>}
       - GET (return list of users)
       - POST (create user) 
                Params: 
                    - name (string)
                    - category (string)
                    - price (string)
                        
  `/products/<category>`: 
          
       Auth: {usenrmae: <username>, password: <password>}
       Category: 'fruit', 'legume', 'vegetable'
       Output: return a list of instance filtered by category
                        
  `/token/`: 
          
        Auth: {usenrmae: <username>, password: <password>}
        Output: return a token for current user


### 4) Pale kale
**Description:** Google Oauth2 

**Methods:** 

  `/clientOAuth/`: 
        
       Output: view with google oauth button, which return one time auth code 
                        
  `/oauth/<provider>/`: 
           
       - POST (exchange a one time auth code and a token) 
                Params: 
                    - auth_code (string) // here should be one time auth code 
                    
   `/users/`: 
          
        - POST (create user)
              Params: 
                  - username (string)
                  - password (string)
                  
   `/api/resource/`:
        
        - GET (return "hello, <username>")   

### 5) Restaurants
**Description:** Searching restaurants based on a meal type and a location data through interactions with google maps and foursquare apis.

**Note:** Please check out [Foursquare API] and [Google Maps API] and [Google Maps Geocoding API] for details.

**Methods:**

  `/restaurants/`: 

      - GET (return list of restaurants)
      - POST (add a restaurant to db) 
            Params: 
                - location (string)
                - mealType (string)
                        
  `/restaurants/<id>/`:
  
      - GET (return restaurant by id)
      - PUT (modify restaurant)
            Params: 
                - address (string)
                - name (string)
                - image (string)
      - DELETE (remove restaurant)

### 6) Bargain mart
**Description:** Limiting of requests to the rest api

**Note:** Instruction for the running [redis server]. Also to test the project you need to run first of all *views.py* then *hungyclient.py*.

**Methods:** 

  `/catalog/`:
        
      - GET (return catalog of items)
            Limit of requests: 30 requests per 60 seconds

### 7) Meet and Eat
*in progress*

[Google Maps Geocoding API]: https://developers.google.com/maps/documentation/geocoding/intro
[Google Maps API]: https://developers.google.com/maps/?hl=en
[Foursquare API]: https://developer.foursquare.com/docs/venues/venues
["Design RESTful APIs"]: https://www.udacity.com/course/designing-restful-apis--ud388
[here]: https://github.com/udacity/APIs/blob/master/Final%20Project/FinalProject.pdf
[redis server]: https://redis.io/topics/quickstart
