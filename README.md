[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/powered-by-responsibility.svg)](https://forthebadge.com)

## Quick Start

___

1) git clone https://github.com/zabit923/media-uploader.git
2) create .env file in ./src

.env file example:
```commandline
POSTGRES_DB=YOUR_DB
POSTGRES_USER=postgres
POSTGRES_PASSWORD=YOUR_DB_PASS
DB_HOST=database
DB_PORT=5432

DEBUG=False

SECRET_KEY=YOUR_SECRET
```
3) docker-compose up -d

___
## Guide
1) > Documentation | http://127.0.0.1:8000/docs
2) > User registration |
http://127.0.0.1:8000/users/register
3) > Upload audio | http://127.0.0.1:8000/record
4) > Download audio | http://127.0.0.1:8000/record?audio_id=uuid4&user_id=1
5) > Admin panel | http://127.0.0.1:8000/admin/login
```uuid4 access_token into password field```
## `Project Styling` ✅

| Tools          |                                                                                                                                                                                                                                                                                      Description                                                                                                                                                                                                                                                                                       |
| -------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| `isort`        |                                                                                                                                                                                                         isort your python imports for you so you don't have to. isort is a Python utility / library to sort imports alphabetically, and automatically separated into sections.                                                                                                                                                                                                         |
| `black`        |                       Black is the uncompromising Python code formatter. By using it, you agree to cede control over minutiae of hand-formatting. In return, Black gives you speed, determinism, and freedom from pycodestyle nagging about formatting. You will save time and mental energy for more important matters. Blackened code looks the same regardless of the project you're reading. Formatting becomes transparent after a while and you can focus on the content instead. Black makes code review faster by producing the smallest diffs possible.                       |
| `pre-commit`   | Git hooks allow you to run scripts any time you want to commit or push. This lets us run all of our linting and tests automatically every time we commit/push. Git hook scripts are useful for identifying simple issues before submission to code review. We run our hooks on every commit to automatically point out issues in code such as missing semicolons, trailing whitespace, and debug statements. By pointing these issues out before code review, this allows a code reviewer to focus on the architecture of a change while not wasting time with trivial style nitpicks. |

For more information on `Project Styling` check out the detailed guide 👉 [How to set up a perfect Python project](https://sourcery.ai/blog/python-best-practices/)
