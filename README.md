# tech_trends direct cmds 
- ```bash
  python manage.py runserver 
  ```

- ```bash
  redis-server
  ```
- ```bash
  celery -A tech_trends beat --loglevel=info
  ```
- ```bash
  celery -A tech_trends worker --pool=solo -l info
  ```


# Tech Trends API

This project is a Django-based API for scraping and updating tech news trends. It uses Celery for asynchronous task management, Redis as a message broker, and a custom scraper to fetch the latest tech news.

## Features

- **Tech News Scraping**: Automatically fetches and updates the latest tech news trends.
- **Celery Integration**: Handles asynchronous tasks for updating trends every 5 minutes.
- **Redis**: Used as a message broker for Celery tasks.
- **Django REST Framework**: Provides endpoints to access the latest tech trends.

## Installation

### Prerequisites

- Python
- Redis
- Django

### Setup

1. **Clone the repository:**

    
```bash
    git clone https://github.com/kushal1o1/tech_trends.git
    cd tech_trends
```

2. **Create a virtual environment and activate it:**

    
```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

    
```bash
    pip install -r requirements.txt
```

4. **Setup Redis:**

    - Ensure Redis is installed and running on localhost:6379.
    - If Redis is not installed, follow the installation guide [here](https://redis.io/download).

5. **Configure Django settings:**

    - In tech_trends/settings.py, set your database configurations and any other necessary settings.
    - Ensure the following Celery settings are configured:

    
```python
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'
```

6. **Run migrations:**

    
```bash
    python manage.py migrate
```

7. **Start the development server:**

    
```bash
    python manage.py runserver
```

8. **Run Celery worker and beat:**

    Open two separate terminal windows and run the following commands:

    **Celery Worker:**

    
```bash
    celery -A tech_trends worker --pool=solo -l info
```


 **Celery Beat:**

    
```bash
    celery -A tech_trends beat --loglevel=info
```

## Usage

- The API will automatically fetch and update the latest tech trends every 5 minutes.
- Access the latest trends through the provided endpoints.

## Endpoints

- GET /api/trends/ - Fetch the latest tech trends.


## Contributing

Feel free to open issues or submit pull requests if you'd like to contribute to this project.

## License

This project is licensed under the MIT License.

---

**Author**: [Kushal Baral](https://github.com/kushal1o1)