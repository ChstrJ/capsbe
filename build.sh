#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# if [ -f "db.sqlite3" ]; then
#     rm db.sqlite3
#     echo "deleted"
# else
#     echo "pass"
# fi

# Apply any outstanding database migrations
# python manage.py makemigrations
python manage.py migrate

# Generate test account
# python manage.py account
# python manage.py generate

