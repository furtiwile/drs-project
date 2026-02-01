# Flight Service - Production Deployment Guide

## Overview

This guide covers the complete setup for local development and production deployment of the flight-service using Docker, GitHub Actions, and Render.

## Architecture

### Local Development
- **Dockerfile.dev**: Development environment with hot-reload
- **docker-compose.yml**: Orchestrates all services locally
- Uses Flask's built-in Werkzeug server

### Production
- **Dockerfile.prod**: Multi-stage production build
- **Gunicorn + Gevent**: Production-grade WSGI server with async support
- **GitHub Actions**: Automated CI/CD pipeline
- **GitHub Container Registry (GHCR)**: Docker image storage
- **Render**: Cloud deployment platform

## Prerequisites

1. **GitHub Account** with access to GitHub Container Registry
2. **Render Account** (free tier available)
3. **Production Database** (PostgreSQL)
   - Recommended: [Neon](https://neon.tech/), [Supabase](https://supabase.com/), or Render PostgreSQL
4. **Production Redis** (optional, if using cache/sessions)
   - Recommended: [Render Key-Value Store](https://render.com/docs/redis), [Upstash](https://upstash.com/)

## Local Development Setup

### 1. Start all services locally
```bash
docker-compose up --build
```

The flight-service will be available at `http://localhost:5555` (or your configured port).

### 2. Development with live reload
The `Dockerfile.dev` configuration runs Flask with Werkzeug, which includes auto-reload on code changes.

## Production Setup

### Step 1: Configure GitHub Secrets

Navigate to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

1. **RENDER_DEPLOY_HOOK_FLIGHT_SERVICE**
   - This will be created in Step 3 after setting up Render

### Step 2: Prepare Production Database

1. Create a production PostgreSQL database on your chosen platform
2. Save the connection string (format: `postgresql://user:password@host:port/database`)
3. Run your database migrations/initialization scripts

### Step 3: Configure Render Web Service

#### Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **Web Service**
3. Select **Deploy an existing image from a registry**
4. Configure the service:

   **Image URL:**
   ```
   ghcr.io/YOUR-GITHUB-USERNAME/YOUR-REPO-NAME/flight-service:latest
   ```
   
   **Example:**
   ```
   ghcr.io/johndoe/drs-project/flight-service:latest
   ```

5. **Authentication**:
   - Select "Private Registry"
   - Username: Your GitHub username
   - Password: Create a GitHub Personal Access Token (PAT)
     - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
     - Generate new token with `read:packages` scope
     - Copy and paste the token as password

6. **Service Configuration**:
   - **Name**: `flight-service`
   - **Region**: Choose closest to your users
   - **Instance Type**: Free or paid (depending on needs)

#### Configure Environment Variables

In Render Web Service settings, add these environment variables:

```bash
# Flask Configuration
FLASK_ENV=production
FLIGHT_SERVICE_HOST=0.0.0.0
FLIGHT_SERVICE_PORT=5000

# Database (Production PostgreSQL)
DB2_URL=postgresql://user:password@host:port/database

# Redis (Production Redis - if using)
REDIS_URL=redis://user:password@host:port

# Other required environment variables from your .env
# Add all variables needed at runtime here
```

**Important**: 
- These are RUNTIME environment variables
- They are NOT used during the Docker build
- Add all variables your application needs when running

#### Generate Deploy Hook

1. In Render Web Service settings, find **Deploy Hook**
2. Copy the Deploy Hook URL (looks like: `https://api.render.com/deploy/srv-xxxxx?key=xxxxx`)
3. Add this to GitHub Secrets as `RENDER_DEPLOY_HOOK_FLIGHT_SERVICE`

### Step 4: Push to GitHub

When you push changes to the `main` branch that affect `flight-service/`:

```bash
git add .
git commit -m "Update flight-service"
git push origin main
```

**Automatic Process:**
1. ✅ GitHub Actions detects changes in `flight-service/`
2. 🏗️ Builds production Docker image using `Dockerfile.prod`
3. 📦 Pushes image to GitHub Container Registry
4. 🔔 Triggers Render Deploy Hook
5. 🚀 Render pulls new image and redeploys service
6. ✨ Production is live with new changes!

## Architecture Details

### Gunicorn Configuration

The production setup uses Gunicorn with gevent workers for optimal performance:

```bash
gunicorn --worker-class gevent --workers 1 --bind 0.0.0.0:5000 --timeout 120 wsgi:app
```

**Why Gevent?**
- ✅ Async support for WebSocket connections (Flask-SocketIO)
- ✅ Handles multiple concurrent connections efficiently
- ✅ Better performance than sync workers for I/O-bound operations

**Configuration:**
- `--worker-class gevent`: Use gevent async workers
- `--workers 1`: Single worker (gevent handles concurrency internally)
- `--timeout 120`: 2-minute timeout for long-running requests
- `wsgi:app`: Entry point to the application

### Multi-Stage Docker Build

**Stage 1 - Builder:**
- Installs build dependencies (gcc, postgresql-client)
- Installs all Python packages
- Creates optimized Python environment

**Stage 2 - Production:**
- Minimal base image (only runtime dependencies)
- Copies only necessary files from builder
- Runs as non-root user for security
- Smaller final image size

### File Structure

```
flight-service/
├── Dockerfile.dev          # Local development
├── Dockerfile.prod         # Production (multi-stage)
├── .dockerignore          # Files to exclude from Docker build
├── requirements.txt       # Python dependencies (includes gunicorn, gevent)
├── run.py                # Development entry point
├── wsgi.py               # Production entry point (Gunicorn)
├── config.py             # Configuration
└── app/                  # Application code
```

## Monitoring and Debugging

### Check GitHub Actions

1. Go to your repository on GitHub
2. Click **Actions** tab
3. View workflow runs and logs

### Check Render Deployment

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click on your `flight-service`
3. View **Logs** tab for runtime logs
4. View **Events** tab for deployment history

### Common Issues

#### Build Fails on GitHub Actions
- Check workflow logs in GitHub Actions
- Verify `Dockerfile.prod` syntax
- Ensure all required files exist

#### Render Deployment Fails
- Verify image URL is correct in Render
- Check GitHub PAT has `read:packages` permission
- Verify environment variables are set correctly

#### Application Crashes on Render
- Check Render logs
- Verify all environment variables are set
- Ensure database connection string is correct
- Check that database is accessible from Render

## Scaling Considerations

### Gunicorn Workers
For higher traffic, adjust worker count in `Dockerfile.prod`:

```dockerfile
# For CPU-bound tasks:
CMD ["gunicorn", "--workers", "4", "--worker-class", "gevent", ...]

# For I/O-bound tasks (current setup):
CMD ["gunicorn", "--workers", "1", "--worker-class", "gevent", ...]
```

**Rule of thumb:** `workers = (2 × CPU cores) + 1`

### Render Instance Type
- **Free**: Limited resources, good for testing
- **Starter**: More resources, better for production
- **Standard+**: For high-traffic applications

## Environment Variables Guide

### Build-time vs Runtime

**Build-time** (GitHub Secrets → used during `docker build`):
- Variables needed to build the application
- For frontend: API URLs, feature flags
- Passed as `--build-arg` in Dockerfile

**Runtime** (Render Environment Variables):
- Variables needed when application runs
- Database URLs, API keys, secrets
- Set in Render dashboard

### Flight Service Environment Variables

**Required Runtime Variables:**
```bash
FLASK_ENV=production
FLIGHT_SERVICE_HOST=0.0.0.0
FLIGHT_SERVICE_PORT=5000
DB2_URL=postgresql://...
REDIS_URL=redis://...
```

**Optional Variables** (add as needed):
```bash
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
# ... etc
```

## Testing Production Build Locally

Test the production Docker image locally before deploying:

```bash
# Build production image
docker build -f flight-service/Dockerfile.prod -t flight-service:prod ./flight-service

# Run production image
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e DB2_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  flight-service:prod
```

## Rollback Strategy

If a deployment fails:

1. **Via Render Dashboard:**
   - Go to your service → **Manual Deploy**
   - Select a previous successful deployment

2. **Via GitHub:**
   - Revert the commit: `git revert HEAD`
   - Push to trigger new deployment

3. **Via Docker Tag:**
   - Update Render to use a specific image tag instead of `latest`

## Security Best Practices

✅ **Implemented:**
- Non-root user in Docker container
- Environment variables for secrets (not hardcoded)
- Multi-stage build (minimal attack surface)
- GitHub Container Registry (private by default)

🔒 **Recommended:**
- Enable Render's DDoS protection
- Use HTTPS only (Render provides free SSL)
- Rotate secrets regularly
- Enable GitHub branch protection
- Use GitHub environment protection rules

## Cost Considerations

### Free Tier Limits

**GitHub:**
- ✅ GitHub Actions: 2,000 minutes/month (free tier)
- ✅ GHCR: 500MB storage (free tier)

**Render:**
- ✅ Web Service: Free tier available (sleeps after inactivity)
- ✅ PostgreSQL: Free tier available (limited storage)
- ✅ Redis: Free tier available

### Recommendations
- Start with free tiers for testing
- Upgrade to paid plans for production traffic
- Monitor usage to avoid unexpected charges

## Next Steps

1. ✅ Set up production database
2. ✅ Configure GitHub Secrets
3. ✅ Create Render Web Service
4. ✅ Test deployment pipeline
5. ✅ Monitor application in production
6. 🔄 Set up logging and monitoring
7. 🔄 Configure custom domain (optional)
8. 🔄 Set up CI/CD for other services (frontend, server)

## Support

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Render Docs**: https://render.com/docs
- **Gunicorn Docs**: https://docs.gunicorn.org/
- **Flask-SocketIO**: https://flask-socketio.readthedocs.io/

---

**Happy Deploying! 🚀**
