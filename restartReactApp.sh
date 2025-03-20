source ~/.bash_profile

homedirn=$(echo ~)
codedirn="$homedirn/EventServer/Codebase/PythonReact/reactapp/"
logdirn="${codedirn}runlog.txt"
countLines=($(wc -l "$logdirn"))
count=${countLines[0]}
if [ $count -lt "4" ]; then
	screen -m -d sh "${codedirn}runReact.sh"
fi
