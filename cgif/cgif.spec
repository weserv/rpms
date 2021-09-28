%global cgif_version 0.0.1
%global cgif_prever f414411
%global cgif_tarver f414411976a7dc559663b7bd9cd53cc061bed0fc

Name:           libcgif
Version:        %{cgif_version}%{?cgif_prever:~%{cgif_prever}}
Release:        1%{?dist}
Summary:        A fast and lightweight GIF encoder

License:        MIT
URL:            https://github.com/dloebl/cgif
Source0:        https://github.com/dloebl/cgif/archive/%{cgif_tarver}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson

%description
CGIF is a fast and lightweight C library for creating GIF images.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n cgif-%{cgif_tarver}

%build
%meson -Dtests=true
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license LICENSE
%doc README.md
%{_libdir}/libcgif.so.0*

%files devel
%{_includedir}/cgif.h
%{_libdir}/libcgif.so
%{_libdir}/pkgconfig/cgif.pc

%changelog
* Tue Sep 28 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.0.1~f414411-1
- Update to dloebl/cgif@f414411
- Change package name to libcgif

* Sun Sep  5 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.0.0~99724e6-1
- Initial package
