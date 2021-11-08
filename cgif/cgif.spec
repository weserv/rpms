%global cgif_version 0.0.1

Name:           cgif
Version:        %{cgif_version}
Release:        1%{?dist}
Summary:        A fast and lightweight GIF encoder

License:        MIT
URL:            https://github.com/dloebl/cgif
Source0:        %{url}/archive/V%{cgif_version}/cgif-%{cgif_version}.tar.gz

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
%autosetup -p1 -n cgif-%{cgif_version}

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
* Mon Nov  8 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.0.1-1
- Initial package
