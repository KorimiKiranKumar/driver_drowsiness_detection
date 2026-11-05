# Deploying Driver Drowsiness System on Render with MySQL

This guide walks you through deploying the project to **[Render](https://render.com)** connected to a **MySQL** database.

---

## 1. Quick Solution for the `<port>` Error

If you encountered:
```text
ValueError: Port could not be cast to integer value as '<port>'
```
This happened because the template text (like `<port>` or `<PASSWORD>`) was pasted into Render without replacing it with your real port (`4000`) and real generated password.

We have added safety guards to the code so it will never crash with this error. Below are the exact credentials to enter.

---

## 2. Git Commands: Push the Fix to GitHub

Run these commands in PowerShell or terminal inside the project directory:

```bash
git add driver_drowsiness_system/settings.py RENDER_DEPLOYMENT.md
git commit -m "Fix database URL parsing and add fallback for placeholder templates"
git push origin main
```

---

## 3. How to Set Up Your TiDB Cloud MySQL Credentials

Based on your TiDB Cloud cluster:

1. In your **TiDB Cloud** popup:
   - Click the **[Generate Password]** button.
   - TiDB will generate a password (e.g., `abc123XYZ456!`). **Copy this password**.

2. In your **Render Dashboard** &rarr; open your Web Service &rarr; go to the **Environment** tab:

### Method A: Individual Variables (Recommended — Cleanest & Easiest)
Delete `DATABASE_URL` (if added) and add these exact key-value pairs:

| Key | Value |
| :--- | :--- |
| `MYSQL_HOST` | `gateway01.ap-northeast-1.prod.aws.tidbcloud.com` |
| `MYSQL_PORT` | `4000` |
| `MYSQL_USER` | `ZUj9YdM5YhQ3xug.root` |
| `MYSQL_PASSWORD` | *(Paste the password you generated in TiDB)* |
| `MYSQL_DATABASE` | `sys` |
| `MYSQL_SSL` | `true` |
| `PYTHON_VERSION` | `3.11.9` |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_SECRET_KEY` | *(Click Generate or enter a random string)* |

---

### Method B: Using `DATABASE_URL`
If you prefer setting a single `DATABASE_URL`, replace `<YOUR_PASSWORD>` with the password you generated in TiDB:

```text
mysql://ZUj9YdM5YhQ3xug.root:<YOUR_PASSWORD>@gateway01.ap-northeast-1.prod.aws.tidbcloud.com:4000/sys?ssl-mode=REQUIRED
```

*(Make sure port is `4000`, not `<port>`, and `<YOUR_PASSWORD>` contains your actual TiDB password).*

---

## 4. Trigger Deploy on Render

1. After saving the environment variables, click **Manual Deploy** &rarr; **Deploy latest commit** (or Render will automatically redeploy upon pushing to GitHub).
2. The build command `./build.sh` will run:
   - Python dependencies will be installed.
   - Static files will be collected.
   - MySQL migrations will run against your TiDB database.
3. Once the deployment turns green (**Live**), visit:
   `https://<your-service-name>.onrender.com/health/` &rarr; should show `{"status": "ok"}`.

---

## 5. Post-Deployment: Create Admin User

1. In your Render Dashboard, click the **Shell** tab on the left.
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Enter your desired username, email, and password.
4. Open `https://<your-service-name>.onrender.com/accounts/login/` and start using the system!
