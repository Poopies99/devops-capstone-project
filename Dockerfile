FROM python:3.9-slim

# Install libpq (Make sure to update versions and dependencies as needed)
RUN apt-get update && \
    apt-get install -y libpq-dev

# Sets the working directory for COPY, RUN, CMD, Entrypoint and ADD to /app
WORKDIR /app

# Copy requirements.txt from project directory to working directory
COPY requirements.txt .

# Install pylibs
RUN pip install --no-cache-dir -r requirements.txt

# Copy service package
COPY service/ ./service/

# Create non-root user (Change the owner of all files and directories to new user)
RUN useradd --uid 1000 theia && chown -R theia /app

# Switch to new user
USER theia

# --- Run the service
# Open Port in container
EXPOSE 8080

# 1. Starts a Gunicorn servicer
# 2. Listen to on all network interfaces of container on port 8080
# 3. Log information message, warning, errors and critical messages
# 4. Specifies the application module and the application instance
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "service:app"]


#LABEL authors="chris"
#ENTRYPOINT ["top", "-b"]