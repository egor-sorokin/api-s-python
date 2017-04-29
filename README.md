# api-s-python
## General description
This repo presents results of online course "Design RESTful APIs" on Udacity

link: https://www.udacity.com/course/designing-restful-apis--ud388

author: https://github.com/lobrown


Starter code also has been taken from Udacity course, except the final project, because there was no a starter code. The final project is called "Meet and Eat" (curently in progress). Requirements for that project you can find here https://github.com/udacity/APIs/blob/master/Final%20Project/FinalProject.pdf

## Types of rest api implementations
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

  `/clientOAuth/`: 
        
       Output: view with google oauth button, which return one time auth code 
                        
  `/oauth/<provider>/`: 
           
       - POST (create instance) 
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
**Description:** Searching restaurants based on a meal type and a location data through interactions with google maps and foursquare apis

*in progress...*

### 6) Bargain mart
**Description:** Limiting of requests to the rest api

*in progress...*
