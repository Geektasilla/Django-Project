# NEW_Django

A new Django project.

## Prerequisites

This project uses `mysqlclient` to connect to a MySQL database. You may need to install some system-level dependencies before you can install `mysqlclient`.

- **Windows:**
  On Windows, you need the C build tools and the MySQL C connector libraries.
  1.  Install **Microsoft C++ Build Tools**. Go to the [Visual Studio downloads page](https://visualstudio.microsoft.com/visual-cpp-build-tools/), download the tools, and during installation, make sure to select the "C++ build tools" workload.
  2.  Download and install the **MySQL Connector/C** from the [official MySQL website](https://dev.mysql.com/downloads/connector/c/). This provides the necessary libraries to connect to MySQL.

- **Debian/Ubuntu:**
  ```bash
  sudo apt-get install build-essential libmysqlclient-dev
  ```

- **Red Hat/CentOS:**
  ```bash
  sudo yum install gcc mysql-devel
  ```

- **macOS (using Homebrew):**
  ```bash
  brew install mysql
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd NEW_Django
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
5. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Apply the migrations:
   ```bash
   python manage.py migrate
   ```
2. Run the development server:
   ```bash
   python manage.py runserver
   ```
3. Open your browser and go to `http://127.0.0.1:8000/`.
