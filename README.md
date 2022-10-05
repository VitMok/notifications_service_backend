# The following tasks were implemented in this project:
```
1. Adding a new client to the directory with all its attributes.
2. Update client attribute data.
3. Removing a client from the directory.
4. Adding a new mailing with all its attributes.
5. Obtaining general statistics on the created mailing lists and the number of sent messages on them, grouped by status.
6. Obtaining detailed statistics of sent messages for a specific mailing list.
7. Updating distribution attributes.
8. Removing the mailing list.
9. Processing active mailings and sending messages to clients.
10. Opening a page with Swagger UI and a description of the developed API at /docs/.
11. Sending statistics on processed mailing lists to email.
12. Handling external service errors and postponing requests if unsuccessful for later resubmission.
```

## Running Development Servers
```
$ docker compose up
```

## Setup
```
$ docker compose exec web python manage.py makemigrations
$ docker compose exec web python manage.py migrate
$ docker compose exec web python manage.py createsuperuser
```