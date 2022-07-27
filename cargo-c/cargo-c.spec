# Use bundled deps as we don't ship the exact right versions for all the
# required rust libraries
%global bundled_rust_deps 1

%bcond_without check

# libgit2-sys expects to use its bundled library, which is sometimes just a
# snapshot of libgit2's master branch.  This can mean the FFI declarations
# won't match our released libgit2.so, e.g. having changed struct fields.
# So, be careful if you toggle this...
%bcond_without bundled_libgit2

%if 0%{?rhel}
%bcond_without bundled_libssh2
%else
%bcond_with bundled_libssh2
%endif

Name:           cargo-c
Version:        0.9.9
Release:        1%{?dist}
Summary:        Helper program to build and install c-like libraries

# Upstream license specification: MIT
License:        MIT
URL:            https://github.com/lu-zero/cargo-c
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Use vendored crate dependencies so we can build offline.
# Created using "cargo vendor"
Source1:        https://rpms.weserv.nl/sources/%{name}-%{version}-vendor.tar.xz

BuildRequires:  rust-packaging
# needed by curl-sys
BuildRequires:  pkgconfig(libcurl)
# needed by openssl-sys
BuildRequires:  pkgconfig(openssl) >= 1.0.1

%if %{with bundled_libgit2}
Provides:       bundled(libgit2) = 1.3.0
%else
BuildRequires:  pkgconfig(libgit2) >= 1.1.0
%endif

%if %{with bundled_libssh2}
Provides:       bundled(libssh2) = 1.10.0~dev
%else
# needs libssh2_userauth_publickey_frommemory
BuildRequires:  pkgconfig(libssh2) >= 1.6.0
%endif

# It only supports being called as a subcommand, e.g. "cargo cbuild"
Requires:       cargo

%description
Helper program to build and install c-like libraries.

%prep
%autosetup -p1 -n %{name}-%{version}

%if 0%{?bundled_rust_deps}
# Use the vendored dependencies in Source1
%{__tar} -xoaf %{SOURCE1}
%define cargo_registry $(pwd)/vendor
%endif

%cargo_prep

%if ! 0%{?bundled_rust_deps}
%generate_buildrequires
%cargo_generate_buildrequires
%endif

%build

%if %{without bundled_libgit2}
# convince libgit2-sys to use the distro libgit2
export LIBGIT2_SYS_USE_PKG_CONFIG=1
%endif

%if %{without bundled_libssh2}
# convince libssh2-sys to use the distro libssh2
export LIBSSH2_SYS_USE_PKG_CONFIG=1
%endif

%cargo_build

%if %{with check}
%check
%cargo_test
%endif

%install
%cargo_install

%if 0%{?bundled_rust_deps}
rm -rf %{buildroot}/%{_builddir}/%{name}-%{version}/vendor/
%endif

%files
%license LICENSE
%doc README.md
%{_bindir}/cargo-cbuild
%{_bindir}/cargo-cinstall
%{_bindir}/cargo-ctest
%{_bindir}/cargo-capi

%changelog
* Wed Jul 27 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.9.9-1
- Update to 0.9.9

* Mon Nov  8 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.9.2-2
- Add missing requirements

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
