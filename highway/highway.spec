%global common_description %{expand:
Highway is a C++ library for SIMD (Single Instruction, Multiple Data), i.e.
applying the same operation to 'lanes'.}

%if 0%{?fedora}
%bcond_without gtest
%bcond_without contrib
%else
%bcond_with gtest
%bcond_with contrib
%endif

Name:           highway
Version:        1.1.0
Release:        1%{?dist}
Summary:        Efficient and performance-portable SIMD

License:        Apache-2.0 AND BSD-3-Clause
URL:            https://github.com/google/highway
Source0:        %url/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
%if %{with gtest}
BuildRequires:  gtest-devel
%endif
BuildRequires:  libatomic

%description
%common_description

%package        devel
Summary:        Development files for Highway
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{common_description}

Development files for Highway.

%package        doc
Summary:        Documentation for Highway
BuildArch:      noarch

%description doc
%{common_description}

Documentation for Highway.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%cmake %{!?with_gtest:-DHWY_ENABLE_TESTS:BOOL=OFF} \
       %{?with_gtest:-DHWY_SYSTEM_GTEST:BOOL=ON} \
       %{!?with_contrib:-DHWY_ENABLE_CONTRIB:BOOL=OFF}
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE LICENSE-BSD3
%{_libdir}/libhwy.so.1
%{_libdir}/libhwy.so.%{version}
%if %{with contrib}
%{_libdir}/libhwy_contrib.so.1
%{_libdir}/libhwy_contrib.so.%{version}
%endif
%if %{with gtest}
%{_libdir}/libhwy_test.so.1
%{_libdir}/libhwy_test.so.%{version}
%endif

%files devel
%license LICENSE LICENSE-BSD3
%{_includedir}/hwy/
%{_libdir}/cmake/hwy/
%{_libdir}/libhwy.so
%if %{with contrib}
%{_libdir}/libhwy_contrib.so
%{_libdir}/pkgconfig/libhwy-contrib.pc
%endif
%if %{with gtest}
%{_libdir}/libhwy_test.so
%{_libdir}/pkgconfig/libhwy-test.pc
%endif
%{_libdir}/pkgconfig/libhwy.pc

%files doc
%license LICENSE LICENSE-BSD3
%doc g3doc hwy/examples

%changelog
* Fri Mar 15 2024 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.1.0-1
- Update to 1.1.0

* Thu Oct 19 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.0.7-1
- Import from Fedora
- Update to 1.0.7

* Sat Sep 18 13:43:22 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.1-1
- Update to 1.0.1

* Sun Jun 13 13:15:46 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.12.2-1
- Update to 0.12.2

* Mon May 31 22:26:28 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.12.1-2
- Add workaround for the lack of pkgconfig in RHEL8 gtest

* Sun May 23 19:03:29 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.12.1-1
- Update to 0.12.0
- Close: rhbz#1963675

* Mon May 17 18:03:58 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.12.0-1.20210518git376a400
- Initial RPM
