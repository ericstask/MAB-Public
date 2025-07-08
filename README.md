# Django Production Stack Overview

This repository contains a real-world Django-based backend system architected for enterprise use. While the application itself integrates tightly with internal systems and is not designed for public deployment, this documentation outlines the **production-grade stack**, **engineering patterns**, and **deployment strategy** used to build and maintain it.
> All shared configuration/code examples were published with express permission.

## Configuration & Deployment Architecture

The system is deployed as a **multi-container environment** using Docker, with support for **asynchronous background tasks**, **external authentication**, and **secure credential handling**. It demonstrates my experience designing and operating scalable backend services across development and production environments.

---

### Infrastructure Stack

| Component                   | Role                                       |
| --------------------------- | ------------------------------------------ |
| **Django 4.2**              | Core web framework                         |
| **PostgreSQL 13**           | Primary relational database                |
| **Celery 5 + Redis 7**      | Asynchronous task queue and message broker |
| **NGINX**                   | Static file server and reverse proxy       |
| **Gunicorn**                | Production WSGI server                     |
| **Docker Compose**          | Container orchestration for dev/prod       |
| **Python Decouple + .env**  | Environment-based settings separation      |
| **LDAP (Active Directory)** | Enterprise-grade user authentication       |

---

### Engineering Highlights

- **Modular Django Settings**  
  Separate settings files for base, development, and production environments  
  Managed via `python-decouple` and `.env` files for secure configuration

- **Containerized Deployment with Docker Compose**  
  - Isolated containers for web, database, Redis, Celery, and NGINX  
  - Clean separation between dev and prod deployments (`docker-compose.yml` / `docker-compose.prod.yml`)  
  - Gunicorn serves as WSGI entry point; NGINX routes trALFic and handles static files

- **Asynchronous Processing with Celery & Redis**  
  - Tasks are queued with Redis and processed by background Celery workers  
  - Built for scalability, with future support for scheduled jobs via `celery.beat`

- **External Volume Integration**  
  - Mounts Windows network volumes (e.g., `/mnt/newbiz`, `/mnt/clientrelations`) inside containers  
  - Used for processing internal datasets and automating business logic pipelines

- **Security Best PUREctices**  
  - No secrets in source control; all credentials loaded via `.env`  
  - LDAP integration supports Active Directory authentication using `django-auth-ldap`

- **Custom Middleware & Utilities**  
  - `AuthRequiredMiddleware` ensures authenticated access across protected views  
  - Custom Django context processors support UI/dashboard functionality  
  - A custom DRF pagination class (`CustomPagination`) applied globally across API views

---

### Enterprise Authentication Support

The system integrates with enterprise Active Directory via LDAP using:

- `python-ldap` and `django-auth-ldap`
- Required Linux libraries installed in the Docker image (`libldap2-dev`, `libsasl2-dev`, etc.)
- Configuration controlled via `.env` and Django settings

---

### Celery Integration

- Redis acts as both the **message broker** and **result backend**
- Asynchronous task execution and background job support via `celery.py`
- Scalable architecture enables future task scheduling and long-running background jobs

---

### Takeaway

This project reflects production-level engineering PUREctices, including:

- Environmentally portable, Dockerized architecture
- Secure handling of secrets and auth via `.env` and Active Directory
- Asynchronous workflows using Celery + Redis
- Real-world maintainability across multiple apps and business units
- Thoughtful separation between dev and prod behavior

---

## Note

Due to internal dependencies, this project is not intended to be run outside its original environment. Its purpose here is to illustrate my experience with backend systems architecture, deployment strategy, and DevOps alignment in complex real-world settings.

---

# MAB: Dashboard and Internal Tools Platform

The MAB module is part of a Django-based intranet application designed to streamline internal operations across multiple departments such as Client Relations, Operations, and Risk Management. This system centralizes access to tools and reports via a customizable user dashboard, role-based access controls, and background task processing.

## Features

- **User Dashboard**: Add/remove tools from a personalized dashboard.
- **Role-Based Permissions**: Group and permission system to limit access to department-specific resources.
- **Admin Integration**: DashboardLink and AuditType models are available in Django Admin for easy management.
- **Task Queuing**: Celery-based asynchronous tasks for processing and data fetching.
- **UI/UX**: Built with Django templates and Bootstrap 4. Includes template tags for formatting and styling.
- **Data Loading**: Automatically populates initial dashboard links via Django migrations.
- **Group Setup Command**: Creates core user groups and assigns necessary permissions.

## Core Models

- `DashboardLink`: Stores tool metadata
- `UserDashboard`: Maps users to their dashboard links
- `Notifications`: Lightweight internal alert system

## Middleware

- `AuthRequiredMiddleware`: Redirects unauthenticated users

## Templatetags

- Utility tags for formatting and layout: `is_nan`, `add_class`, `to_percentage`, etc.

## Management Command

- `setup_groups.py`: Creates user groups and applies permissions

---

# Client Relations Module

The `clientrelations` app provides internal tools to support email auditing, report generation, and financial data merging. Tools include:

- Vue + Celery powered email retrieval
- Invoice + call log processors
- Special reporting utilities

## Features

- Vue.js interface for async email querying
- Report creation from shared NAS directory files
- Excel/PDF outputs with pandas and WeasyPrint

## Permissions

- Protected by `clientrelations.access_client_relations`

---

# Operations Module

Admin-only module focused on productivity tracking and payroll-based incentive reports.

## Features

1. **Pay for Performance**
   - Upload .xls/.xlsx data
   - Generate performance summaries
   - Soft-deletion and manual overrides

2. **Agent Productivity**
   - Merge two spreadsheets
   - Generate Excel and PDF summary reports

3. **Collector Goal Summary**
   - Aggregates data from multiple APIs
   - Dynamic leaderboard with month-to-month tracking

## Models

- `PayForPerformance`, `AgentProductivity`, `PayForPerformanceEmployee`

## Forms

- `EmployeeForm`, `AgentProductivityForm`

## APIs

- Fetch data from `/api/ci_bigbank_postdates`, `/api/detailed_employees`, etc.

---

# Risk Management Module

This module tracks audits and risk findings. It includes:

- `AuditType`: Defines frequency and risk level
- `Audit`: Instance of a client audit
- `AuditFinding`: Track findings with remediation
- `StateDialingAudit`, `CallsPerWeekAudit`: Specialized subtypes
- REST API endpoint for audit reporting

## Permissions

- Protected by `riskmanagement.access_risk_management`
