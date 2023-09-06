ShareIt App is used to record shared expenses between users.

The main features are:
<ul>
  <li>Create expense types and allocate expenses to them.</li>
  <li>Provide aggregated data per month.</li>
  <li>Send monthly reports at the end of the month.</li>
  <li>DB and media backup.</li>
</ul>

<i>The project uses Black and Mypy.</i>

To set the project localy clone the repo and create .env file in the project folder and set the following variables:<br/>
```SECRET_KEY```<br/>
```DB_BACKUP_ACCESS_KEY``` - <i><a href="https://django-dbbackup.readthedocs.io/en/master/storage.html#amazon-s3" target="_blank">Docs</a></i><br/>
```DB_BACKUP_SECRET_KEY``` - <i><a href="https://django-dbbackup.readthedocs.io/en/master/storage.html#amazon-s3" target="_blank">Docs</a></i><br/>
```DB_BUCKET_NAME``` - <i>The bucket name in AWS S3</i>
```DB_USER``` - <i>The user that Django will use to access the DB</i><br/>
```DB_PASSWORD``` - <i>DB_USER's password</i><br/>
```DB_HOST``` - <i>Where the database is hosted</i><br/>
```DB_PORT``` - <i>On which port it is hosted</i><br/>
```EMAIL_HOST``` - <i>The email host used to send the automated emails (smtp.gmail.com for Gmail)</i><br/>
```EMAIL_HOST_USER```<br/>
```EMAIL_HOST_PASSWORD```<br/>
```ADMINS``` - <i>| separated list with emails to receive runtime error messages.</i><br/><br/>

Then run ```pip install -r requirements.txt``` in your virtual environment to install the project's requirements.<br/>
<i>Note that DEBUG=True should be used when testing.</i><br/>
Start a development server ```python manage.py runserver```.

AWS S3 is used for the automated DB and media backups. In order to use this feature you will need to create a bucket and set ```DB_BUCKET_NAME``` to its name.<br/>
You will also need a running Celery service, which will require a message brocker like RabbitMQ to run.<br/>
