cat /dev/null > Results.txt
for shell in `find ./ -maxdepth 3 -name "SRR*.sh" | grep -`
do
echo ${shell}.o* &>> Results.txt
cat ${shell}.o* &>> Results.txt
echo ${shell}.e* &>> Results.txt
cat ${shell}.e* &>> Results.txt
echo "" &>> Results.txt
done
qstat | grep wanluliu | grep -c SRR
cat Results.txt | grep -c "Pipestance completed successfully\!"