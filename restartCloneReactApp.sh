source ~/.bash_profile

homedirn=$(echo ~)
codedirn="$homedirn/EventServer/Replica/PythonReactClone/reactapp/"
logdirn="${codedirn}runlog.txt"
countLines=($(wc -l "$logdirn"))
count=${countLines[0]}
if [ $count -lt "4" ]; then
	screen -m -d sh "${codedirn}runCloneReact.sh"
fi
