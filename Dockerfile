FROM python:3.9-slim


WORKDIR /techtrends

RUN python3 -m venv /venv

COPY requirements.txt .

RUN /venv/bin/pip install --upgrade pip \
 && /venv/bin/pip install -r requirements.txt


COPY . .

ENV PATH="/venv/bin:$PATH"

ENV DJANGO_SETTINGS_MODULE=tech_trends.settings


EXPOSE 8000



CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]