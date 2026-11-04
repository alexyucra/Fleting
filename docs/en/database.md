## 🗄️ Database Setup

### Quick MySQL with Docker

Get a MySQL 8 container running in one line:

#### Linux / macOS:

```bash
docker run --name fleting_mysql -e MYSQL_ROOT_PASSWORD=fleting123 -e MYSQL_DATABASE=fleting -p 3306:3306 -d mysql:8.0 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

#### Windows (PowerShell):

```bash
docker run --name fleting_mysql -e MYSQL_ROOT_PASSWORD=fleting123 -e MYSQL_DATABASE=fleting -p 3306:3306 -d mysql:8.0 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

#### Windows (CMD):

```bash
docker run --name fleting_mysql -e MYSQL_ROOT_PASSWORD=fleting123 -e MYSQL_DATABASE=fleting -p 3306:3306 -d mysql:8.0 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

<details> <summary><strong>🔧 MySQL Connection Details</strong></summary>

|Setting	|Value|
|-----------|-----|
|Host	    |localhost|
|Port	    |3306|
|User	    |root|
|Password	|fleting123|
|Database	|fleting|

- To verify the container is running:

```bash
docker ps
docker logs fleting_mysql
```

- To access MySQL directly:

```bash
docker exec -it fleting_mysql mysql -uroot -pfleting123
```

- To stop the container:

```bash
docker stop fleting_mysql
docker rm fleting_mysql
```

</details>

### Custom Port Configuration
If your MySQL container is running on a different port (e.g., 3366), update your `configs/database.py`:

```py
DATABASE = {
    "ENGINE": "mysql",
    "MYSQL": {
        "HOST": "localhost",
        "PORT": 3366,  # Change to your port
        "USER": "root",
        "PASSWORD": "fleting123",
        "NAME": "fleting",
        # ...
    }
}
```

### Database Commands

|Command	|Description|
|-----------|-----------|
|fleting db init	        |Initialize database structure|
|fleting db init --mysql	|Initialize with MySQL (if using MySQL)|
|fleting db migrate	        |Run pending migrations|
|fleting db seed	        |Seed the database with initial data|
|fleting db make <name>	    |Create a new migration|
|fleting db rollback	    |Rollback the last migration|
|fleting db status	        |Check migration status|
|fleting db model pull	    |Generate models from existing tables|
|fleting shell	            |Interactive database console|

## 🚀 Recommended Development Workflow

### 1. Set up your environment

```bash
# Using uv (recommended)
uv init myapp
cd myapp
uv venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows PowerShell
uv pip install flet fleting

# Or using venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows PowerShell
pip install flet fleting
```

### 2. Create your project
```bash
# With SQLite (default)
fleting init myapp

# With MySQL
fleting init myapp --mysql
cd myapp
```

### 3. Initialize database
```bash
# For SQLite
fleting db init

# For MySQL (after setting up container)
fleting db init --mysql
```

### 4. Start developing

```bash
# Create a new page
fleting create page dashboard

# Run the app
fleting run
```

### 5. Database migrations

```bash
# Create a migration
fleting db make add_user_profile

# Apply it
fleting db migrate

# Seed data
fleting db seed
```

## 📊 Environment Setup Comparison

|Tool	|Speed	|Ease of Use	|Recommended For|
|-------|-------|---------------|---------------|
|uv	    |⚡ Fastest	   |✅ Easy	      |New projects, production|
|venv	|🐢 Standard	|✅ Standard	   |All projects|
|Poetry	|🐢 Standard	|⚠️ Complex	    |Large projects with dependencies|
|Conda	|🐢 Slower	    |⚠️ Complex	    |Data science projects|

## 💡 Pro Tips

<details> <summary><strong>🔹 Use uv for faster dependency management</strong></summary>
uv is 10-100x faster than pip and poetry. Install it with:

```bash
pip install uv
```

</details><details> <summary><strong>🔹 Use Docker for MySQL development</strong></summary>

Get a MySQL 8 container in one line:

```bash
docker run --name fleting_mysql -e MYSQL_ROOT_PASSWORD=fleting123 -e MYSQL_DATABASE=fleting -p 3306:3306 -d mysql:8.0 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```
</details><details> <summary><strong>🔹 Use .env for sensitive data</strong></summary>

Create a .env file for database credentials and load it with python-dotenv.

</details> 