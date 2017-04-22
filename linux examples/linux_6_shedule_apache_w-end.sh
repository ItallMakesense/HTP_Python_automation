crontab -l 2>/dev/null; echo "0 12 * * 6 ~/start-stop_apache.sh $1 12" | crontab -
crontab -l 2>/dev/null; echo "0 23 * * 6 ~/start-stop_apache.sh $1 23" | crontab -
