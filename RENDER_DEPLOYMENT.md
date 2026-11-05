# Deploying Driver Drowsiness System on Render with MySQL

This guide walks you through deploying the project to **[Render](https://render.com)** connected to a **MySQL** database (e.g. TiDB Cloud).

---

## 1. Why Did the Migration Fail with `CREATE command denied`?

In MySQL and TiDB, **`sys`** is a built-in internal system schema used solely for performance diagnostics. It does **not** allow creating application tables.

TiDB Cloud's standard application database is **`test`**.
We have updated the code so that if `sys` is passed, it automatically maps to **`test`**.

---

## 2. Push Changes to GitHub

Run these commands in PowerShell or terminal inside the project directory:

```bash
git add driver_drowsiness_system/settings.py RENDER_DEPLOYMENT.md
git commit -m "Auto-map MySQL system schema sys to test application database"
git push origin main
```

---

## 3. Update Environment Variables in Render

In your **Render Dashboard** &rarr; open your Web Service &rarr; **Environment** tab:

### Method A: Individual Variables (Recommended — Cleanest & Most Reliable)

Ensure these variables are set:

| Key | Value |
| :--- | :--- |
| `MYSQL_HOST` | `gateway01.ap-northeast-1.prod.aws.tidbcloud.com` |
| `MYSQL_PORT` | `4000` |
| `MYSQL_USER` | `ZUj9YdM5YhQ3xug.root` |
| `MYSQL_PASSWORD` | *(Your generated password from TiDB Cloud)* |
| `MYSQL_DATABASE` | `test` |
| `MYSQL_SSL` | `true` |
| `PYTHON_VERSION` | `3.11.9` |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_SECRET_KEY` | *(Generated random secret key)* |

*(Make sure `MYSQL_DATABASE` is set to `test`, not `sys`).*

---

### Method B: Single `DATABASE_URL`

If you are using `DATABASE_URL`, change the database path from `/sys` to `/test`:

```text
mysql://ZUj9YdM5YhQ3xug.root:<YOUR_GENERATED_PASSWORD>@gateway01.ap-northeast-1.prod.aws.tidbcloud.com:4000/test?ssl-mode=REQUIRED
```

---

## 4. Trigger Deploy on Render

1. Click **Manual Deploy** &rarr; **Deploy latest commit** (or Render will automatically redeploy after you push).
2. The build command will now run `python manage.py migrate --noinput` against the `test` database.
3. Once the deployment turns **Live**, visit:
   `https://<your-service-name>.onrender.com/health/` &rarr; should show `{"status": "ok"}`.

---

## 5. Post-Deployment: Create Admin User

1. In your Render Dashboard, click the **Shell** tab on the left.
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Enter your desired username, email, and password.
4. Open `https://<your-service-name>.onrender.com/accounts/login/` and start monitoring!
