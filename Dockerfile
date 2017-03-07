# --------------------- Base image -------------------------------------------
FROM python:2.7
MAINTAINER lewissg@tcd.ie

# --------------------- Create User and Home Dir -----------------------------
RUN useradd -m ealpha -d /code
WORKDIR /code

# --------------------- Python libraries -------------------------------------
ADD ./requirements /code/requirements

RUN pip install -r requirements/base.txt

# --------------------- Application ------------------------------------------
ADD ./ealpha /code/ealpha

ADD setup.py setup.py
RUN pip install -e .

# --------------------- Tidy Up ---------------------------------------------
RUN find . -type f -name "*.py[co]" -delete
RUN find . -type d -name "__pycache__" -delete

# --------------------- Default Entrypoint -----------------------------------
ENTRYPOINT ["ealpha"]