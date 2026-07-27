# BinaryGuard Odoo ERP

Custom Odoo modules and deployment automation for the BinaryGuard ERP
production environment.

## Repository structure

- `.github/workflows/` — GitHub Actions deployment workflow
- `custom-addons/` — BinaryGuard custom Odoo modules
- `deployment/` — backup, deployment and module configuration scripts
- `requirements.txt` — extra Python dependencies

## Current custom modules

### binaryguard_core

Foundation module providing BinaryGuard ERP menus and shared client records.

## Production paths

- Repository: `/opt/binaryguard-odoo`
- Odoo source: `/opt/odoo/src`
- Custom addons: `/opt/odoo/custom-addons`
- Odoo configuration: `/etc/odoo.conf`
- Deployment command: `/usr/local/bin/deploy-odoo`
- Backup command: `/usr/local/bin/backup-odoo`

## Security

Never commit:

- `/etc/odoo.conf`
- database credentials
- Odoo master password
- SMTP passwords
- SSH private keys
- PostgreSQL database files
- Odoo filestore
- backups or deployment logs
