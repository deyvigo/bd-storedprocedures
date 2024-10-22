This is a project on Flask and MySQL using Stored Procedures.

## Install

1. You make sure you have installed MySQL.
2. Create a database with any name.
3. Create a .env file with the following content:

```
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```
* DB_NAME: The name of the database.

4. Create a virtual environment and install the requirements.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Then you can run the app.

```bash
python src/app.py
```
