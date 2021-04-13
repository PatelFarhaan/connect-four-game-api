# Assessment

## How to Run this application:

1. Create a virtual environment using the command: 
    ```virtualenv venv```
   
2. Actiavte the virtual environment using the command: 
    ```source venv/bin/activate```

3. Install all the requirements: 
    ```pip3 install -r requirements.txt```
   
4. Run the application:
    ```python3 app.py```
   
5. This also assumes you have mongo installed on your machine with the user, password and database names as admin and running on port 27017.


## How to Run this application using Docker:

If you have docker client installed on your machine, just clone this repo and type the command below:
```docker compose up -d --build```
   
## API LIST:

Once you have the application up and running, you can access all the apis by importing this collection in your postman:
### For Dev:

```https://www.getpostman.com/collections/2c95c34394fbffe8f2f3```


(If you dont want to run this application, and directly call the apis, import this deployed apis)
### For Prod
```https://www.getpostman.com/collections/2c95c34394fbffe8f2f3```
