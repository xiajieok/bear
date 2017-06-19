import os


class cpu():
    def version():
        cpu_version = os.popen("dmidecode -t 4|grep Version |awk -F ':'  '{print $2}' |awk 'NR==1'").read()
        if cpu_version == '' :
            return None
        return cpu_version

    def physical():
        cpu_physical = os.popen('cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l').read()
        if cpu_physical == '' :
            return None
        return cpu_physical

    def cores():
        cpu_cores = os.popen("cat /proc/cpuinfo| grep 'cpu cores'| uniq|awk '{print $4}'").read()
        if cpu_cores  == '' :
            return None
        return cpu_cores

    def processor():
        cpu_processor = os.popen('cat /proc/cpuinfo| grep "processor"| wc -l').read()
        if cpu_processor == '' :
            return None
        return cpu_processor




if __name__ == '__main__':
    t = cpu.cores()
    print(t)
