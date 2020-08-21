# -*- coding: UTF-8 -*- 
#!/usr/bin/python3

# kmodtool - Helper script for building kernel module RPMs

import os,subprocess,sys

def print_verrel ():
    #verrel=subprocess.getoutput("(rpm -q --qf '%{VERSION}-%{RELEASE}' `rpm -q kernel-devel` | head -n 1)")
   # if (len(verrel)== 0):
    verrel=subprocess.getoutput("uname -r")
    return verrel
  
def print_rpmtemplate():
    kmod_name = sys.argv[2]
 #   verrel=subprocess.getoutput("(rpm -q --qf '%{VERSION}-%{RELEASE}' `rpm -q kernel-devel` | head -n 1)")
  #  if (len(verrel)== 0):
    verrel=subprocess.getoutput("uname -r")

    if not kmod_name:
        print("Please provide the kmodule-name as first parameter.") 
        exit()
    get_rpmtemplate(kmod_name,verrel)


def get_rpmtemplate(kmod_name,verrel):
    print("%package       -n kmod-" + kmod_name)
    print("Summary:        " + kmod_name + " " + "kernel module(s)")
    print("Group:           System Environment/Kernel")
    if  "%{version}":
        print("Version: %{version}")
    if  "%{release}":
        print("Release: %{release}")
    print("Provides:         kernel-modules =" + " " + verrel)
    print("Provides:         "+ kmod_name + "-kmod = %{?epoch:%{epoch}:}%{version}-%{release}")
    print("Requires(post):   /usr/sbin/depmod") 
    print("Requires(postun): /usr/sbin/depmod")
    print("%description   -n kmod-" + kmod_name)
    print("This package provides the " + kmod_name + " kernel modules built for the Linux")
    print("kernel "+ verrel + " for the %{_target_cpu} family of processors.")
    print("%post          -n kmod-" + kmod_name)
    print("if [ -e /boot/System.map-" + verrel + " ]; then")
    print("   /sbin/depmod -aeF /boot/System.map-" + verrel +" " + verrel +"> /dev/null || :")
    print("fi")
    if (kmp !=""):
        print("modules=( $(find /lib/modules/" + verrel + "/extra/" + kmod_name + ") )")
        print("""if [ -x "/sbin/weak-modules" ]; then
    printf '%s\\n' "${modules[@]}" | /sbin/weak-modules --add-modules
fi""") 
        print("%preun         -n kmod-" + kmod_name)
        print("rpm -ql kmod-" + kmod_name + "| grep '\.ko$'   > /var/run/rpm-kmod-" + kmod_name +"-modules")

    print("%postun        -n kmod-" + kmod_name)
    print("/sbin/depmod -aF /boot/System.map-" + verrel+" " + verrel + " &> /dev/null || :")

    if (kmp !=""):
        print("modules=( $(cat /var/run/rpm-kmod-" + kmod_name + "-modules) )")
        print("#rm /var/run/rpm-kmod-" + kmod_name + "-modules")
        print("""if [ -x "/sbin/weak-modules" ]; then
    printf '%s\\n' "${modules[@]}" | /sbin/weak-modules --remove-modules
fi""")

    print("%files         -n kmod-" + kmod_name)
    kmp_override_filelist= sys.argv[3]
    if  kmp_override_filelist == '%filelist':
        print("%defattr(644,root,root,755)")
        print("/lib/modules/" + verrel)
        print("/lib/firmware/")
    else:
        with open(kmp_override_filelist) as f:
            for line in f:
                print(line, end = '')
     
#for i in range(len(sys.argv)): 
if (sys.argv[1] == "verrel"):
    print_verrel()
if (sys.argv[1] == "rpmtemplate_kmp"):
    kmp=1
    print_rpmtemplate()
else:
    print("Error: Unknown option 'sys.argv[i]'.")
    exit()

