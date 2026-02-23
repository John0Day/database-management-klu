# DATABASE-MANAGEMENT PROJECT @ KLU - GROUP (2)
### Groupmembers: Aya, Willia, Felipe, John

## Notice, Python version
Python **3.12** is the **last supported version for this project setup**. Newer Python versions may cause dependency issues in the app environment and can lead to a non-smooth local PostgreSQL integration on some systems. Use **Python 3.12.x**.

## Project structure
```text
event-management-db/
  app/
    app.py
    db.py
    transactions.py
    requirements.txt
    .env          # create locally
  .venv/          # created locally at repo root
  sql/
    01_database_creation.sql
    02_data_insertion.sql
    03_transactions.sql
```
## Requirements
- PostgreSQL 16 (or compatible) running on `localhost:5432`
- Python 3.12

## Setup
1) Clone and enter
```bash
git clone <REPO_URL> event-management-db
cd event-management-db
```
2) Install PostgreSQL via brew
### macOS (Homebrew, PostgreSQL 16)
### Install Homebrew (if missing)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
### Install PostgreSQL 16
```bash
brew update
brew install postgresql@16
```
### Add PostgreSQL tools to PATH (zsh)
```bash
echo 'export PATH="$(brew --prefix)/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```
### Start PostgreSQL server
```bash
brew tap homebrew/services
brew services start postgresql@16
```
### Verify it is running
```bash
psql --version
pg_isready -h localhost -p 5432
```
```text
Expected: accepting connections.
```
3) Create DB and load schema + data (Postgres must be running)
```bash
createdb eventdb
psql -d eventdb -f sql/01_database_creation.sql
psql -d eventdb -f sql/02_data_insertion.sql
```
4) Create virtual env and install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r app/requirements.txt
```
5) Configure env
- Copy the template: `cp app/.env.example app/.env`
- Edit `app/.env` and set your Postgres user/password if needed.

6) Run the app
```bash
cd app
python3 -m streamlit run app.py
```

## Restart later
```bash
cd /path/to/event-management-db
source .venv/bin/activate
cd app
python3 -m streamlit run app.py
```

## Notes
- VS Code/Postgres extensions are optional; not required to run the app.
- If `psql` is missing, install Postgres and ensure its bin directory is on PATH (e.g., Homebrew: `$(brew --prefix)/opt/postgresql@16/bin`).
