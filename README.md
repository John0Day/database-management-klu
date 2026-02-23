# DATABASE-MANAGEMENT PROJECT @ KLU - GROUP (2)
### Groupmembers: Aya, Willia, Felipe, John

# Event Management Database, Setup (VS Code)

This repository contains:
- PostgreSQL schema + seed data in `sql/`
- a Streamlit app in `app/` that connects via `app/.env`

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
## 1. Get the Project Code
### Option A, Clone (recommended)
```bash
git clone <REPO_URL>
cd event-management-db
code .
```
### Option B, Download ZIP
- Download the ZIP from GitHub and unzip it.
- Open the folder event-management-db in VS Code.
- Open a VS Code terminal and continue below.

## 2. Install PostgreSQL
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
## Windows
#### Install PostgreSQL via the official installer (PostgreSQL 16 recommended). Ensure psql is available in your terminal (PATH), or use the included “SQL Shell (psql)”.

## 3. Create Database and Load Schema/Data

#### Important: PostgreSQL must be running before you can execute createdb or psql commands.

### macOS (Homebrew start)
```bash
brew services start postgresql@16
```
### Create DB and load SQL (run from repo root event-management-db/)
```bash
createdb eventdb
psql -d eventdb -f sql/01_database_creation.sql
psql -d eventdb -f sql/02_data_insertion.sql
```
### Quick Test
```sql
psql -d eventdb -c "SELECT current_database(), current_user;"
psql -d eventdb -c "SELECT * FROM v_event_overview LIMIT 1;"
```
## 4. Configure a Database Client in VS Code (optional)
### Install any PostgreSQL client extension in VS Code.

### Connection Settings
```sql
Host: localhost (or 127.0.0.1)
Port: 5432
Database: eventdb
Username: your local Postgres role (on macOS Homebrew often your macOS username)
Password: empty unless you set one
```
## Set a password (if needed)
### Run it, for example, like this:
```sql
psql -d postgres -c "ALTER ROLE YOUR_USERNAME WITH PASSWORD 'YOUR_PASSWORD';"
```
## 5. Streamlit App Setup
### 5.1 Create venv and install dependencies

### Run from repo root:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r app/requirements.txt
```
### 5.2 Verify Streamlit
```bash
python3 -m streamlit --version
```
### 5.3 Create app/.env
### Create the file event-management-db/app/.env:
```sql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=eventdb
DB_USER=YOUR_USERNAME
DB_PASSWORD=YOUR_PASSWORD
DB_SSLMODE=prefer
```
## 6. Run the App
### Start Streamlit (run from event-management-db/app):
```bash
cd app
python3 -m streamlit run app.py
```
## 7. Reopen Later (macOS)
### 7.1 Start PostgreSQL
```bash
brew services restart postgresql@16
pg_isready -h localhost -p 5432
```
### 7.2 Start the app again
### Replace the path below with your own local folder path:
```bash
cd /path/to/your/local/event-management-db
source .venv/bin/activate
cd app
python3 -m streamlit run app.py
```
## Troubleshooting
#### Error, ECONNREFUSED

## PostgreSQL is not running or not listening on localhost:5432.
#### Check server and port
```bash
pg_isready -h localhost -p 5432
lsof -nP -iTCP:5432 | grep LISTEN
```
## Start Postgres (macOS)
```bash
brew services start postgresql@16
```
## Error, zsh: command not found: streamlit
#### Run Streamlit via Python (works even if PATH is not set):
```bash
python3 -m streamlit run app.py
```
## python not found (macOS)
#### Use python3. All commands in this README use python3.
