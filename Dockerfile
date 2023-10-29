# Step 1: Use official lightweight Python image as base OS.
FROM tiangolo/uvicorn-gunicorn:python3.8-slim

# Step 2. Copy local code to the container image.
WORKDIR /app
COPY . .

# Step 3. Install production dependencies.
RUN pip install -r requirements.txt

# Step 4: Run the web service on container startup using uvicorn.
ENV PORT=8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
