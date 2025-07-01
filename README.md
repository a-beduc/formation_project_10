# SoftDesk Support Django Restful API - Project 10

Tenth project for the online course of Python application development on 
OpenClassrooms.

<p align="center">
    <img    alt="Logo of the Softdesk company" 
            style="width:70%; height:auto;" 
            src="src/mystatic/images/softdesk_banner.png" 
            title="Logo of SoftDesk" />
</p>

## Description

This is Django REST API application created for a fictitious company called 
SoftDesk Support. The application functions as a locally hosted API where users
can interact with projects, issues and comments as a team of project's 
contributors. Developed with **Django Rest Framework**, it proposes an 
authentication system using **JWT** (Json Web Token), access based on 
permissions and basic filters.


## Installation & Launch

Ensure you have the following installed on your system:

- [Python 3.7+](https://www.python.org/downloads/)
  - Tested with Python 3.12 should work on Python 3.7+.
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

### Steps to Install

**1. Clone the project or download the files to your local machine:**

    ```bash
    git clone https://github.com/a-beduc/formation_project_10
    ```
   
**2. Create virtual environnement and install depencencies**

<details>
<summary>With Pip</summary>

+ Create a virtual environment

    ```
    python -m venv .venv
    
    source .venv/bin/activate  # Linux
    or
    .venv\Scripts\activate     # Windows
    ```

+ Install dependencies

   ```
   pip install -r requirements.txt
   ```
</details>

<details>
<summary>With PipEnv</summary>

+ Create a virtual environment

    ```
    pipenv shell
    ```

+ Install dependencies:

    ```
    pipenv install            # Only needed dependencies
    or
    pipenv install --dev      # Additional dev tools (linters)
    ```
   
</details>

-----

<details>
<summary><b>3. (Optional) If you want a new and clean Database</b></summary>

- *Delete the current data*
     - *Delete the db.sqlite3 in the src/ directory*

   - *Apply migrations*
     - *Make sure you are in the project's src/ directory*

         ```
         python manage.py migrate
         ```
   - Create an admin user to access the Admin panel. 
   *You can follow the process to create a new superuser with this 
   [w3school tutorial](https://www.w3schools.com/django/django_admin_create_user.php)*

</details>

**4. Generate a SECRET_KEY:**
   * Create a .env file at the root of the project (not in /src) by copying the content .env.example 
   * Go to https://djecrety.ir/ to generate a Django SECRET_KEY 
   * Paste the generated key as a string in the .env
   * It should look like : SECRET_KEY='your_unique_generated_secret_key'

**5. Navigate to the src directory and start the server:**

```
python manage.py runserver
``` 

**6. Access the application:**
    
With your web browser, open the link : http://127.0.0.1:8000 or http://127.0.0.1:8000/api/v1/


### Site Administration

Access the admin panel: http://127.0.0.1:8000/admin
    
   ```
   default admin credentials:
   username: admin
   password: 53CR37!4dm1n
   ```

### Test Users
   ```
   username: user_one     | password: 53CR37!U53R
   username: user_two     | password: 53CR37!U53R
   username: user_thr     | password: 53CR37!U53R
   ```

## Postman Documentation
A postman collection is available at 
[Documentation postman](https://documenter.getpostman.com/view/42454429/2sB34ZqPrd).

It is not a test suite for the API but a written reference of this API endpoints.


## API Endpoints
Every end points of the API except for the 
[authentication endpoints](#authentication) needs to carry a way to 
authenticate users, in the form of a Json Web Token.
Some endpoints require some permissions to be reached, explained in the 
"Permission" part following every table. 
The list endpoints come with basic filters, consult the "Filters" part 
following a table to learn more.

---

### Authentication
| # | API Endpoints                      | HTTP Method | URL base: `http//127.0.0.1:8000/api/v1` |
|---|------------------------------------|-------------|-----------------------------------------|  
| 1 | Receive a Json Web Token           | `POST`      | `/token/`                               |
| 2 | Obtain a new access Json Web Token | `POST`      | `/token/refresh/`                       |

#### Permissions
1. Token request, can be reached by anyone.
2. Token request, can be reached by anyone.

---

### Users
| #                | API Endpoints            | HTTP Method       | URL base: `http//127.0.0.1:8000/api/v1` |
|------------------|--------------------------|-------------------|-----------------------------------------|  
| 3 <a id="3"></a> | Get the list of users    | `GET`             | `/users/`                               |
| 4                | Get the detail of a user | `GET`             | `/users/:user_id/`                      |
| 5                | Create a new user        | `POST`            | `/users/`                               |
| 6                | Delete a user            | `DELETE`          | `/users/:user_id/`                      |
| 7                | Update a user            | `PUT` or `PATCH`  | `/users/:user_id/`                      |

#### Permissions
3. List endpoint, can be reached by any user.
4. Detail endpoint, can be reached by the user with the specified ID or admin.
5. Create endpoint, can only be reached by admin.
6. Delete endpoint, can be reached by the user with the specified ID or admin.
7. Update endpoint, can be reached by the user with the specified ID.

#### Filters (available for [3](#3))
- `/users/?user_id=<:int>` : Get the user where the specified integer 
correspond to their id in the database.
- `/users/?username=<:name>` or `/users/?username_contains=<:string>`: 
Get the users whose username correspond to the string chain. The former 
performs a search with an exact match while the latter filters based on the 
username containing the search term. The search is case-free. 

---

### Projects
| #                | API Endpoints               | HTTP Method       | URL base: `http//127.0.0.1:8000/api/v1` |
|------------------|-----------------------------|-------------------|-----------------------------------------|  
| 8 <a id="8"></a> | Get the list of projects    | `GET`             | `/projects/`                            |
| 9                | Get the detail of a project | `GET`             | `/projects/:project_id/`                |
| 10               | Create a new project        | `POST`            | `/projects/`                            |
| 11               | Delete a project            | `DELETE`          | `/projects/:project_id/`                |
| 12               | Update a project            | `PUT` or `PATCH`  | `/projects/:project_id/`                |

#### Permissions
8. List endpoint, can be reached by any user.
9. Detail endpoint, can be reached by the project's author and its contributors.
10. Create endpoint, can be reached by any user.
11. Delete endpoint, can be reached by the project's author.
12. Update endpoint, can be reached by the project's author.

#### Filters (available for [8](#8))
- `/projects/?project_id=<:int>` : Get the project where the specified integer 
correspond to its id in the database.
- `/projects/?title=<:name>` or `/projects/?title_contains=<:string>`: Get the 
projects whose title correspond to the string chain. The former performs a 
search with an exact match while the latter filters based on the title 
containing the search term. The search is case-free.
- `/projects/?type=<:string>` : Get a list of project filtered by their type. 
The value must match **exactly** one of the following predefined options 
(case-sensitive):
  - `"BACKEND"`
  - `"FRONTEND"`
  - `"IOS"`
  - `"ANDROID"`
- `/projects/?author_id=<:int>` : Get the projects where the specified integer 
correspond to its author user_id in the database.
- `/projects/?my_projects=<:bool>` : Get the projects where the authenticated 
user is either the author or a contributor.

---

### Contributors
| #                  | API Endpoints                            | HTTP Method | URL base: `http//127.0.0.1:8000/api/v1`                        |
|--------------------|------------------------------------------|-------------|----------------------------------------------------------------|  
| 13 <a id="13"></a> | Get the list of a project contributors   | `GET`       | `/projects/:project_id/contributors/`                          |
| 14                 | Get the detail of a contributor relation | `GET`       | `/projects/:project_id/contributors/:contributor_relation_id/` |
| 15                 | Add a contributor to the project         | `POST`      | `/projects/:project_id/contributors/`                          |
| 16                 | Remove a contributor to the project      | `DELETE`    | `/projects/:project_id/contributors/:contributor_relation_id/` |

#### Permissions
13. List endpoint, can be reached by the project's author and contributors.
14. Detail endpoint, can be reached by the project's author and the user 
with the id of the relationship.
15. Create endpoint, can be reached by the project's author.
16. Delete endpoint, can be reached by the project's author and the user with 
the id of the relationship. 

#### Filters (available for [13](#13))
- `/projects/:project_id/contributors/?user_id=<:int>` : Get the contributor 
relation in the project where the specified integer correspond to an user_id 
in the database.

---

### Issues
| #                  | API Endpoints               | HTTP Method       | URL (base: http//127.0.0.1:8000/api/v1)   |
|--------------------|-----------------------------|-------------------|-------------------------------------------|  
| 17 <a id="17"></a> | Get the list of projects    | `GET`             | `/projects/:project_id/issues/`           |
| 18                 | Get the detail of a project | `GET`             | `/projects/:project_id/issues/:issue_id/` |
| 19                 | Create a new project        | `POST`            | `/projects/:project_id/issues/`           |
| 20                 | Delete a project            | `DELETE`          | `/projects/:project_id/issues/:issue_id/` |
| 21                 | Update a project            | `PUT` or `PATCH`  | `/projects/:project_id/issues/:issue_id/` |


#### Permissions
17. List endpoint, can be reached by the project's author and contributors.
18. Detail endpoint, can be reached by the project's author and its contributors.
19. Create endpoint, can be reached by the project's author and its contributors.
20. Delete endpoint, can be reached by the **issue's author**.
21. Update endpoint, can be reached by the **issue's author**.

#### Filters (available for [17](#17))
- `/projects/:project_id/issues/?issue_id=<:int>` : Get the issue where the 
specified integer correspond to its id in the database.
- `/projects/:project_id/issues/?title=<:name>` or 
`/projects/:project_id/issues/?title_contains=<:string>` : Get the issue(s) 
whose title correspond to the string chain. The former performs a search with 
an exact match while the latter filters based on the title containing the 
search term. The search is case-free.
- `/projects/:project_id/issues/?author_id=<:int>` : Get the issues where the
specified integer correspond to its author user_id in the database.
- `/projects/:project_id/issues/?assigned_to=<:int>` : Get the issues where the
specified integer correspond to the user it has been assigned to in the 
database.
- `/projects/:project_id/issues/?priority=<:string>` : Get a list of this 
project issues filtered by their priority. The value must match **exactly** one
of the following predefined options (case-sensitive):
  - `"LOW"`
  - `"MEDIUM"`
  - `"HIGH"`
- `/projects/:project_id/issues/?type=<:string>` : Get a list of this 
project issues filtered by their type. The value must match **exactly** one
of the following predefined options (case-sensitive):
  - `"BUG"`
  - `"FEATURE"`
  - `"TASK"`
- `/projects/:project_id/issues/?status=<:string>` : Get a list of this 
project issues filtered by their status. The value must match **exactly** one
of the following predefined options (case-sensitive):
  - `"TO_DO"`
  - `"IN_PROGRESS"`
  - `"FINISHED"`

---

### Comments
| #                  | API Endpoints               | HTTP Method       | URL base: `http//127.0.0.1:8000/api/v1`                          |
|--------------------|-----------------------------|-------------------|------------------------------------------------------------------|  
| 22 <a id="22"></a> | Get the list of comments    | `GET`             | `/projects/:project_id/issues/:issue_id/comments/`               |
| 23                 | Get the detail of a comment | `GET`             | `/projects/:project_id/issues/:issue_id/comments/:comment_uuid/` |
| 24                 | Create a new comment        | `POST`            | `/projects/:project_id/issues/:issue_id/comments/`               |
| 25                 | Delete a comment            | `DELETE`          | `/projects/:project_id/issues/:issue_id/comments/:comment_uuid/` |
| 26                 | Update a comment            | `PUT` or `PATCH`  | `/projects/:project_id/issues/:issue_id/comments/:comment_uuid/` |

#### Permissions
22. List endpoint, can be reached by the project's author and contributors.
23. Detail endpoint, can be reached by the project's author and its contributors.
24. Create endpoint, can be reached by the project's author and its contributors.
25. Delete endpoint, can be reached by the **comment's author**.
26. Update endpoint, can be reached by the **comment's author**.

#### Filters (available for [22](#22))
- `/projects/:project_id/issues/:issue_id/comments/?author_id=<:int>` : 
Get the comments where the specified integer correspond to its author user_id 
in the database.

## About
Application created as a student's project for the online course on OpenClassrooms; Python Application Developer.
