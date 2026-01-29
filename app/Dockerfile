# Use a lightweight Python base image
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port (Streamlit defaults to 8501, Dash to 8050)
# Change this if you configured a different port in your code
EXPOSE 8501

# The command to run the app
# UPDATE 'app.py' to match your main filename (e.g., dashboard.py, main.py)

CMD ["streamlit", "run", "fraud_viz.py", "--server.port=8501", "--server.address=0.0.0.0"]
