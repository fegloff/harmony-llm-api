# harmony-llm-api

## Deploy to fly.io
### Create instance
fly launch
fly scale vm performance-2x --group app

### development
fly deploy

### production
fly deploy deploy -c fly.production.toml

