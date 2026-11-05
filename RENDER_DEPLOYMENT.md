# Deploying Driver Drowsiness System on Render with MySQL

This guide walks you through deploying the project to **[Render](https://render.com)** connected to a **MySQL** database.

---

## 1. Why MySQL on Render?

Render natively provides PostgreSQL and Redis, but does not offer an in-dashboard managed MySQL database. However, this application is configured to connect to any external cloud MySQL database seamlessly using standard connection URLs or credentials.

### Recommended Free Cloud MySQL Providers:

1. **[TiDB Cloud (Serverless)](https://tidbcloud.com)** *(Highly Recommended)*
   - 100% MySQL compatible.
   - **Free forever** tier (5 GB storage, no credit card required).
   - Instant setup: Create cluster &rarr; Click **Connect** &rarr; Copy the connection URL (`mysql://...`).
2. **[Aiven for MySQL](https://aiven.io)**: Free trial cloud MySQL with SSL.
3. **[Clever Cloud](https://www.clever-cloud.com)**: Free MySQL add-on.
4. **[Railway MySQL](https://railway.app)**: MySQL service with connection URL.

---

## 2. Git Commands: Push Changes to GitHub

Run these commands in your project terminal to push the updated configuration to GitHub:

```bash
git status
git add requirements.txt driver_drowsiness_system/settings.py driver_drowsiness_system/__init__.py Procfile build.sh render.yaml RENDER_DEPLOYMENT.md
git commit -m "Configure Render deployment with MySQL support and Daphne ASGI"
git push origin main
```

---

## 3. Step-by-Step Render Deployment

### Step A: Create the Web Service on Render

1. Log in to **[Render Dashboard](https://dashboard.render.com)**.
2. Click **New +** at the top right and select **Web Service**.
3. Choose **Build and deploy from a Git repository** and click **Next**.
4. Select your GitHub repository: `KorimiKiranKumar/driver_drowsiness_detection`.
   *(If not visible, click "Configure account" to grant Render access to your repo).*

### Step B: Configure Build & Runtime Settings

Fill in the settings:

| Setting | Value |
| :--- | :--- |
| **Name** | `driver-drowsiness-system` (or your choice) |
| **Region** | Choose the region closest to your users / database |
| **Branch** | `main` |
| **Root Directory** | *(leave blank)* |
| **Runtime** | **Python 3** |
| **Build Command** | `./build.sh` |
| **Start Command** | `daphne -b 0.0.0.0 -p $PORT driver_drowsiness_system.asgi:application` |
| **Instance Type** | **Free** |

> **Note:** If you prefer Docker deployment, you can alternatively select **Docker** as the Runtime. The included `Dockerfile` will build and run the app automatically.

### Step C: Add Environment Variables

Scroll down to **Environment Variables** and click **Add Environment Variable**:

| Key | Value | Description |
| :--- | :--- | :--- |
| `PYTHON_VERSION` | `3.11.9` | Ensures Python 3.11 compatibility |
| `DJANGO_DEBUG` | `False` | Production security |
| `DJANGO_SECRET_KEY` | *(Click "Generate" or paste a long random string)* | Django encryption key |
| `DATABASE_URL` | `mysql://<user>:<password>@<host>:<port>/<database>` | Your MySQL connection URL |

#### If your MySQL provider gave you separate credentials instead of a URL:
Instead of `DATABASE_URL`, you can add:
- `MYSQL_HOST`: `gateway01.us-east-1.prod.aws.tidbcloud.com`
- `MYSQL_PORT`: `4000` (or `3306`)
- `MYSQL_DATABASE`: `test` (your database name)
- `MYSQL_USER`: `xxxxxx.root`
- `MYSQL_PASSWORD`: `your_password`
- `MYSQL_SSL`: `true`

### Step D: Deploy

Click **Create Web Service**.
Render will:
1. Clone your repository.
2. Run `./build.sh` (installs packages, runs `collectstatic`, and applies MySQL migrations).
3. Start the application using Daphne on port `$PORT`.

---

## 4. Post-Deployment Steps

### 1. Verify Deployment Health
Once the status changes to **Live**, open your public URL:
```text
https://<your-service-name>.onrender.com/health/
```
You should see:
```json
{"status": "ok"}
```

### 2. Create an Admin User
1. In the Render Dashboard, open your Web Service.
2. In the left navigation, click **Shell**.
3. Run the following command:
   ```bash
   python manage.py createsuperuser
   ```
4. Enter your desired admin username, email, and password.

### 3. Test the Live Application
1. Open `https://<your-service-name>.onrender.com/accounts/login/`.
2. Sign in with your user credentials or register a new user.
3. Open the **Driver Monitoring** page.
4. Allow browser camera access when prompted.
5. Click **Start Monitoring** and verify that face landmarks, EAR, MAR, head pose, and drowsiness alerts respond in real time.

---

## 5. Troubleshooting Common Issues

- **Database Connection Error (SSL)**:
  Cloud providers like TiDB and Aiven require SSL encryption. The system automatically converts `?ssl-mode=REQUIRED` to Python SSLContext. If using individual variables, make sure `MYSQL_SSL=true` is set.
- **Allowed Hosts Error**:
  Render automatically sets `RENDER_EXTERNAL_HOSTNAME`, which is recognized and whitelisted in `settings.py`. If using a custom domain, add it to `DJANGO_ALLOWED_HOSTS`.
- **Camera Access Blocked**:
  Browsers only permit camera access over secure HTTPS connections (`https://...`). Render provides free SSL certificates automatically on `.onrender.com`.
