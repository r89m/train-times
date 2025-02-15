FROM python:3.10.13 as BACKEND_HOST
RUN pip install poetry==1.8.3

WORKDIR /source

COPY backend/poetry.lock backend/poetry.toml backend/pyproject.toml ./

RUN mkdir traintimes && touch traintimes/__init__.py && poetry install

COPY backend/traintimes ./traintimes

CMD [ "/source/.venv/bin/gunicorn", "-w", "4", "-b", "0.0.0.0", "traintimes.app:app" ]

FROM node:18.12.1 as FRONTEND_BUILD

WORKDIR /source

COPY frontend/package.json frontend/package-lock.json ./

RUN npm install

COPY frontend ./

RUN ./node_modules/.bin/ng build --output-path=dist

FROM nginx:1.22.1-alpine as FRONTEND_HOST

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy nginx config file
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy dist folder fro build stage to nginx public folder
COPY --from=FRONTEND_BUILD /source/dist /usr/share/nginx/html

# Start NgInx service
CMD ["nginx", "-g", "daemon off;"]
