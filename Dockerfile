# ---- Base Image ----
FROM python:3.12-slim

# ---- Working Directory ----
WORKDIR /app

# ---- Dependencies ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy Source Code ----
COPY . .

# ---- Environment ----
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# ---- Expose Flask Port ----
EXPOSE 5000

# ---- Run with Gunicorn (production WSGI server) ----
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]