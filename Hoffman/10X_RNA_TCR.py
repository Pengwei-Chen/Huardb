import os
import re

fasterq = False
delete_after_count = True
prefetch = "/u/home/w/wanluliu/tools/sratoolkit/sratoolkit.3.0.0-centos_linux64/bin/prefetch"
sra = "/u/home/w/wanluliu/wanluliu/ncbi/Naive_hESC/sra"
fastq_dump = "/u/home/w/wanluliu/tools/sratoolkit/sratoolkit.3.0.0-centos_linux64/bin/fastq-dump"
fasterq_dump = "/u/home/w/wanluliu/tools/sratoolkit/sratoolkit.3.0.0-centos_linux64/bin/fasterq-dump"
cellranger = "/u/home/w/wanluliu/biosoft/cellranger-6.1.2/bin/cellranger"
transcriptome_gex = "/u/home/w/wanluliu/wanluliu/refData/refdata-gex-GRCh38-2020-A"
reference_tcr = "/u/home/w/wanluliu/wanluliu/refData/refdata-cellranger-vdj-GRCh38-alts-ensembl-5.0.0"
def generate_command(srr, gex_or_vdj, transcriptome_or_reference):
    command = "#!/bin/sh\n#$ -cwd\n#$ -o ./\n#$ -V\n#$ -S /bin/bash\n#$ -l h_data=101G,h_rt=24:00:00\n#$ -e ./\n\n"
    if not fasterq:
        # Prefetch
        print("Prefetching", srr + "...")
        command += prefetch + " -X 100G " + srr + "\n"

        # Move
        print("Moving", srr + "...")
        command += "mv " + sra + "/" + srr + ".sra ./sra" + "\n"

        # Fastq-dump
        print("Dumping", srr + "...")
        command += fastq_dump + " --outdir fastq --gzip --split-files ./sra/" + srr + ".sra" + "\n"
        
        if delete_after_count:
            command += "rm sra/" + srr + ".sra" + "\n"
    else:
        command += "echo $(date +%F%n%T)' Fasterq dumping...'\n"
        command += fasterq_dump + " --outdir fastq --split-files -e 16 --include-technical " + srr + "\n"

    # Rename
    print("Renaming fastq files...")
    if not fasterq:
        suffix = ".fastq.gz"
    else:
        suffix = ".fastq"
    command += "cd fastq" + "\n"
    command += "if [ -f ./" + srr + "_3" + suffix + " ]\n"
    command += "then\n"
    command += "\tif [ `head -n 1 ./" + srr + "_1" + suffix + " | awk -F 'length=' '{print $2}'` -lt `head -n 1 ./" + srr + "_3" + suffix + " | awk -F 'length=' '{print $2}'` ];\n"
    command += "\tthen\n"
    command += "\t\tmv " + srr + "_1" + suffix + " " + srr + "_S1_L001_I1_001" + suffix + "\n"
    command += "\t\tmv " + srr + "_2" + suffix + " " + srr + "_S1_L001_R1_001" + suffix + "\n"
    command += "\t\tmv " + srr + "_3" + suffix + " " + srr + "_S1_L001_R2_001" + suffix + "\n"
    command += "\telse\n"
    command += "\t\tmv " + srr + "_3" + suffix + " " + srr + "_S1_L001_I1_001" + suffix + "\n"
    command += "\t\tmv " + srr + "_1" + suffix + " " + srr + "_S1_L001_R1_001" + suffix + "\n"
    command += "\t\tmv " + srr + "_2" + suffix + " " + srr + "_S1_L001_R2_001" + suffix + "\n"
    command += "\tfi\n"
    command += "else\n"
    command += "\tmv " + srr + "_1" + suffix + " " + srr + "_S1_L001_R1_001" + suffix + "\n"
    command += "\tmv " + srr + "_2" + suffix + " " + srr + "_S1_L001_R2_001" + suffix + "\n"
    command += "fi\n"
    command += "cd ../\n"
    # Cellranger
    print("Counting", srr + "...")
    if gex_or_vdj == "gex":
        command += cellranger + " count --id=ProcessedData --transcriptome=" + transcriptome_or_reference + " --fastqs=./fastq --sample=" + srr + " --localcores=16 --localmem=100 --jobmode=local" + "\n"
    else:
        command += cellranger + " vdj --id=ProcessedData --reference=" + transcriptome_or_reference + " --fastqs=./fastq --sample=" + srr + " --localcores=16 --localmem=100 --jobmode=local" + "\n"
    # Delete raw data if delete_after_count is set
    if delete_after_count:
        print("Deleting sra and fastq files...")
        command += "rm fastq/" + srr + "_S1_L00*.fast*" + "\n"
    return command

csv = []
for file in os.listdir():
    if re.match(r"^\w+_\d+.csv$", file):
        csv.append(file[ : -4])
for paper in csv:
    table = open(paper + ".csv", "r")
    header = table.readline().rstrip("\n").split("\t")
    name = header.index("sample name")
    gex = header.index("SRR")
    tcr = header.index("TCR SRR")
    samples = table.readlines()
    table.close()
    for i in range(len(samples)):
        samples[i] = samples[i].rstrip("\n").split("\t")
    print(paper + "\t" + "count: " + str(len(samples)))
    print("name" + "\t" + "gex_srr" + "\t" + "tcr_srr")
    for i in range(len(samples)):
        samples[i][gex] = "SRR" + samples[i][gex]
        samples[i][tcr] = "SRR" + samples[i][tcr]
    for sample in samples:
        print(sample[name] + "\t" +  sample[gex] + "\t" + sample[tcr])
    os.popen("mkdir " + paper + "_GEX").readlines()
    os.chdir(paper + "_GEX")
    for sample in samples:
        os.popen("mkdir " + sample[name]).readlines()
        os.chdir(sample[name])
        os.popen("mkdir sra").readlines()
        os.popen("mkdir fastq").readlines()
        file = open(sample[gex] + ".sh", "w")
        file.write(generate_command(sample[gex], "gex", transcriptome_gex))
        file.close()
        os.chdir("../")
    os.chdir("../")
    os.popen("mkdir " + paper + "_TCR").readlines()
    os.chdir(paper + "_TCR")
    for sample in samples:
        os.popen("mkdir " + sample[name]).readlines()
        os.chdir(sample[name])
        os.popen("mkdir sra").readlines()
        os.popen("mkdir fastq").readlines()
        file = open(sample[tcr] + ".sh", "w")
        file.write(generate_command(sample[tcr], "tcr", reference_tcr))
        file.close()
        os.chdir("../")
    os.chdir("../")