# Django LiveChat

Chat Service for [Low Latency Live Streaming](https://github.com/sriharshamvs/low-latency-live-streaming)

## Local Development

#### Prerequisites

- `Python3.6` or `Python 3.7`
- [Redis](https://redis.io/topics/quickstart)
- [PostgreSQL](https://www.postgresql.org/download/linux/debian/)

#### Redis

- Install Redis Server

```bash
sudo apt install redis-server
```

#### Database setup

- Creating a New Role

```bash
sudo -u postgres createuser --interactive
```

```bash
#output
Enter name of role to add: comments
Shall the new role be a superuser? (y/n) y
```

Creating a Comments Database

- Open `psql` promt

```bash
sudo su - postgres
psql
```

- Enter Commands one by one

```bash
CREATE DATABASE comments;
CREATE USER comments WITH PASSWORD 'comments';
ALTER ROLE comments SET client_encoding TO 'utf8';
ALTER ROLE comments SET default_transaction_isolation TO 'read committed';
ALTER ROLE comments SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE comments TO comments;
```

- Exit the SQL prompt and postgres user’s shell session

```bash
\q

exit
```

#### Django Setup

- Clone the project and go the project root directory

```bash
git clone git@github.com:sriharshamvs/live-stream-comments.git
cd live-stream-comments
```

- Create a virtual environment and activate

```bash
python3 -m venv venv

source venv/bin/activate
```

**Note:** To deactivate virtual environment, type `deactivate`

- Install required Python Packages

```bash
pip3 install -r requirements.txt
```

- Create __.env__ file by creating a copy of __env.example__

```bash
cp env.example .env
```

- Migrate the Database

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

- Create an Administrative User

```bash
python3 manage.py createsuperuser
```

- Comment & Uncomment code blocks in the following files:

  - `templates/comments/room.html`
  - `templates/comments/room_mod.html`
  - `static/comments.js`
  - `static/comments_2.js`
  - `static/comments_login.js`

- Run the Server

```bash
python3 manage.py runserver
```

- Run Daphne on port 8001

```bash
daphne -b 127.0.0.1 -p 8001 live-stream-comments.asgi:application
```

## Contributing

Please read [CONTRIBUTING](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Changelog

Check [CHANGELOG](CHANGELOG.md) to get the version details.

## License

This project is licensed under the GNU AGPLv3 License - see the [LICENSE](LICENSE) file for details

