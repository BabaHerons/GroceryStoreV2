![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Vue](https://img.shields.io/badge/Vue.js-3-4FC08D?logo=vue.js&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/status-stable-brightgreen)


# GroceryStoreV2 🛒

A full-stack grocery store management system built with a **Python backend** and a
**modern SPA frontend**, designed to simulate real-world e-commerce workflows
such as inventory management, cart handling, order processing, reporting, and authentication.

This project emphasizes **backend architecture, data flow, and business logic**
over simple CRUD operations.

---

## 📌 Overview

**GroceryStoreV2** is a multi-module grocery store platform that supports:

- User authentication and authorization
- Product and category management
- Cart and order lifecycle
- Sales summaries and reports
- Background tasks and caching
- Server-generated documents (invoices, reports, emails)
- SPA-based frontend dashboards

The project is structured to resemble a **production-ready service**, not a demo app.

---

## 🧠 Architecture Diagram

```mermaid
flowchart TD
    USER[User / Admin / Store Manager]

    UI[Vue SPA<br/>Vite + TypeScript]
    ROUTER[Vue Router<br/>Role-based Navigation]
    API_LAYER[API Abstraction<br/>api.ts]

    BACKEND[Python Backend]
    AUTH[JWT Auth Layer]
    ROUTES[Modular Routes<br/>auth, cart, order, product]
    CACHE[Custom Cache]
    TASKS[Background Tasks]
    DB[(SQLite Database)]
    TEMPLATES[HTML Templates<br/>Invoices & Emails]

    USER --> UI
    UI --> ROUTER
    ROUTER --> API_LAYER
    API_LAYER --> BACKEND

    BACKEND --> AUTH
    BACKEND --> ROUTES
    ROUTES --> CACHE
    ROUTES --> TASKS
    ROUTES --> DB
    TASKS --> TEMPLATES
```

## 🧠 High-Level Architecture

```text
Frontend (SPA)
 └─ Vue.js + Vite
     └─ Auth-aware routing
     └─ Role-based dashboards

Backend (API + Services)
 └─ Python (Flask-style architecture)
     ├─ REST APIs
     ├─ JWT Authentication
     ├─ Background Tasks
     ├─ Caching Layer
     ├─ Database (SQLite)
     ├─ HTML Templates
     └─ Reporting & Exports
```

## 🚀 Key Features

### Backend

* JWT-based authentication
* Role-based access (Admin / Store Manager / User)
* Product & category management
* Cart and order processing
* Background task execution
* Custom caching layer
* Sales analytics & summary endpoints
* CSV export support
* HTML email & invoice templates
* Database-backed persistence

### Frontend

* SPA built with Vue + TypeScript
* Route-based navigation
* Role-specific dashboards
* Authentication-aware UI
* Centralized API layer

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask-style architecture
* SQLite (development database)
* JWT for authentication
* Background tasks
* Custom caching
* HTML templates for emails & invoices

### Frontend

* Vue.js
* TypeScript
* Vite
* Vue Router
* Modular component architecture

---

## 📁 Project Structure

```text
GroceryStoreV2
├── backend
│   ├── main.py
│   ├── requirements.txt
│   ├── instance/
│   │   └── grocery_store_v2.db
│   └── src/
│       ├── routes/          # API routes (auth, cart, product, order, etc.)
│       ├── models.py        # Database models
│       ├── jwt.py           # Auth & token handling
│       ├── custom_cache.py  # Caching layer
│       ├── tasks.py         # Background jobs
│       ├── utils.py         # Shared utilities
│       ├── templates/       # Emails & invoices
│       ├── exports/         # CSV exports
│       └── sales_report/    # Generated reports
│
└── frontend
    ├── src/
    │   ├── components/      # UI components
    │   ├── pages/           # Application pages
    │   ├── router.ts        # Route configuration
    │   ├── api.ts           # API abstraction
    │   └── App.vue
    └── package.json
```

---

## 🔐 Authentication & Authorization

* JWT-based authentication
* Tokens validated on protected routes
* Role-aware dashboards:

  * Admin
  * Store Manager
  * User

This ensures **separation of responsibilities** and secure access control.

---

## 🧩 Backend Highlights

### 🔹 Modular Route Design

Each business domain (auth, product, cart, order, summary) has its own route module,
keeping logic isolated and maintainable.

---

### 🔹 Background Tasks

Long-running or periodic operations (such as reports or reminders) are handled
outside request-response cycles.

---

### 🔹 Custom Caching Layer

Caching is introduced to reduce redundant computation and improve response times.

---

### 🔹 Reporting & Templates

* HTML templates for invoices and emails
* Auto-generated sales and category reports
* CSV exports for external analysis

---

## ▶️ Running the Project

### Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend runs on:

```
http://localhost:5000
```

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

```
http://localhost:5173
```
