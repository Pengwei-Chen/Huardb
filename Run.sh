directory=`pwd`
count=0
for shell in `find ./ -maxdepth 3 -name "SRR*.sh"`
do
count=`expr $count + 1`
cd $directory/${shell%/*}
echo "$directory/${shell#*/}"
bash ${shell##*/} 2>&1 | tee ${shell##*/}.o
done
cd $directory
echo "Count: "$count