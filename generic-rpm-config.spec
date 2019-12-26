%global vendor %{?_vendor:%{_vendor}}%{!?_vendor:openEuler}

Name:       %{vendor}-rpm-config
Version:    29
Release:    20
License:    GPL+
Summary:    specific rpm configuration files
URL:        https://src.fedoraproject.org/rpms/redhat-rpm-config

# Core rpm settings
#fedora 29 snapshots from https://src.fedoraproject.org/rpms/redhat-rpm-config
Source0: redhat-rpm-config-118.tar.gz
#https://src.fedoraproject.org/rpms/fpc-srpm-macros/blob/f29/f/macros.fpc-srpm
Source1: macros.fpc-srpm
#https://src.fedoraproject.org/rpms/ghc-srpm-macros/blob/f29/f/macros.ghc-srpm
Source2: macros.ghc-srpm
#https://src.fedoraproject.org/rpms/gnat-srpm-macros/blob/f29/f/macros.gnat-srpm
Source3: macros.gnat-srpm
#https://src.fedoraproject.org/rpms/nim-srpm-macros/tree/f29
Source4: macros.nim-srpm
#https://src.fedoraproject.org/rpms/ocaml-srpm-macros/blob/f29/f/macros.ocaml-srpm
Source5: macros.ocaml-srpm
#https://src.fedoraproject.org/rpms/openblas-srpm-macros/blob/f29/f/macros.openblas-srpm
Source6: macros.openblas-srpm
#https://src.fedoraproject.org/rpms/perl-srpm-macros/blob/f29/f/macros.perl-srpm
Source7: macros.perl-srpm
#https://pagure.io/fedora-rust/rust2rpm
Source8: macros.rust-srpm
#https://github.com/gofed/go-macros
Source9: macros.go-srpm


#python https://src.fedoraproject.org/rpms/python-rpm-macros/blob/f29/
Source10:        macros.python
Source11:        macros.python-srpm
Source12:        macros.python2
Source13:        macros.python3
Source14:        macros.pybytecompile

Source99:        macros.openEuler

Patch0: genericOS.patch
Patch1: remove-fcf-protection-for-gcc-7.3.0-x86_64.patch

Provides: python-rpm-macros = %{version}-%{release}
Provides: python2-rpm-macros = %{version}-%{release}
Provides: python3-rpm-macros = %{version}-%{release}
Provides: python-srpm-macros = %{version}-%{release}
Provides: fpc-srpm-macros
Provides: ghc-srpm-macros
Provides: gnat-srpm-macros
Provides: nim-srpm-macros
Provides: ocaml-srpm-macros
Provides: openblas-srpm-macros
Provides: perl-srpm-macros
Provides: rust-srpm-macros
Provides: go-srpm-macros
Obsoletes: python-rpm-macros
Obsoletes: python2-rpm-macros
Obsoletes: python3-rpm-macros
Obsoletes: python-srpm-macros
Obsoletes: fpc-srpm-macros
Obsoletes: ghc-srpm-macros
Obsoletes: gnat-srpm-macros
Obsoletes: nim-srpm-macros
Obsoletes: ocaml-srpm-macros
Obsoletes: openblas-srpm-macros
Obsoletes: perl-srpm-macros
Obsoletes: rust-srpm-macros
Obsoletes: go-srpm-macros

Requires: efi-srpm-macros
Requires: qt5-srpm-macros

Requires: rpm >= 4.11.0
Requires: dwz >= 0.4
Requires: zip
#Requires: (annobin if gcc)

# for brp-mangle-shebangs
Requires: %{_bindir}/find
Requires: %{_bindir}/file
Requires: %{_bindir}/grep
Requires: sed
Requires: %{_bindir}/xargs

# -fstack-clash-protection and -fcf-protection require GCC 8.
Conflicts: gcc < 7

Provides: system-rpm-config = %{version}-%{release}

%global rrcdir /usr/lib/rpm/%{vendor}

%description
specific rpm configuration files for %{vendor}.

%package -n kernel-rpm-macros
Summary: Macros and scripts for building kernel module packages
Requires: %{vendor}-rpm-config

%description -n kernel-rpm-macros
Macros and scripts for building kernel module packages.

%prep
sed -i "s/generic_os/%{vendor}/g" $RPM_SOURCE_DIR/genericOS.patch

