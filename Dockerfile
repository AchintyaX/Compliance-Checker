# Use an official Python runtime as a parent image
FROM    python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install poetry
RUN pip install uvicorn[standard]

RUN poetry config virtualenvs.create false 

RUN poetry install --no-cache --no-root

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
