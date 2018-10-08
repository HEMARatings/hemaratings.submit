# hemaratings.submit
HEMA Ratings Submit app


## Installation
### Docker
todo

### local dev instance 
1. Install ODBC Driver 
This is script for Ubuntu 18.04. For other systems check https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017. 
```
sudo su  
sudo apt-get update  
sudo ACCEPT_EULA=Y apt-get install msodbcsql17  
sudo ACCEPT_EULA=Y apt-get install mssql-tools    
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.zshrc    
sudo apt-get install unixodbc-dev
```

2. Copy `.env.temp` to `.env` and fill it with real settings and load it with  
```
set -o allexport; source .env; set +o allexport
```

3. Fetch code
```
git clone git@github.com:adam-tokarski/hemaratings.submit.git
```


4. Install vitualenv with all dependenciens
```
pipenv install --dev
pipenv shell
```

5. Django stuff
```
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
