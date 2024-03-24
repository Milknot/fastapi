# FastApi

Python version 3.10.4

## Initialize

Create virtual enviroment
```
python -m venv .
```

Start virtual enviroment
```
./Scripts/activate.bat
```

Install requirements by txt file
```
python -m pip install requirements.txt
```

Start Server
```
cd app
python -m uvicorn main:app --reload
```
> if you need test your api on local network add `--host 0.0.0.0` command

## Apply modifications

On case that you modify the project, on respect to add libraries, add these new libraries on requirements.txt to ensure correct work.

Update requirements.txt
```
python -m pip freeze > requirements.txt
```

## Configuration

In the `app` directory, you'll find the `env.json` file where you can configure your database settings. The settings include:

1. connector: Specifies the type of database (e.g., "mysql", "sqlite").
2. host: The address of your database.
3. user: Username for database login.
4. password: Corresponding password for the user.
5. schema: The default database to connect to.

> *Note:* In this version, only MySQL and SQLite database connectors are configured. You can add more connectors depending on your needs.