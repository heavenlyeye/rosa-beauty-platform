#!/bin/bash

# Clone the repository (if not already cloned)
# git clone https://github.com/username/rosa-project.git
# cd rosa-project

# Create root files
touch .env .DS_Store requirements.txt rosa.db README.md .gitignore

# Create directory structure
mkdir -p \
  docker \
  app/{routers,ui,locales,auth,chatbot,utils,models,schemas,static/{css,images,js},services} \
  tests \
  docs \
  alembic/versions

# Create __init__.py files
find app -type d -exec touch {}/__init__.py \;
touch tests/__init__.py

# Create specific files in app/routers
touch app/routers/{auth.py,services.py,bookings.py,admin.py,reports.py,salons.py}

# Create auth related files
touch app/auth/{jwt_handler.py,permissions.py}

# Create utils files
touch app/utils/{validators.py,helpers.py}

# Create model files
touch app/models/{service.py,user.py,booking.py,salon.py,stylist.py}

# Create schema files
touch app/schemas/{service.py,user.py,booking.py,salon.py}

# Create static files
touch app/static/{index.html,admin.html,dashboard.html,dashboard.html.backup}
touch app/static/css/dashboard.css
touch app/static/js/dashboard.js

# Create service files
touch app/services/{ai_service.py,auth_service.py,service_service.py,reports_service.py,booking_service.py,salon_service.py}

# Create other app files
touch app/{config.py,database.py,main.py}

# Create .DS_Store files in specified directories
touch app/.DS_Store app/ui/.DS_Store app/static/.DS_Store app/services/.DS_Store alembic/.DS_Store

# Create __pycache__ directories (but these should be in .gitignore)
mkdir -p app/__pycache__ app/routers/__pycache__ app/auth/__pycache__ app/models/__pycache__ app/schemas/__pycache__ app/services/__pycache__

# Add content to .gitignore
cat > .gitignore <<EOL
# Python
__pycache__/
*.pyc

# macOS
.DS_Store

# Environment
.env

# Database
*.db
*.sqlite

# IDE
.vscode/
.idea/
EOL

# Initialize git (if not already initialized)
# git init

# Add all files
git add .

# Commit changes
git commit -m "Create complete project structure"

# Push to remote (uncomment when ready)
# git push origin main

echo "Project structure created successfully!"