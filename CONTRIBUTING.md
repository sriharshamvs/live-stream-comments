# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue with the owners of this repository before making a change.

Please note we have a Code of Conduct, please follow it in all your interactions with the project.

### Learning Resources

- [Django](https://www.djangoproject.com/start/)
- [Writing your first Django app](https://docs.djangoproject.com/en/3.2/intro/tutorial01/)

## Your First Code Contribution

Unsure where to begin contributing to the project? You can start by looking through these `beginner` and `help-wanted` issues:

- Beginner issues - issues which should only require a few lines of code, and a test or two.
- Help wanted issues - issues which should be a bit more involved than `beginner` issues.

## How Can I Contribute?

### Local Development

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
git clone git@code.swecha.org:swecha-sites/swecha-comments.git
cd swecha-comments
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
daphne -b 127.0.0.1 -p 8001 swecha_comments.asgi:application
```

## Reporting Issues/Features

This section guides you through submitting a issue for the project. Following these guidelines helps maintainers and the community understand your issue, reproduce the issue and find related issues.

### Issue Description

1. Steps to Reproduce:
2. Expected behavior:
3. Actual behavior:
4. Frequency of Occurrence:
5. Environment configuration:
6. Additional Information:

Before submitting an issue or feature request, please check the existing issues as your issue might have already been noted.

## Pull Requests

The process described here has several goals:

- Maintain the project's quality
- Fix problems that are important to users
- Engage the community in working in harmony
- Enable a sustainable system for the maintainers to review contributions

Please follow these steps to make your contribution considered:

1. Create a feature branch from `develop`, make changes and raise a PR against it
2. Please make sure that the feature branch is even with the develop branch while raising a PR.
3. Please ensure that all the testcases are passing to make sure that your changes didn't impact any other existing features

While the prerequisites above must be satisfied prior to having your pull request reviewed, the reviewer(s) may ask you to complete additional design work, tests, or other changes before your pull request can be ultimately accepted.

## Styleguides

### Git Commit Messages

- Limit the commit message to 72 characters or less
- Reference issues and pull requests liberally in the commit description
- Consider starting the commit message with an applicable keyword:
  - fix: when fixing a bug
  - feat: when new feature is added
  - test: when updating testcases
  - docs: when docs are updated
  - lint: when lint errors are fixed
  - dep: when any of the dependencies are upgraded
  - chore: for any normal task, which is done as a part of above tasks like updating build scripts, gulp tasks, etc.
