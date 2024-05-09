# For more information, please refer to https://aka.ms/vscode-docker-python
# Use the official Conda image as a base image
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the Conda environment YAML file into the container
COPY environment.yml /app

# Create the Conda environment
RUN conda env create -f environment.yml

# Activate the Conda environment
SHELL ["conda", "run", "-n", "dashboard2", "/bin/bash", "-c"]

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port number that the Dash application should run on
EXPOSE 8050

# Command to run the Dash application within the Conda environment
CMD ["conda", "run", "--no-capture-output", "-n", "dashboard2", "python", "index.py"]
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
