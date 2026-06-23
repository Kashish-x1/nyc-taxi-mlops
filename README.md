# 🚕 NYC Taxi Trip Duration Predictor

An end-to-end Machine Learning project that predicts how long a taxi trip in New York City will take, based on pickup/dropoff location, time of day, and other trip details.

This project demonstrates a complete MLOps workflow — from raw data to a deployed, interactive prediction app.

---

## 📌 What this project does

Given a **pickup location**, **dropoff location**, and basic trip details (date, hour, passenger count, vendor), the model predicts the **expected trip duration in minutes**. It mirrors the kind of ETA prediction used by real ride-hailing apps like Uber and Ola.

The dataset is based on the **Kaggle NYC Taxi Trip Duration** competition.

---

## 🏗️ Project Architecture

The project follows a modular, reproducible ML pipeline managed with **DVC**:

```
Raw data (zipped)
      ↓  extract_dataset
Extracted CSVs
      ↓  make_dataset (train/val split)
Interim data
      ↓  modify_features
Transformed data
      ↓  build_features (feature engineering)
Built features
      ↓  data_preprocessing (scaling/encoding)
Final processed data
      ↓  train_model (RandomForest / XGBoost)
Trained model
      ↓  predict_model + plot_results
Predictions & evaluation plots
```

Each stage is defined in `dvc.yaml`, with hyperparameters controlled via `params.yaml`, making the entire pipeline reproducible with a single command: `dvc repro`.

---

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| Data versioning & pipeline | DVC |
| Modeling | scikit-learn (RandomForest), XGBoost |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Geocoding | OpenStreetMap Nominatim API |
| Mapping | Folium |
| Containerization | Docker |
| CI/CD | GitHub Actions |

---

## 🖥️ Interactive Frontend

On top of the FastAPI prediction backend, this project includes a **Streamlit web app** that lets users:

- Enter pickup and dropoff **addresses** (auto-converted to coordinates via geocoding — no manual lat/long needed)
- Pick trip date, hour, passenger count, and vendor
- Get an instant **predicted trip duration** and **estimated fare**
- View the pickup → dropoff route on an interactive map

---

## ⚙️ Setup & Usage

### 1. Clone the repo and create a virtual environment
```bash
git clone https://github.com/Kashish-x1/nyc-taxi-mlops.git
cd nyc-taxi-mlops
python -m venv venv
venv\Scripts\activate   # on Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
pip install -e .
```

> **Note:** This project must be installed as an editable package (`pip install -e .`) for internal imports (`src/...`) to work correctly.

### 3. Add the raw dataset
Download `train.zip` and `test.zip` from the Kaggle NYC Taxi Trip Duration competition and place them in:
```
data/raw/zipped/train.zip
data/raw/zipped/test.zip
```

### 4. Run the ML pipeline
```bash
dvc repro
```
This runs every stage — extraction, preprocessing, feature engineering, training, evaluation — end to end.

### 5. Start the backend API
```bash
uvicorn app:app --reload
```

### 6. Start the frontend app
In a second terminal:
```bash
streamlit run streamlit_app.py
```

---

## 📊 Model Performance

| Metric | Train | Validation |
|---|---|---|
| R² Score | 0.808 | 0.801 |

The close train/validation scores indicate the model generalizes well without significant overfitting.

---

## 📁 Project Structure

```
├── data/                  # Raw, interim, and processed data (DVC-tracked)
├── src/                   # Source code (data, features, models, visualization)
├── models/                # Trained models & transformers
├── plots/                 # Evaluation plots
├── app.py                 # FastAPI backend
├── streamlit_app.py       # Streamlit frontend
├── dvc.yaml               # DVC pipeline definition
├── params.yaml            # Pipeline hyperparameters
└── requirements.txt       # Python dependencies
```

---

