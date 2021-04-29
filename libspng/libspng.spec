Name:           libspng
Version:        0.6.3
Release:        1%{?dist}
Summary:        Simple, modern libpng alternative

License:        BSD
URL:            https://libspng.org/
Source0:        https://github.com/randy408/libspng/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(zlib)

%description
Libspng is a C library for reading and writing Portable Network Graphics (PNG)
format files with a focus on security and ease of use.

Libspng is an alternative to libpng, the projects are separate and the APIs are
not compatible.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%meson -Ddev_build=true
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license LICENSE
%doc CONTRIBUTING.md README.md
%{_libdir}/libspng.so.0*

%files devel
%doc docs
%{_includedir}/spng.h
%{_libdir}/libspng.so
%{_libdir}/pkgconfig/spng.pc

%changelog
* Thu Apr 29 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.6.3-1
- Update to 0.6.3

* Sun Feb  7 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.6.2-1
- Update to 0.6.2

* Fri Jan  1 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.6.1-2
- Import from Fedora

* Sat Nov 14 14:17:48 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.1-1
- Update to 0.6.1
- Close rhbz#1879648

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 20:29:55 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.0-1
- Update to 0.6.0 (#1835162)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 21 19:17:01 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.5.0-1
- Initial package
