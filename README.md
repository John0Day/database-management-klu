# DATABASE-MANAGEMENT PROJECT @ KLU - GROUP ()
### Groupmembers: Aya, Willia, Felipe, John
How to Install the Project
---
This Setup manual is only ment for a VS Code setup. If you want to use the Database differently, you can also just download the sql files manually.

#### 1. Install Homebrew on Mac if you haven't already. Otherwise use WSL if on Windows.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. PostgreSQL install.

```bash
brew update
brew install postgresql@16
```

#### 3. Start PostgreSQL as Service.

```bash
brew services start postgresql@16
```

#### 4. Set Tools in Path so they can be used.

```bash
echo "export PATH=\"$(brew --prefix)/opt/postgresql@16/bin:\$PATH\"" >> ~/.zshrc
source ~/.zshrc
```

Test if your Ok so far. (Optional): 

```bash
psql --version
createdb --version
```

#### 5. Create the databse called "eventdb".

```bash
createdb eventdb
```

#### 6. Load schema and data from repo.

```bash
psql -d eventdb -f sql/01_database_creation.sql
psql -d eventdb -f sql/02_data_insertion.sql
```

#### 7. Next you got to install a Databse client like the VS Extension (PostgreSQL).

- You can find it in the Extension Marketplace it has a blue elephant head logo and says "Database Client" in the bottom.

#### 8. Create a connection "New Connection" (input your information like this).

```dotenv
Host: localhost
Port: 5432
Username: YOUR_USERNAME (Mac or Windows username)
Password: YOUR_PASSWORD
Database: eventdb
```

Press Connect, you should see your database in the top left corner with a green light indicator. (It should say: localhost@5432)

#### 9. Test a Query. (Navigate to the Menubar on the left and look for a Databse icon.
Navigate to eventdb/Query -> click the plus sign and add your code to the query. You can select the green run symbol in the top right corner to run the query.

```sql
Create a new Query and insert:
SELECT current_database(), current_user;
SELECT * FROM v_event_overview LIMIT 1;
```

run the Query and check the output.

#### 10. App setup (Creates a virutal environment for Python and installs all the needed dependencies)
Python 3.12 is recommended! Any higher Version might produce compatibality issues.

```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

afterwards test if streamlit is installed:

```bash
streamlit --version
```

#### 11. Setup your enivronment file in app/.env

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=eventdb
DB_USER=YOUR_USER_NAME!
DB_PASSWORD=YOUR_PASSWORD_HERE!
DB_SSLMODE=prefer
```

if you want to set a password: `psql -d postgres -c "ALTER ROLE <YOUR_USER> WITH PASSWORD '<PASSWORD>';"`

#### 12. Start APP. (Should open a new Browserwindow)

```bash
streamlit run app.py
```

#### 13. In case you closed VS Code and want to open the Project up back again

```bash
brew services restart postgresql@16
pg_isready
```
#### !Navigate to the /app folder. (Drag and Drop in Terminal works too!)

```bash
cd "/Users/YOUR-PATH/event-management-db/app"
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

#### 13. (Optional).
You can run the Transactions from Assignment 6 in the Database automatically.
```bash
psql -d eventdb -f sql/03_transactions.sql
```
