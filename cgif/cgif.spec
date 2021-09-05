%global cgif_version 0.0.0
%global cgif_prever 80bd8fb
%global cgif_tarver 80bd8fb500dd3ac108c2b8dcc1dcfa9dd597323b

Name:           cgif
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

%package     -n libcgif
Summary:        Library files for %{name}

%description -n libcgif
Library files for %{name}, the fast and lightweight GIF encoder.

%package     -n libcgif-devel
Summary:        Development files for %{name}
Requires:       libcgif%{?_isa} = %{version}-%{release}

%description -n libcgif-devel
The libcgif-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n %{name}-%{cgif_tarver}

%build
%meson -Dtests=true
%meson_build

%install
%meson_install

%check
%meson_test

%files -n libcgif
%license LICENSE
%doc README.md
%{_libdir}/libcgif.so

%files -n libcgif-devel
%{_includedir}/cgif.h
%{_libdir}/pkgconfig/cgif.pc

%changelog
* Sun Sep  5 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.0.0~99724e6-1
- Initial package
