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


### For Prod
```https://www.getpostman.com/collections/1ade6fd3ca8b20688ed9```
(If you dont want to run this application, and directly call the apis, import this deployed apis)

# Points to Consider:
1. Python3 and pip3 should be installed if you are running on your local machine without using docker
2. There is a config file in projects/__init__.py which contains localhost_database_string and docker_database_string, so if you are not using docker, then its fine as by default I have set it to localhost_database_string, but if using docker make sure to replace line no. 17 with docker_database_string
