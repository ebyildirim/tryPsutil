from flask import Flask,render_template,request,redirect,url_for
import psutil
import platform





print("="*40, "System Information", "="*40)
uname = platform.uname()
machine=f"{uname.machine}"
system=f"{uname.system}"

print(f"Machine: {uname.machine}")
print(f"System: {uname.system}")



# let's print CPU information
print("="*40, "CPU Info", "="*40)
# number of cores
print("Physical cores:", psutil.cpu_count(logical=False))
PhysicalCores=psutil.cpu_count(logical=False)
print("Total cores:", psutil.cpu_count(logical=True))
TotalCores=psutil.cpu_count(logical=True)
print(f"Total CPU Usage: {psutil.cpu_percent()}%")
CpuUsage=f"{psutil.cpu_percent()}"

svmem = psutil.virtual_memory()
print(f"Total: {svmem.total}")
print(f"Available: {svmem.available}")
print(f"Used: {svmem.used}")
print(f"Percentage: {svmem.percent}%")

partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    print(f"  Total Size: {partition_usage.total}")
    print(f"  Used: {partition_usage.used}")
    print(f"  Free: {partition_usage.free}")
    print(f"  Percentage: {partition_usage.percent}%")


if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"  IP Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"  MAC Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast MAC: {address.broadcast}")


app = Flask(__name__)
@app.route('/',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        return redirect(url_for('tmp'))


    return render_template('login.html')

@app.route('/result')
def tmp():

    return render_template('result.html',machine=machine,system=system,PhysicalCores=PhysicalCores,TotalCores=TotalCores,CpuUsage=CpuUsage)


if __name__ == '__main__':
    app.run(debug=True)