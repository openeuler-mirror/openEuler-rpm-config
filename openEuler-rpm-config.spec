%global vendor %{?_vendor:%{_vendor}}%{!?_vendor:openEuler}
%global rpmvdir /usr/lib/rpm/%{vendor}

Name:		%{vendor}-rpm-config
Version:	30
Release:	38
License:	GPL+
Summary:	specific rpm configuration files
URL:		https://gitee.com/openeuler/openEuler-rpm-config

Source0:        https://gitee.com/openeuler/openEuler-rpm-config/repository/archive/%{version}.tar.gz

Patch0:         fix-error-message-for-kmodtool.patch
Patch1:         0001-1-Add-riscv64-to-golang_arches.patch
Patch2:         Fix-a-typo-in-brp-digest-list.patch
Patch3:         change-the-vendor-to-generic-for-common-use.patch
Patch4:         remove-fexceptions.patch
Patch5:         exclude-kernel-source-and-EFI-files-in-digest-list-building.patch
Patch6:         add-brp-scripts-to-delete-rpath.patch
Patch7:         add-common-script.patch
Patch8:         Fix-python3_version-macros-for-Python-3.10.patch
Patch9:         Give-a-warning-when-using-kabi-outside-our-stablelis.patch
Patch10:        fixed-a-bug-that-missing_-p-in-macros.kmp.patch
Patch11:        update-config.guess-and-config.sub-for-loongarch64.patch
Patch12:        add-loongarch64-to-generic_arches.patch
Patch13:	add-loongarch64-support-for-config.guess-and-config.sub.patch
Patch14:        backport-kmp-feature.patch
Patch15:	0001-add-loongarch64-for-golang_arches.patch
Patch16:	fix-config-error-for-loongarch64.patch
Patch17:	Feature-support-EBS-sign-for-IMA-digest-list.patch
Patch18:        fix-brp-ldconfig-riscv-default-library-directory.patch
Patch19:        add-pyproject-macros.patch

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

%if "%{vendor}" != "openEuler"
Provides: openEuler-rpm-config = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: openEuler-rpm-config <= %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Requires: efi-srpm-macros
Requires: qt5-srpm-macros

Requires: rpm >= 4.11.0
Requires: zip
Requires: curl
#Requires: (annobin if gcc)

# for brp-mangle-shebangs
Requires: %{_bindir}/find
Requires: %{_bindir}/file
Requires: %{_bindir}/grep
Requires: %{_bindir}/sed
Requires: %{_bindir}/xargs

%if "%{_arch}" == "riscv64"
Requires: coreutils
%endif

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
install -p -m 755 -t %{buildroot}%{_rpmconfigdir} brp-*
install -p -m 644 -t %{buildroot}%{_rpmconfigdir} generic-*
install -p -m 755 -t %{buildroot}%{rpmvdir} kmodtool
install -p -m 755 -t %{buildroot}%{rpmvdir} find-requires*

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/macros.d/ macros.perl macros.python macros.go macros.forge macros.kmp

mkdir -p %{buildroot}%{_fileattrsdir}

mkdir -p %{buildroot}%{_rpmluadir}/%{_vendor}/{rpm,srpm}
install -p -m 644 -t %{buildroot}%{_rpmluadir}/%{_vendor} common.lua

# Adaptive according to vendor
sed -i "s/__vendor/%{vendor}/g" `grep "__vendor" -rl %{buildroot}%{_rpmconfigdir}`

