directory=`pwd`
count=0
for shell in `find ./ -maxdepth 3 -name "SRR*.sh"`
do
count=`expr $count + 1`
cd $directory/${shell%/*}
echo "$directory/${shell#*/}"
qsub ${shell##*/}
done
cd $directory
echo "Count: "$count