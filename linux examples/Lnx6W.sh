"""
Schedules Apache to start every weekend at noon and
stop the service at 1 hour before midnight that day.
"""

crontab -l 2>/dev/null; echo "0 12 * * 6 ~/Lnx6.sh $1 12" | crontab -
crontab -l 2>/dev/null; echo "0 23 * * 6 ~/Lnx6.sh $1 23" | crontab -