%files
%dir %{rpmvdir}
%{rpmvdir}/macros
%{rpmvdir}/rpmrc
%{_rpmconfigdir}/brp-*
%{rpmvdir}/config.*
%{_rpmconfigdir}/generic-*
%{_fileattrsdir}/
%{_rpmconfigdir}/macros.d/
%{_rpmluadir}/%{_vendor}/*.lua
%exclude %{_rpmconfigdir}/macros.d/macros.kmp

%files -n kernel-rpm-macros
%exclude %{_prefix}/lib/rpm/*/__pycache__/*
%{rpmvdir}/kmodtool
%{_rpmconfigdir}/macros.d/macros.kmp
%{rpmvdir}/find-requires
%{rpmvdir}/find-requires.ksyms

%changelog
* Thu Apr 20 2023 caodongxia <caodongxia@h-partners.com> - 30-38
- support pyproject compilation

* Fri Mar 24 2023 laokz <zhangkai@iscas.ac.cn> - 30-37
- fix riscv64 default library directory of brp-ldconfig

* Fri Mar 17 2023 Xinliang Liu <xinliang.liu@linaro.org> - 30-36
- Fix kmod rpm install failed.

* Sat Jan 14 2023 luhuaxin <luhuaxin1@huawei.com> - 30-35
- support EBS sign

* Wed Dec 14 2022 huajingyun <huajingyun@loongson.cn> - 30-34
- fix config error for loongarch64

* Tue Dec 13 2022 Wenlong Zhang <zhangwenlong@loongson.cn> - 30-33
- add loongarch64 for golang_arches

* Wed Dec 7 2022 yangmingtai <yangmingtai@huawei.com> - 30-32
- fix latest_kernel macro

* Wed Dec 7 2022 Yang Yanchao <yangyanchao6@huawei.com> - 30-31
- backport kmp feature

* Wed Nov 30 2022 yangmingtai <yangmingtai@huawei.com> - 30-30
- support Adaptive according to vendor

* Mon Nov 21 2022 huajingyun <huajingyun@loongson.cn> - 30-29
- add loongarch64 support

* Wed Oct 12 2022 yangmingtai <yangmingtai@huawei.com> - 30-28
- macro.kmp support -p preamble

* Thu Sep  8 2022 yangmingtai <yangmingtai@huawei.com> - 30-27
- add find-requires and find-requires.ksyms

* Mon Jun 13 2022 yangmingtai <yangmingtai@huawei.com> - 30-26
- fix build failed, bare words are no longer supported

* Mon Dec 13 2021 Liu Zixian <liuzixian4@huawei.com> - 30-25
- fix python macros

* Fri Nov 26 2021 shixuantong <shixuantong@huawei.com> - 30-24
- update the definition of python3_version

* Wed Oct 13 2021 wangkerong <wangkerong@huawei.com> - 30-23
- add common lua scripts resolve "%fontpkg" macro translation failure 

* Sat Sep 4 2021 yangmingtai <yangmingtai@huawei.com> - 30-22
- add brp scripts to delete rpath

* Thu Apr 8 2021 Anakin Zhang <benjamin93@163.com> - 30-21
- exclude kernel source and EFI files in digest list building

* Mon Mar 29 2021 shenyangyang <shenyangyang4@huawei.com> - 30-20
- Patched missing patch that remove fexceptions

* Thu Mar 25 2021 shenyangyang <shenyangyang4@huawei.com> - 30-19
- Modify support for change vendor with better method

* Thu Mar 18 2021 shenyangyang <shenyangyang4@huawei.com> - 30-18
- Change the name of spec to openEuler-rpm-spec and fix few bugs

* Thu Mar 11 2021 shenyangyang <shenyangyang4@huawei.com> - 30-17
- Add for support for change vendor

* Tue Dec 1 2020 whoisxxx <zhangxuzhou4@huawei.com> - 30-16
- Add riscv64 in macros.go

* Wed Sep 30 2020 shenyangyang <shenyangyang4@huawei.com> - 30-15
- Change the source code to tar

* Fri Aug 21 2020 Wang Shuo <wangshuo_1994@foxmail.com> - 30-14
- fix error message for kmodtool

* Thu Aug 13 2020 shenyangyang <shenyangyang4@huawei.com> - 30-13
- Add provides of perl-macros

* Thu Aug 6 2020 tianwei <tianwei12@huawei.com> - 30-12
- delete strip-file-prefix

* Mon Aug 3 2020 Anakin Zhang <benjamin93@163.com> - 30-12
- add brp-digest-list

* Fri Jun 19 2020 zhangliuyan <zhangliuyan@huawei.com> - 30-11
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
