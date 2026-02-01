# Flight Service - Quick Reference

## Quick Commands

### Local Development
```bash
# Start all services
docker-compose up --build

# Start only flight-service
docker-compose up flight-service

# Stop all services
docker-compose down

# View logs
docker-compose logs -f flight-service

# Rebuild flight-service
docker-compose up --build flight-service
```

### Production Testing (Local)
```bash
# Build production image
docker build -f flight-service/Dockerfile.prod -t flight-service:prod ./flight-service

# Run production image locally
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e FLIGHT_SERVICE_PORT=5000 \
  -e DB2_URL=postgresql://user:pass@host:5432/db \
  -e REDIS_URL=redis://host:6379/0 \
  flight-service:prod

# Test the service
curl http://localhost:5000/health
```

### GitHub Actions
```bash
# View workflows
# Go to: https://github.com/YOUR-USERNAME/YOUR-REPO/actions

# Manually trigger workflow (if enabled)
# Go to Actions → Select workflow → Run workflow

# Check workflow status
git push origin main
# Then check GitHub Actions tab
```

### Docker Commands
```bash
# List running containers
docker ps

# Stop container
docker stop flight-service

# Remove container
docker rm flight-service

# List images
docker images

# Remove image
docker rmi flight-service:prod

# View container logs
docker logs flight-service -f

# Execute command in container
docker exec -it flight-service bash
```

## Environment Variables

### Development (.env)
```bash
FLASK_ENV=development
FLIGHT_SERVICE_HOST=0.0.0.0
FLIGHT_SERVICE_PORT=5555
DB2_URL=postgresql://postgres:postgres@flights_db:5432/flights_db
REDIS_URL=redis://redis_db:6379/0
```

### Production (Render)
```bash
FLASK_ENV=production
FLIGHT_SERVICE_HOST=0.0.0.0
FLIGHT_SERVICE_PORT=5000
DB2_URL=postgresql://user:pass@production-host/db
REDIS_URL=redis://production-redis:6379/0
```

## GitHub Secrets Required

Add these in: Repository Settings → Secrets and variables → Actions

```
RENDER_DEPLOY_HOOK_FLIGHT_SERVICE
```

## Render Configuration

### Image URL Format
```
ghcr.io/YOUR-GITHUB-USERNAME/YOUR-REPO-NAME/flight-service:latest
```

### Authentication
- **Username**: Your GitHub username
- **Password**: GitHub Personal Access Token (with `read:packages` scope)

## Deployment Flow

1. **Make changes** to code
2. **Test locally** with docker-compose
3. **Commit & Push** to main branch
   ```bash
   git add .
   git commit -m "Update flight-service"
   git push origin main
   ```
4. **GitHub Actions** automatically:
   - Builds Docker image
   - Pushes to GHCR
   - Triggers Render deploy
5. **Render** automatically:
   - Pulls new image
   - Restarts service
   - Application is live!

## Monitoring

### GitHub Actions
- URL: `https://github.com/YOUR-USERNAME/YOUR-REPO/actions`
- Check build status and logs

### Render Dashboard
- URL: `https://dashboard.render.com/`
- View service status, logs, and metrics

### Health Check
```bash
# Local
curl http://localhost:5555/health

# Production
curl https://your-service.onrender.com/health
```

## Troubleshooting

### Build fails on GitHub Actions
1. Check GitHub Actions logs
2. Verify Dockerfile.prod syntax
3. Test build locally

### Render deployment fails
1. Check Render logs
2. Verify environment variables
3. Check database connectivity
4. Verify image URL and credentials

### Application crashes
1. Check Render logs
2. Verify all environment variables are set
3. Test production image locally
4. Check database migrations

### SocketIO not working
- Ensure gevent worker is used
- Check CORS settings
- Verify WebSocket support on hosting platform

## Port Configuration

| Environment | Port | Access |
|------------|------|--------|
| Development | 5555 | http://localhost:5555 |
| Production (Docker) | 5000 | Internal only |
| Production (Render) | 443 | https://your-service.onrender.com |

## File Reference

| File | Purpose |
|------|---------|
| `Dockerfile.dev` | Development environment |
| `Dockerfile.prod` | Production multi-stage build |
| `docker-compose.yml` | Local orchestration |
| `requirements.txt` | Python dependencies |
| `run.py` | Development entry point |
| `wsgi.py` | Production entry point |
| `gunicorn_config.py` | Gunicorn configuration |
| `.dockerignore` | Exclude files from Docker build |
| `.github/workflows/flight-service-ci-cd.yml` | CI/CD pipeline |

## Performance Tuning

### Gunicorn Workers
Edit `gunicorn_config.py`:
```python
# For more concurrent connections
workers = 2
worker_connections = 2000

# For lower memory usage
workers = 1
worker_connections = 1000
```

### Environment Variables
```bash
# Set workers via environment variable
GUNICORN_WORKERS=2

# Set log level
LOG_LEVEL=warning  # Options: debug, info, warning, error
```

## Security Checklist

- ✅ Run as non-root user in Docker
- ✅ Use environment variables for secrets
- ✅ Use HTTPS in production (Render provides this)
- ✅ Keep dependencies updated
- ⬜ Enable firewall rules
- ⬜ Set up rate limiting
- ⬜ Enable CORS properly
- ⬜ Rotate secrets regularly

## Support Resources

- **GitHub Actions**: https://docs.github.com/en/actions
- **Docker**: https://docs.docker.com/
- **Gunicorn**: https://docs.gunicorn.org/
- **Gevent**: http://www.gevent.org/
- **Flask-SocketIO**: https://flask-socketio.readthedocs.io/
- **Render**: https://render.com/docs

---

For detailed setup instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)
