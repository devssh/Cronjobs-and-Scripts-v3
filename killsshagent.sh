sleep 10

processids=$(ps aux | grep "\?\?  Ss .* 0:00.00 ssh-agent" | awk '{print $2}' | xargs)
for procids in $processids
do
kill $procids
done

