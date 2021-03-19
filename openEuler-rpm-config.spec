%global vendor %{?_vendor:%{_vendor}}%{!?_vendor:openEuler}
%global rpmvdir /usr/lib/rpm/%{vendor}
# the _change_vendor macro should be defined in the project config of obs
# or just in this spec if you want to change openEuler to other vendor.
# If the _change_vendor is 1, it means that it is the first building round for all.
# rpm packages, so we need both openEuler and the vendor as an transistion.
# And the others value of _change_vendor indicates that we don't need openEuler anymore.
%global change_vendor %{?_change_vendor:%{_change_vendor}}%{!?_change_vendor:0}

Name:		%{vendor}-rpm-config
Version:	30
Release:	15
License:	GPL+
Summary:	specific rpm configuration files
URL:		https://gitee.com/openeuler/openEuler-rpm-config

Source0:        https://gitee.com/openeuler/openEuler-rpm-config/repository/archive/%{version}.tar.gz

Patch0:         fix-error-message-for-kmodtool.patch
Patch1:         Fix-a-typo-in-brp-digest-list.patch

Patch9000:      openEuler-replace-openEuler-with-_vendor-macro.patch
%if %{vendor} != openEuler && %{change_vendor} == 1
Patch9001:      openEuler-fix-brp-ldconfig.patch
%endif
Patch9002:      openEuler-remove-fexceptions.patch

Provides: python-rpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: python2-rpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: python3-rpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: python-srpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: fpc-srpm-macros = 1.1-6
Provides: ghc-srpm-macros = 1.4.2-8
Provides: gnat-srpm-macros = 4-6
Provides: nim-srpm-macros = 1-3
Provides: ocaml-srpm-macros = 5-4
Provides: openblas-srpm-macros = 2-4
Provides: perl-srpm-macros = 1-28
Provides: rust-srpm-macros = 10-1
Provides: go-srpm-macros = 2-18
Provides: perl-macros = 4:5.32.0-1
Obsoletes: perl-macros <= 4:5.32.0-1
Obsoletes: python-rpm-macros <= %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: python2-rpm-macros <= %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: python3-rpm-macros <= %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: python-srpm-macros <= %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: fpc-srpm-macros <= 1.1-6
Obsoletes: ghc-srpm-macros <= 1.4.2-8
Obsoletes: gnat-srpm-macros <= 4-6
Obsoletes: nim-srpm-macros <= 1-3
Obsoletes: ocaml-srpm-macros <= 5-4
Obsoletes: openblas-srpm-macros <= 2-4
Obsoletes: perl-srpm-macros <= 1-28
Obsoletes: rust-srpm-macros <= 10-1
Obsoletes: go-srpm-macros <= 2-18

%if %{vendor} != openEuler
Provides: openEuler-rpm-config = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: openEuler-rpm-config <= %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Requires: efi-srpm-macros
Requires: qt5-srpm-macros

Requires: rpm >= 4.11.0
Requires: zip
#Requires: (annobin if gcc)

# for brp-mangle-shebangs
Requires: %{_bindir}/find
Requires: %{_bindir}/file
Requires: %{_bindir}/grep
Requires: %{_bindir}/sed
Requires: %{_bindir}/xargs

# -fstack-clash-protection and -fcf-protection require GCC 8.
Conflicts: gcc < 7

Provides: system-rpm-config = %{version}-%{release}

%description
specific rpm configuration files for %{vendor}.

%package -n kernel-rpm-macros
Summary: Macros and scripts for building kernel module packages

%description -n kernel-rpm-macros
Macros and scripts for building kernel module packages.

%prep
%autosetup -n openEuler-rpm-config -p1

%install
mkdir -p %{buildroot}%{rpmvdir}
install -p -m 644 -t %{buildroot}%{rpmvdir} macros rpmrc
install -p -m 755 -t %{buildroot}%{rpmvdir} config.*
install -p -m 755 -t %{buildroot}%{rpmvdir} brp-*
install -p -m 644 -t %{buildroot}%{rpmvdir} openEuler-*
install -p -m 755 -t %{buildroot}%{rpmvdir} kmodtool.py

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/macros.d/ macros.perl macros.python macros.go macros.forge macros.kmp

mkdir -p %{buildroot}%{_fileattrsdir}

%if %{vendor} != openEuler
pushd %{buildroot}%{rpmvdir}
mv openEuler-hardened-cc1 %{vendor}-hardened-cc1
mv openEuler-hardened-ld %{vendor}-hardened-ld
mv openEuler-pie-cc1 %{vendor}-pie-cc1
mv openEuler-pie-ld %{vendor}-pie-ld
popd

%if %{change_vendor} == 1
pushd %{buildroot}%{rpmvdir}/../
cp -a %{vendor} openEuler
popd

pushd %{buildroot}/usr/lib/rpm/openEuler
mv %{vendor}-hardened-cc1 openEuler-hardened-cc1
mv %{vendor}-hardened-ld openEuler-hardened-ld
mv %{vendor}-pie-cc1 openEuler-pie-cc1
mv %{vendor}-pie-ld openEuler-pie-ld
popd
%endif
%endif

%files
%dir %{rpmvdir}
%{rpmvdir}/macros
%{rpmvdir}/rpmrc
%{rpmvdir}/brp-*
%{rpmvdir}/config.*
%if %{vendor} != openEuler && %{change_vendor} == 1
%exclude %{_prefix}/lib/rpm/openEuler/kmodtool.py
%{_prefix}/lib/rpm/openEuler/*
%endif
%{rpmvdir}/%{vendor}-*
%{_fileattrsdir}/
%{_rpmconfigdir}/macros.d/
%exclude %{_rpmconfigdir}/macros.d/macros.kmp

%files -n kernel-rpm-macros
%exclude %{_prefix}/lib/rpm/*/__pycache__/*
%{rpmvdir}/kmodtool.py
%if %{vendor} != openEuler && %{change_vendor} == 1
%{_prefix}/lib/rpm/openEuler/kmodtool.py
%endif
%{_rpmconfigdir}/macros.d/macros.kmp

%changelog
* Fri Mar 19 2021 shenyangyang <shenyangyang4@huawei.com> - 30-15
- Change the name of spec to openEuler-rpm-spec and fix few bugs

* Wed Mar 17 2021 shenyangyang <shenyangyang4@huawei.com> - 30-14
- Add for support for change vendor

* Wed Sep 30 2020 shenyangyang <shenyangyang4@huawei.com> - 30-13
- Add provides of perl-macros and change the source code to tar

* Fri Aug 21 2020 Wang Shuo <wangshuo_1994@foxmail.com> - 30-12
- fix error message for kmodtool

* Wed Jun 19 2020 zhangliuyan <zhangliuyan@huawei.com> - 30-11
- add kmodtool.py macros.kmp

* Wed May 6 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-10
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: disable buildid link macro

* Tue Feb 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-9
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify python_provide macro from python2 to python3

* Sun Jan 19 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-8
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:revise vendor in macro

* Sun Jan 19 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-7
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:revise macro file

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-6
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update macros file

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-5
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add macros to macros.python

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update macros.python

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:change type of files

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add source10 to package

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:rebuild

* Thu Dec 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 29-20
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
