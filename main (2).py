import subprocess
import time
from win10toast import ToastNotifier
import sys

TN = ToastNotifier()
currentTip=""
i=1
#程序白名单，防止一直提示你。
wz=["xxx.exe"]
def run_cmd(cmdfileName):
    global wz
    global TN
    global i

    p = subprocess.Popen(['handle64.exe', cmdfileName,'-nobanner','-u'],
              stdin=subprocess.PIPE,
              stdout=subprocess.PIPE,
              )
    try:
        outs, errs = p.communicate(timeout=15)
        out = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "\n"
        sin = outs.decode("utf-8")
        out += sin
        i += 1
        if (i == 200):
            print(i)
            i = 1
        if ("No matching handles found" in out):
            return

        with open("Gaa2.txt", "a") as f:
            for item in sin.split("\r"):

                item=item.replace("\n","").replace("\r","").strip()
                if(item==""):
                    continue
                if(wz.count(item.split(" ")[0]) <1 or  sin.find("MSI-NTC-2015\???")<0):
                    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"    "+item+"\n")
                    showToastNotifier(item.split(" ")[0])
                    f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"    "+item+"\n")



    except TimeoutError:
        p.kill()
        outs, errs = p.communicate()
        return

def showToastNotifier(strz):
    global currentTip
    TN.show_toast("通知", "检测到{0}在访问文件".format(strz), None, 7, threaded=True)
    currentTip=strz

while(1):
    run_cmd(sys.argv[1])