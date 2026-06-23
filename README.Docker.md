# 🐳 Docker Setup — NYC Taxi Trip Duration Predictor

This document explains how to run the **FastAPI prediction backend** for this project inside a Docker container.

> **Note:** This Docker setup containerizes only the backend API (`app.py`). The Streamlit frontend (`streamlit_app.py`) is meant to be run locally and will connect to whichever backend it's pointed at (containerized or local).

---

## What's inside the container

The image is built from a slim Python 3.11 base and includes:
- `app.py` — the FastAPI app exposing the `/predictions` endpoint
- `data_models.py` — request schema validation
- `container_models/` — the pre-trained model, preprocessor, and output transformer used for inference

The container runs as a **non-root user** for better security, and dependencies are installed from `requirements.txt`.

---

## Building and running the backend

From the project root, build and start the container:

```bash
docker compose up --build
```

Once running, the API will be available at:
```
http://localhost:8000
```

You can test it directly via the auto-generated Swagger docs:
```
http://localhost:8000/docs
```

To stop the container:
```bash
docker compose down
```

---

## Running the Streamlit frontend alongside it

The Streamlit app expects the backend at `http://127.0.0.1:8000/predictions`. As long as the container is running and mapped to port `8000` (which it is, by default), you can start the frontend normally on your host machine:

```bash
streamlit run streamlit_app.py
```

---

## Building the image manually (without Compose)

```bash
docker build -t nyc-taxi-api .
docker run -p 8000:8000 nyc-taxi-api
```

## Deploying to the cloud

If deploying to a cloud provider with a different CPU architecture than your local machine (e.g., building on an Apple Silicon Mac for an amd64 server), specify the target platform:

```bash
docker build --platform=linux/amd64 -t nyc-taxi-api .
```

Then push it to your container registry:

```bash
docker push <your-registry>/nyc-taxi-api
```

---

## References

- [Docker's Python guide](https://docs.docker.com/language/python/)
- [Docker Compose reference](https://docs.docker.com/go/compose-spec-reference/)
