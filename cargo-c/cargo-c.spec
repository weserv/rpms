%bcond_without check

Name:           cargo-c
Version:        0.9.2
Release:        1%{?dist}
Summary:        Helper program to build and install c-like libraries

# Upstream license specification: MIT
License:        MIT
URL:            https://github.com/lu-zero/cargo-c
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Use vendored crate dependencies so we can build offline.
# Created using cargo-vendor
Source1:        https://rpms.weserv.nl/sources/%{name}-%{version}-vendor.tar.xz

BuildRequires:  rust-toolset >= 1.52.1

%description
Helper program to build and install c-like libraries.

%files
%license LICENSE
%doc README.md
%{_bindir}/cargo-cbuild
%{_bindir}/cargo-cinstall
%{_bindir}/cargo-ctest
%{_bindir}/cargo-capi

%prep
%autosetup -p1 -n %{name}-%{version}

# Source1 is vendored dependencies
%cargo_prep -V 1

%build
%cargo_build

%install
%cargo_install

%if %{with check}
%check
%cargo_test
%endif

%changelog
* Thu Aug 12 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.9.2-1
- Update to 0.9.2

* Tue Jul  6 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.8.1-1
- Update to 0.8.1

* Sun Feb  7 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.7.2-1
- Update to 0.7.2

* Fri Jan  1 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.7.0-1
- Import from Fedora
- Update to 0.7.0

* Tue Dec 29 14:21:55 CET 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.6.18-2
- Rebuild against libgit2 1.1.x

* Sun Nov 29 2020 Fabio Valentini <decathorpe@gmail.com> - 0.6.18-1
- Update to version 0.6.18+cargo-0.49.
- Fixes RHBZ#1887871

* Mon Sep 21 2020 Fabio Valentini <decathorpe@gmail.com> - 0.6.13-1
- Update to version 0.6.13.

* Sun Aug 23 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.6.10-2
- Rebuild

* Wed Jul 29 2020 Josh Stone <jistone@redhat.com> - 0.6.10-1
- Update to 0.6.10

* Fri Jul 10 2020 Josh Stone <jistone@redhat.com> - 0.6.8-1
- Update to 0.6.8

* Wed Jun 10 2020 Josh Stone <jistone@redhat.com> - 0.6.7-1
- Update to 0.6.7

* Tue May 05 2020 Josh Stone <jistone@redhat.com> - 0.6.5-1
- Update to 0.6.5

* Fri Apr 24 2020 Josh Stone <jistone@redhat.com> - 0.6.4-1
- Update to 0.6.4

* Thu Apr 23 2020 Josh Stone <jistone@redhat.com> - 0.6.3-2
- Bump to cargo 0.44

* Fri Apr 17 2020 Josh Stone <jistone@redhat.com> - 0.6.3-1
- Update to 0.6.3

* Wed Apr 15 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.6.2-2
- Rebuild for libgit2 1.0.0

* Wed Apr 01 2020 Josh Stone <jistone@redhat.com> - 0.6.2-1
- Update to 0.6.2

* Tue Mar 17 2020 Josh Stone <jistone@redhat.com> - 0.5.3-1
- Update to 0.5.3

* Wed Feb 26 2020 Josh Stone <jistone@redhat.com> - 0.5.2-4
- Update cbindgen to 0.13

* Tue Feb 11 13:41:07 CET 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.5.2-3
- Update pretty_env_logger to 0.4

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Josh Stone <jistone@redhat.com> - 0.5.2-1
- Update to 0.5.2

* Thu Dec 19 19:13:31 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.1-1
- Initial package