%setup -T -c
tar -xf %{SOURCE0} --strip-components 1
%patch0 -p1
%patch1 -p1
mv redhat-hardened-cc1 %{vendor}-hardened-cc1
mv redhat-hardened-ld %{vendor}-hardened-ld
mv redhat-annobin-cc1 %{vendor}-annobin-cc1

%install
mkdir -p %{buildroot}%{rrcdir}
install -p -m 644 -t %{buildroot}%{rrcdir} macros rpmrc
install -p -m 444 -t %{buildroot}%{rrcdir} %{vendor}-hardened-*
install -p -m 444 -t %{buildroot}%{rrcdir} %{vendor}-annobin-*
install -p -m 755 -t %{buildroot}%{rrcdir} config.*
install -p -m 755 -t %{buildroot}%{rrcdir} dist.sh rpmsort symset-table kmodtool
install -p -m 755 -t %{buildroot}%{rrcdir} brp-*

install -p -m 755 -t %{buildroot}%{rrcdir} find-*
mkdir -p %{buildroot}%{rrcdir}/find-provides.d
install -p -m 644 -t %{buildroot}%{rrcdir}/find-provides.d firmware.prov modalias.prov

install -p -m 755 -t %{buildroot}%{rrcdir} brp-*

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/macros.d macros.*

mkdir -p %{buildroot}%{_fileattrsdir}
install -p -m 644 -t %{buildroot}%{_fileattrsdir} *.attr
install -p -m 755 -t %{buildroot}%{_rpmconfigdir} kmod.prov

install -m 644 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} \
  %{SOURCE9} %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE99}\
  %{buildroot}/%{rpmmacrodir}/

%files
%dir %{rrcdir}
%{rrcdir}/macros
%{rrcdir}/rpmrc
%{rrcdir}/brp-*
%{rrcdir}/dist.sh
%{rrcdir}/%{vendor}-hardened-*
%{rrcdir}/%{vendor}-annobin-*
%{rrcdir}/config.*
%{rrcdir}/find-provides
%{rrcdir}/find-requires
%{rrcdir}/brp-ldconfig
%{_fileattrsdir}/*.attr
%{_rpmconfigdir}/kmod.prov
%{_rpmconfigdir}/macros.d/macros.*
%doc buildflags.md
%exclude %{_rpmconfigdir}/macros.d/macros.kmp

%files -n kernel-rpm-macros
%dir %{rrcdir}/find-provides.d
%{rrcdir}/kmodtool
%{rrcdir}/rpmsort
%{rrcdir}/symset-table
%{rrcdir}/find-provides.ksyms
%{rrcdir}/find-requires.ksyms
%{rrcdir}/find-provides.d/firmware.prov
%{rrcdir}/find-provides.d/modalias.prov
%{_rpmconfigdir}/macros.d/macros.kmp

%changelog
* Thu Dec 26 2019 openEuler Buildteam <buildteam@openeuler.org> 29-20
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:delete unneeded provides

* Wed Nov 27 2019 fanghuiyu<fanghuiyu@huwei.com> - 29-19
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:change to generic-rpm-config

* Fri Nov 15 2019 jiangchuangang<jiangchuangang@huwei.com> - 29-18
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: remove fcf-protection for x86_64 from rpmrc

* Wed Oct 30 2019 hexiaowen <hexiaowen@huawei.com> - 29-17
- add custom macros

* Wed Sep 25 2019 hexiaowen <hexiaowen@huawei.com> - 29-16
- add rust-srpm-macros and go-srpm-macros

* Fri Sep 20 2019 hexiaowen <hexiaowen@huawei.com> - 29-15
- add version-release for python-rpm-macros

* Fri Sep 20 2019 hexiaowen <hexiaowen@huawei.com> - 29-14
- add python-rpm-macros fpc-srpm-macros ghc-srpm-macros gnat-srpm-macros
- nim-srpm-macros ocaml-srpm-macros openblas-srpm-macros perl-srpm-macros

* Thu Aug 29 2019 hexiaowen <hexiaowen@huawei.com> - 29-13
- fix typo

* Tue Aug 27 2019 hexiaowen <hexiaowen@huawei.com> - 29-2
- delete annobin

* Wed Jul 18 2018 openEuler Buildteam <buildteam@openeuler.org> - 29-1
- Package init
