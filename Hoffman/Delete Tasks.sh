qstat | grep wanluliu | grep SRR | awk '{print "qdel "$1}' | sh