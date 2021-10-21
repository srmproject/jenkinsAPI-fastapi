FROM python:3.7.2-alpine AS builder

ARG USER=fastapi
ARG USERHOME=/home/$USER

RUN adduser -D $USER \
    && apk add gcc musl-dev python3-dev libffi-dev openssl-dev


FROM builder
ARG USER=fastapi
ARG USERHOME=/home/$USER
ENV MODE=dev

COPY --chown=$USER:$USER ./app $USERHOME/app
RUN pip install --upgrade pip \
    && pip install -r $USERHOME/app/requirements.txt

USER $USER
WORKDIR $USERHOME/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
