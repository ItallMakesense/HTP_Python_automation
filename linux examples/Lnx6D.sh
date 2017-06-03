"""
Schedules Apache to start every week day at 11AM and
stop the service at 9PM that day.
"""

crontab -l 2>/dev/null; echo "0 11 * * * ~/Lnx6.sh $1 11" | crontab -
crontab -l 2>/dev/null; echo "0 21 * * * ~/Lnx6.sh $1 21" | crontab -
