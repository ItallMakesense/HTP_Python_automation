crontab -l 2>/dev/null; echo "0 11 * * * ~/start-stop_apache.sh $1 11" | crontab -
crontab -l 2>/dev/null; echo "0 21 * * * ~/start-stop_apache.sh $1 21" | crontab -
