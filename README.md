# SoftDesk Support Django Restful API - Project 10

Tenth project for the online course of Python application development on OpenClassrooms.

<p align="center">
    <img    alt="Logo of the Softdesk company" 
            style="width:90%; height:auto;" 
            src="mystatic/images/softdesk_banner.png" 
            title="Logo of SoftDesk" />
</p>

## Description
>>> NEED TO BE REWORKED

This is Django REST API application created for a fictitious company called SoftDesk Support. The application functions as a locally hosted API where users can interacts with projects.


## Features
>>> NEED TO BE REWORKED:
> CF CHECK CAHIER DES CHARGES

## Installation & Launch

Ensure you have the following installed on your system:

- [Python 3.x](https://www.python.org/downloads/)

### Steps to Install

1. Clone the project or download the files to your local machine:

    ```bash
    git clone https://github.com/a-beduc/formation_project_10
    ```
2. Open a terminal and navigate to the project directory.
3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
   
        ```bash
        cd venv/Scripts
        activate
        cd ../..
        ```
    - On macOS/Linux:
   
        ```bash
        source venv/bin/activate
        ```
5. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```
6. Apply migrations:
Make sure you are in the project's root directory

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
7. Run the server:

    ```bash
    python manage.py runserver
    ``` 
8. Access the application:

    ```bash
    http://127.0.0.1:8000
    ```

### Site Administration

Access the admin panel:
    ```bash
    http://127.0.0.1:8000/admin
   
    default admin credentials:
    username: admin
    password: admin
    ```