# FastAPI Auth0 Integration - Example

## Getting Started

-   Python3
-   Virtualenv (for local development)
-   Poetry (for local development)
-   Make
-   Docker

## Local Development

### Setup Auth0 environment variables

1. Copy the env template file: `cp .env.template .env`.
2. Fill in the required variables:

```
AUTH0_DOMAIN=
AUTH0_API_AUDIENCE=
AUTH0_ALGORITHMS=
AUTH0_ISSUER=
AUTH0_CLIENT_ID=
AUTH0_CLIENT_SECRET=
```

### Run application locally

1. Create virtual environment: `make virtualenv`.
2. Activate virtual environment: `source .venv/bin/activate`.
3. Install dependencies: `make install-deps`.
4. Run locally: `make local-run`.

### Run application with containers locall

1. Start the containers: `make run`.
2. Stop the containers: `make down`.

### Run tests

1. Activate your virtual environment.
2. Start the tests: `make test`.
