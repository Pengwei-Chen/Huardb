cat /dev/null > Results.txt
for shell in `find ./ -maxdepth 3 -name "SRR*.sh" | grep -`
do
echo ${shell}.o* &>> Results.txt
cat ${shell}.o* &>> Results.txt
echo "" &>> Results.txt
done
cat Results.txt | grep -c "Pipestance completed successfully\!"
a=`cat Results.txt | grep -c ".sh.o"`
b=`cat Results.txt | grep -c "No such file or directory"`
echo `expr $a - $b`