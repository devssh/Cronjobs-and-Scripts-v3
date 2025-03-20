hour=$(date '+%H')
minute=$(date '+%M')

if [ "$hour" -eq "23" ] && [ "$minute" -eq "58" ]; then
	echo "yes"
fi
