# Deploy on Railway with MySQL

This folder is configured for a Railway deployment using a Docker container and
Railway MySQL. Do not upload `db.sqlite3`; the deployment creates its schema in
MySQL automatically.

## Before you begin

1. Create accounts on [GitHub](https://github.com) and [Railway](https://railway.app).
2. Create a new GitHub repository and upload this entire project folder. Keep
   `Dockerfile`, `railway.toml`, `requirements.txt`, and `runtime.txt` in the
   top level of the repository.
3. Do not commit `.env`, passwords, or the local SQLite database.

## Create the Railway project

1. In Railway, select **New Project**.
2. Click **Deploy from GitHub repo**, authorize GitHub if requested, and select
   the repository you just uploaded.
3. Wait for the first application service to appear. It may fail now because
   the database has not been added yet; that is expected.
4. In the same Railway project, click **New** → **Database** → **MySQL**.
5. Keep the application and MySQL services in the **same Railway region**.
   They communicate privately, which avoids extra network delay.

## Connect Django to MySQL

1. Open the **application service**, then open **Variables**.
2. Add the following variables exactly. Replace `YOUR_PUBLIC_DOMAIN` only after
   you generate a Railway domain in the next section.

   ```text
   DJANGO_SECRET_KEY=use-a-long-random-secret-value-here
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=YOUR_PUBLIC_DOMAIN,healthcheck.railway.app
   DJANGO_CSRF_TRUSTED_ORIGINS=https://YOUR_PUBLIC_DOMAIN
   DATABASE_URL=${{MySQL.MYSQL_URL}}
   ```

   For `DATABASE_URL`, use Railway's variable-reference picker and select the
   MySQL service's `MYSQL_URL`. If your database service has a different name,
   Railway will insert the correct reference for you.
3. Save the variables. The included settings recognize a `mysql://...` URL,
   use PyMySQL, and set MySQL character encoding to `utf8mb4`.

## Make the site public and finish configuration

1. Open the application service → **Settings** → **Networking**.
2. Click **Generate Domain** and copy the generated hostname only, for example
   `driver-monitor-production.up.railway.app`.
3. Return to **Variables** and replace `YOUR_PUBLIC_DOMAIN` in both Django
   variables with that hostname. Do not include `https://` in
   `DJANGO_ALLOWED_HOSTS`; do include it in `DJANGO_CSRF_TRUSTED_ORIGINS`.
4. Trigger a redeploy. The container installs dependencies, collects static
   files, runs `migrate`, and starts Daphne automatically.
5. Wait until the deployment status is **Success**, then open
   `https://YOUR_PUBLIC_DOMAIN/health/`. It must show `{"status": "ok"}`.
6. Open `https://YOUR_PUBLIC_DOMAIN/accounts/login/`, sign in, open the monitor,
   allow browser camera access, and verify start/stop and the report screen.

## Migrating existing local data (optional)

If you need the users and reports from `db.sqlite3`, run this locally before
deployment:

```powershell
python manage.py dumpdata --exclude contenttypes --exclude auth.Permission --indent 2 | Out-File -Encoding utf8 data.json
```

After MySQL is deployed and the service is linked, run:

```powershell
railway run python manage.py loaddata data.json
```

This is optional. New deployments can simply start with empty MySQL tables.

## Important performance setting

Keep the application at **one replica**. The detector holds short-lived camera
state in local memory so it can avoid database writes for every frame. If you
later scale to multiple replicas, configure a shared Redis cache first.
