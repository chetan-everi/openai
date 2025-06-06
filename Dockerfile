FROM python:3.10-slim
 
# Set the working directory in the container
WORKDIR /app
 
# Copy the requirements.txt file into the container
COPY requirements.txt .
 
# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the rest of your application code into the container
COPY . .
 
# Specify the command to run your application
CMD ["python", "app.py"]
