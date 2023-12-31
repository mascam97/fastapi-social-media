# FastAPI Social Media

_Minimal System to manage user and publications._

### Project goal by mascam97 :goal_net:

Personal project to learn FastAPI / Python. 

### Achievements 2023 :star2:

- [x] Added a CRUD for publications.
- [x] Implemented authentication
- [x] Added testing
- [ ] Added a CRUD for comments
- [ ] Added endpoints to register, logout and update profile
- [ ] Configured hexagonal architecture
- [ ] Added a Docker container
- [ ] Implemented GraphQL
- [ ] Implemented a MySQL database
- [ ] Included a CI/CD pipeline with GitHub Actions
- [x] Implemented best practices like dotenv and fix PEP 8 style

## Getting Started :rocket:

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites :clipboard:

The programs you need are:

- Python 3.10.12.
- pip 22.0.2 .

### Installing 🔧

Install the Python dependencies:

```
pip install -r requirements.txt
```

The, copy the .env.example file to .env and fill the variables with your own values.

```
cp .env.example .env
```

Finally, run the application with

```
uvicorn main:app —reload
```

## Running the tests ⚙️

To run the tests, run the following command

```
python3 -m pytest
```

### Include more dependencies :package:

To include more dependencies into requirements.txt, run the following command

```
pip3 freeze > requirements.txt
```

### Code style :art:

To check the code style, and check PEP8 standard, run the following command

```
autopep8 --in-place --recursive .
```

### Built With 🛠️

-   [FastAPI](https://fastapi.tiangolo.com/) - FastAPI framework, high performance, easy to learn, fast to code, ready for production.
-   [pytest](https://docs.pytest.org/en/7.4.x/) - The pytest framework makes it easy to write small tests, yet scales to support complex functional testing.
-   [autopep8](https://pypi.org/project/autopep8/) - A tool that automatically formats Python code to conform to the PEP 8 style guide.

### Authors

-   Martín S. Campos [mascam97](https://github.com/mascam97)

### Contributing

You're free to contribute to this project by submitting [issues](https://github.com/mascam97/fastapi-social-media/issues) and/or [pull requests](https://github.com/mascam97/fastapi-social-media/pulls).

### License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

### References :books:

- [Fast API intermediate course](https://platzi.com/cursos/fastapi/)
- [FastAPI introduction course](https://platzi.com/cursos/fastapi-modularizacion-datos/)