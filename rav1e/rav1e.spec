%global rav1e_version 0.6.4
#global rav1e_prever alpha
%global rav1e_tarver %{rav1e_version}%{?rav1e_prever:-%{rav1e_prever}}

Name:           rav1e
Version:        %{rav1e_version}%{?rav1e_prever:~%{rav1e_prever}}
Release:        2%{?dist}
Summary:        Fastest and safest AV1 encoder

# Upstream license specification: BSD-2-Clause
# src/ext/x86/x86inc.asm is under ISC, https://github.com/xiph/rav1e/issues/2181
License:        BSD and ISC
URL:            https://github.com/xiph/rav1e
Source0:        %{url}/archive/v%{rav1e_tarver}/%{name}-%{rav1e_tarver}.tar.gz

# Use vendored crate dependencies so we can build offline.
# Created using "cargo vendor"
Source1:        https://rpms.wsrv.nl/sources/%{name}-%{rav1e_tarver}-vendor.tar.xz

BuildRequires:  cargo-c
BuildRequires:  nasm >= 2.14.0
BuildRequires:  rust-toolset >= 1.62.1

%description
Fastest and safest AV1 encoder.

%package libs
Summary:        Library files for rav1e

%description libs
Library files for rav1e, the fastest and safest AV1 encoder.

%package devel
Summary:        Development files for rav1e
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n %{name}-%{rav1e_tarver}

# Use the vendored dependencies in Source1
%cargo_prep -V 1

%build
%cargo_build
%__cargo cbuild --release \
    --destdir=%{buildroot} \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --includedir=%{_includedir} \
    --pkgconfigdir=%{_libdir}/pkgconfig \
    --library-type=cdylib

%install
%cargo_install
%__cargo cinstall --release \
    --destdir=%{buildroot} \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --includedir=%{_includedir} \
    --pkgconfigdir=%{_libdir}/pkgconfig \
    --library-type=cdylib

%ldconfig_scriptlets libs

%files
%{_bindir}/rav1e

%files libs
%license LICENSE PATENTS
%{_libdir}/librav1e.so.0*

%files devel
%license LICENSE PATENTS
%doc README.md
%{_includedir}/rav1e/rav1e.h
%{_libdir}/librav1e.so
%{_libdir}/pkgconfig/rav1e.pc

%changelog
* Tue Apr 11 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.6.4-2
- Rename librav1e0 subpackage to rav1e-libs

* Tue Apr 11 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.6.4-1
- Update to 0.6.4

* Sun Mar 19 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.6.3-1
- Update to 0.6.3

* Wed Dec 28 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.6.2-1
- Update to 0.6.2
- Switch to %%ldconfig_scriptlets

* Mon Nov  8 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.5.0-1
- Update to 0.5.0

* Thu Aug 12 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.4.1-3
- Fix artifacts using fix from
  https://github.com/xiph/rav1e/pull/2758

* Tue Jul  6 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.4.1-2
- Rebuild with Rust 1.49.0 and cargo-c 0.8.1

* Tue Apr  6 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.4.1-1
- Update to 0.4.1

* Mon Jan 18 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.4.0-1
- Update to 0.4.0

* Fri Jan  1 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.4.0~alpha-0.3
- Import from Fedora
- Build with nasm and cargo-c from weserv repo

* Mon Dec 28 13:32:03 CET 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.4.0~alpha-0.2
- Rebuild

* Wed Dec 09 15:17:53 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.4.0~alpha-0.1
- Update to 0.4.0~alpha

* Sun Dec 06 04:37:40 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.3.4-3
- Rebuild with new cargo-c to fix pkgconfig includedir
- Fix: rhbz#1902211

* Tue Oct 20 2020 Fabio Valentini <decathorpe@gmail.com> - 0.3.4-2
- Temporarily skip some broken tests on aarch64.

* Tue Oct 20 2020 Fabio Valentini <decathorpe@gmail.com> - 0.3.4-1
- Update to version 0.3.4.

* Wed Aug 26 2020 Josh Stone <jistone@redhat.com> - 0.3.3-3
- Bump paste to 1.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 11 2020 Josh Stone <jistone@redhat.com> - 0.3.3-1
- Update to 0.3.3

* Mon Mar 09 17:45:25 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.3.1-2
- Fix pkgconfig prefix path

* Thu Feb 20 21:15:47 CET 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1

* Tue Feb 11 01:28:07 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.3.0-1
- Initial package
