#!/bin/bash
# backup_ca_practice.sh

# Backup database
bench --site erp.test.site backup --with-files

# Sync to remote (example with AWS S3)
# aws s3 sync /home/frappe/frappe-bench/sites/ca-practice.local/private/backups s3://your-bucket/erpnext-backups/

# Clean old backups (keep last 7 days)
find /home/frappe/frappe15-bench/sites/erp.test.site/private/backups -type f -mtime +7 -delete

echo "Backup completed: $(date)"
