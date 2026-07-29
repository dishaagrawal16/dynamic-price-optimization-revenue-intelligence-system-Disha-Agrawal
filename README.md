# 🚀 PricePilot AI – Dynamic Pricing Optimization & Revenue Intelligence System

An AI-powered Dynamic Pricing & Revenue Intelligence platform that helps businesses optimize product pricing using historical sales data, competitor pricing, inventory levels, and demand forecasting.

---

## 📌 Project Overview

PricePilot AI enables businesses to:

- 📈 Predict optimal product prices
- 🛒 Analyze sales trends
- 📦 Monitor inventory levels
- 💰 Compare competitor prices
- 🤖 Generate AI-powered pricing recommendations
- 📊 Visualize revenue analytics through interactive dashboards

---

## ✨ Features

- 🔐 User Authentication (JWT)
- 👥 Role-Based Access Control
- 📦 Product Management
- 💵 Dynamic Price Prediction
- 📈 Demand Forecasting
- 🛍 Competitor Price Analysis
- 📊 Revenue Dashboard
- 📉 Price History Tracking
- 📦 Inventory Management

---

## 🏗 System Architecture

```text
                         USER
                           │
                           ▼
                React Frontend (UI)
                           │
                     REST API Calls
                           │
                           ▼
                  FastAPI Backend
       ┌────────────────────────────────────┐
       │ Authentication (JWT)               │
       │ Product Management                 │
       │ Pricing Prediction API             │
       │ Revenue Analytics API              │
       └────────────────────────────────────┘
                │                   │
                ▼                   ▼
      PostgreSQL Database     Machine Learning
                │                   │
                └──────────┬────────┘
                           ▼
                Revenue Dashboard
```

---

## 🗄 Database Design (ER Diagram)

### Entities

- User
- Product
- Sales
- Inventory
- Competitor Price
- Price History
- Price Prediction

### Relationships

| Entity | Relationship |
|---------|--------------|
| User → Product | One-to-Many |
| Product → Sales | One-to-Many |
| Product → Inventory | One-to-One |
| Product → Competitor Price | One-to-Many |
| Product → Price History | One-to-Many |
| Product → Price Prediction | One-to-Many |

---

## 🛠 Tech Stack

### Frontend

- React.js
- Vite
- Axios
- Recharts

### Backend

- FastAPI
- Python
- JWT Authentication
- REST APIs

### Database

- PostgreSQL

### Machine Learning

- Scikit-Learn
- XGBoost
- Pandas
- NumPy

### Deployment

- Docker
- GitHub

---

## 📂 Project Structure

```
PricePilot-AI
│
├── backend/
│   ├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── utils/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── assets/
│   ├── App.jsx
│   └── package.json
│
├── database/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── README.md
│
├── docs/
│   ├── Architecture.png
│   ├── ER_Diagram.png
│   └── UI_Wireframes.png
│
└── README.md
```

---

## 🚀 Development Roadmap

### Week 1

- [x] Repository Setup
- [x] Project Structure
- [x] Architecture Diagram
- [x] ER Diagram
- [ ] PostgreSQL Schema
- [ ] UI Wireframes

### Week 2

- [ ] FastAPI Setup
- [ ] React Setup
- [ ] Authentication
- [ ] Product CRUD

### Week 3

- [ ] Inventory Management
- [ ] Competitor Pricing Module

### Week 4

- [ ] Machine Learning Model
- [ ] Price Prediction API

### Week 5

- [ ] Demand Forecasting

### Week 6

- [ ] Revenue Dashboard

### Week 7

- [ ] Testing

### Week 8

- [ ] Deployment
- [ ] Documentation

---

## 👨‍💻 Team

**Intern:** Disha Agrawal

---

## 📄 License

This project is developed for learning and internship purposes.

---

⭐ If you like this project, don't forget to give it a star!
