# 🔗URL Shortner
This is a simple URL shortner built with Flask for the backend and Bulma for the front end

## 🛠 Setting up
1. Create a .env file and make sure you add the following keys:
    - `HCAPTCHA_SITE_KEY`: Your hCaptcha Site Key
    - `HCAPTCHA_SECRET_KEY`: Your hCaptcha secret key
    - `secret_key:` The secret key to set for your Flask application
    - `MONGODB_CONNECTION_STRING:` A MongoDB connection string that can be used to read/write/modify data in a MongoDB database

2. Download all the required Python packages. You can do this easily with the requirements.txt file that comes with the repository.

3. Download the required NPM modules. Go to the `static` folder and there will be a package.json and a package-lock.json files. 

    The static folder should look something like this
    ```
    static
    ├───css
    ├───js
    └───node_modules
    ```

4. Setup a MongoDB Client

## 🚀 Running the Flask Application
Just run the `app.py` file and the program will do the rest!