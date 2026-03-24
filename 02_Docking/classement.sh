for log in */*_log.txt; do
    score=$(grep -m 1 "^ *1 " "$log" | awk '{print $2}')
    fichier=$(basename "$log")
    name=${fichier%_log.txt}
    
    echo -e "${name} \t : ${score}"
done | sort -k3 -n