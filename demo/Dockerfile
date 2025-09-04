# Stage 1: Build stage
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production stage
FROM python:3.9-slim

# Install MySQL client
RUN apt-get update && apt-get install -y default-mysql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application files
COPY app.py .
COPY templates/ templates/
COPY setup.sql .

# Create entrypoint script
RUN echo '#!/bin/bash\n\
mysql -h$DB_HOST -u$DB_USER -p$DB_PASSWORD < setup.sql\n\
python app.py' > entrypoint.sh && chmod +x entrypoint.sh

EXPOSE 5000

CMD ["./entrypoint.sh"]