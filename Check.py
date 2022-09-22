import os
import re

print(os.popen("bash Check.sh").readlines())
file = open("Results.txt", "r")
results = file.readlines()
file.close()
j = 0
new_results = ""
for i in range(len(results)):
    if i >= j:
        if re.search(r"^\./.+\.sh\.o\*?$", results[i]):
            result = results[i]
            new_results += result
            result = ""
            for j in range(i + 1, len(results)):
                if results[j] == "Pipestance completed successfully!\n":
                    result = "Pipestance completed successfully!\n"
                    break
                elif re.search(r"No such file or directory", results[j]):
                    result = "No such file or directory\n"
                    break
                elif re.search(r"\./.+\.sh\.o", results[j]):
                    result =  results[j - 2]
                    break
            if result == "":
                result =  results[j - 1]
            new_results += result + "\n"
file = open("Results.txt", "w")
file.write(new_results)
file.close()