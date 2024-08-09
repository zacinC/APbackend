⚡ FastAPI for the Python backend API. <br/>
    🧰 SQLModel for the Python SQL database interactions (ORM).<br/>
    🔍 Pydantic, used by FastAPI, for data validation and settings management.<br/>
    💾 MySQL as the SQL database.<br/>
    
🔒 Secure password hashing by default.<br/>
🔑 JWT (JSON Web Token) authentication.<br/>
📫 Email-based password recovery.<br/>

Backend is live on [autobuskiprevozcg.xyz](https://autobuskiprevozcg.xyz/)

There is also interactive documentation available at [autobuskiprevozcg.xyz/docs](https://autobuskiprevozcg.xyz/docs)

![image](https://github.com/user-attachments/assets/a1fe7180-c9fd-46e6-a524-a9681afce752)

![image](https://github.com/user-attachments/assets/98404c67-f305-46f8-a194-1010906dcf8a)

![image](https://github.com/user-attachments/assets/6cdc7732-30b9-42ca-96f6-04fbe930b9cc)

# Running the project locally

If you want to run this project locally then you need to create two files:<br/>
1. settings.py
2. settings.json

Both are used for configuring our project's dependencies.

## settings.py
ALGORITHM = "HS256"<br/>
SECRET_KEY = "Generate a secret key to put here, you can do it with the command $ openssl rand -hex 32"<br/>
ACCESS_TOKEN_EXPIRE_MINUTES = 30<br/>
DATABASE = "name of the database"<br/>
CLOUDINARY_API_SECRET = "cloudinary api secret"<br/>
CLOUDINARY_API_KEY = "cloudinary api key"<br/>
EMAIL_RESET_TOKEN_EXPIRE_MINUTES = 10<br/>
BREVO_API_KEY = "Put your Brevo api key here"<br/>
ENV = 'PRODUCTION'<br/>
DOMAIN = 'Put the domain here'<br/>

## settings.json<br/>
This file is only used for configuring the database<br/>
{<br/>
  "username": "",<br/>
  "password": "",<br/>
  "host": "localhost",<br/>
  "port": 3306,<br/>
  "database": ""<br/>
}<br/>

## Running the project<br/>

1. Create venv folder - $ python3 -m venv venv
2. Install the dependencies - $ pip install -r requirements.txt
3. Run it with $ uvicorn main:app --reload

# Enjoy 😃
