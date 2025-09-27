````markdown
# 🛠️ MyShop: A Custom E-commerce Platform

MyShop is a full-featured, responsive e-commerce application built with **Python Flask** for the backend, **Tailwind CSS** for a modern frontend, and **PostgreSQL** for the database. It includes a custom order system, secure payments via **Stripe**, and a complete admin interface.

## 🌟 Features

* **Product Management:** Catalog, product details, inventory, and categories.
* **E-commerce Workflow:** Session-based Shopping Cart, Secure Checkout.
* **Payments:** Integrated with **Stripe Checkout API** for secure transactions.
* **User Accounts:** Registration, Login (Flask-Login), Order History, Profile.
* **Admin Dashboard:** Protected interface to manage Products, Orders, and Custom Requests.
* **Custom Orders:** Form for customers to upload designs and notes.
* **Deployment:** Production-ready setup using **Docker**, **Gunicorn**, and **Nginx**.
* **Styling:** Fully **responsive** UI using **Tailwind CSS**.

---

## ⚙️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Python, Flask, SQLAlchemy ORM | The core application logic and ORM. |
| **Frontend** | HTML, Tailwind CSS | Modern, utility-first CSS framework. |
| **Database** | PostgreSQL (Production), SQLite (Local) | Robust relational database. |
| **Authentication** | Flask-Login, Werkzeug | Secure user sessions and password hashing. |
| **Payments** | Stripe Checkout API | PCI-compliant payment processing. |
| **Email** | Flask-Mail (SendGrid/SMTP) | For transactional emails (e.g., order confirmations). |
| **Deployment** | Docker, Gunicorn, Nginx | Containerized, scalable production environment. |

---

## 🚀 Local Setup Instructions

### 1. Prerequisites

Ensure you have the following installed:

* **Python 3.8+**
* **pip** (Package installer for Python)
* **Node.js & npm** (For Tailwind CSS build)
* **PostgreSQL** (Optional, SQLite is the default for a quick start)

### 2. Environment Variables

Create a file named `.env` in the root directory (`myshop/`) by copying the example:

```bash
cp .env.example .env
````

Edit the new `.env` file with your specific configurations:

| Variable | Description | Notes |
| :--- | :--- | :--- |
| `SECRET_KEY` | Flask session secret key. | Use a long, random string. |
| `FLASK_ENV` | Environment mode. | Set to `development` for local run. |
| `DATABASE_URL` | SQLAlchemy database URI. | E.g., `sqlite:///app.db` or PostgreSQL URI. |
| `STRIPE_PUBLIC_KEY` | Your Stripe publishable key. | Starts with `pk_test_...` |
| `STRIPE_SECRET_KEY` | Your Stripe secret key. | Starts with `sk_test_...` |
| `MAIL_SERVER`, `MAIL_PORT`, etc. | SMTP server details for email. | Required for order notifications. |

### 3\. Backend Setup (Python)

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Initialize and Run Migrations:**

    ```bash
    flask db upgrade
    ```

    *(This creates the database tables based on `app/models.py`)*

3.  **Seed Initial Data (Optional):**
    You can run a custom script or shell to add initial categories and products.

    ```python
    # Example: from flask shell
    # from app.models import Category, Product, db
    # ... create and add to session, then db.session.commit()
    ```

### 4\. Frontend Setup (Tailwind CSS)

1.  **Install Node dependencies:**
    ```bash
    npm install
    ```
2.  **Build Tailwind CSS:**
    Run this command in a separate terminal during development. It watches for changes in your templates and rebuilds the CSS.
    ```bash
    npm run watch
    ```
    *This generates the final, minimized CSS file at `app/static/css/tailwind.css`.*

### 5\. Running the Application

With the database and Tailwind built, start the Flask development server:

```bash
export FLASK_APP=run.py
flask run
```

The site should now be accessible at `http://127.0.0.1:5000/`.

-----

## 🐳 Docker Deployment

The project is configured for production deployment using **Docker** for containerization, **Gunicorn** as the application server, and **Nginx** as a reverse proxy/static file server.

### 1\. Prerequisites

  * **Docker**
  * **Docker Compose**

### 2\. Environment Variables

Ensure your `.env` file is configured with production-ready values (e.g., **PostgreSQL** `DATABASE_URL`, real **Stripe** keys, production-grade `SECRET_KEY`).

### 3\. Build and Run

From the root directory, execute the following command:

```bash
docker-compose up --build -d
```

  * The `--build` flag ensures your application and Tailwind CSS are built into the image.
  * The `-d` flag runs the containers in detached mode.

The application will be running on `http://localhost:80/`.

> **Note:** Initial database migrations *must* be applied manually after the database container is up or via an entrypoint script in a production setup.

-----

## 💳 Stripe Setup

To enable payment processing, you need to configure Webhooks and ensure your keys are correct.

### 1\. Keys

Set the following in your `.env` file:

  * `STRIPE_PUBLIC_KEY`
  * `STRIPE_SECRET_KEY`

### 2\. Webhooks

The checkout process relies on the **Stripe Webhook** handler (`/checkout/webhook`) to confirm successful payments and create the final order.

1.  Use the **Stripe CLI** for local testing:
    ```bash
    stripe listen --forward-to localhost:5000/checkout/webhook
    ```
2.  In a production environment, expose your webhook URL to Stripe and configure it to listen for the following events:
      * `checkout.session.completed`

Set the Stripe webhook secret in your `.env` file as `STRIPE_WEBHOOK_SECRET`.

```markdown
# ... rest of the file
```

-----

## 📁 Key File Structure

The project uses Flask **Blueprints** to organize the routes into logical sections.

```
myshop/
├─ app/
│  ├─ __init__.py       # Application factory and configuration
│  ├─ models.py         # SQLAlchemy ORM definitions
│  ├─ forms.py          # WTForms for user input and validation
│  ├─ routes/           # Blueprints for application routes
│  │   ├─ auth.py       # Registration, login, logout
│  │   ├─ products.py   # Catalog and product details
│  │   ├─ cart.py       # Shopping cart management
│  │   ├─ checkout.py   # Stripe payments and webhooks
│  │   ├─ admin.py      # Protected admin dashboard
│  │   └─ custom.py     # Custom order form
│  ├─ templates/        # HTML templates (Jinja2)
│  └─ static/           # Static assets (images, compiled CSS)
├─ migrations/          # Alembic migration scripts
├─ Dockerfile           # Docker image definition
├─ docker-compose.yml   # Multi-container setup (app, db, nginx)
├─ requirements.txt     # Python dependencies
└─ run.py               # Entry point to run the application
```

```
# End of README.md
```