%global commit dd2e828907beaae97e742145eaf31b138899e0f1
%global commitdate 20250620
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           nginx-mod-weserv
Version:        5.0.0
Release:        1.%{commitdate}git%{shortcommit}%{?dist}
Summary:        Nginx weserv module

License:        BSD-3-Clause
URL:            https://github.com/weserv/images
Source0:        %{url}/archive/%{commit}/images-%{shortcommit}.tar.gz

%if 0%{?rhel} < 9
# Revert 94279b7 for compat with EL8
Patch0:         revert-94279b7.patch
%endif

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  nginx-mod-devel
BuildRequires:  cmake(Catch2) >= 2.7.1
BuildRequires:  pkgconfig(vips-cpp) >= 8.12.0

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use the API library of %{name}.

%package tools
Summary:        Command-line tools for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
The %{name}-tools package provides command-line tools based on the
API library of %{name}.

%prep
%autosetup -p1 -n images-%{commit}

%build
%cmake -DINSTALL_NGX_MODULE=OFF \
       -DBUILD_TESTS=ON \
       -DBUILD_TOOLS=ON
%cmake_build

%nginx_modconfigure --with-http_ssl_module
%nginx_modbuild

%check
%ctest

%install
%cmake_install

pushd %{_vpath_builddir}
install -dm 0755 %{buildroot}%{nginx_moddir}
install -pm 0755 ngx_weserv_module.so %{buildroot}%{nginx_moddir}
popd

install -dm 0755 %{buildroot}%{nginx_modconfdir}
echo 'load_module "%{nginx_moddir}/ngx_weserv_module.so";' \
    > %{buildroot}%{nginx_modconfdir}/mod-weserv.conf


%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_libdir}/libweserv.so.5*
%{nginx_moddir}/ngx_weserv_module.so
%{nginx_modconfdir}/mod-weserv.conf

%files devel
%{_includedir}/weserv
%{_libdir}/libweserv.so
%{_libdir}/pkgconfig/weserv.pc

%files tools
%{_bindir}/weserv-cli


%changelog
* Fri Jun 20 2025 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20250620gitdd2e828
- Update to weserv/images@dd2e828

* Sat Mar 15 2025 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20250315gitdc6cc09
- Update to weserv/images@dc6cc09

* Sun Feb  9 2025 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20250209git1a0ce63
- Update to weserv/images@1a0ce63

* Wed Jan  1 2025 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20250101git8816488
- Update to weserv/images@8816488

* Tue Dec 24 2024 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20241224gitf2e6e51
- Update to weserv/images@f2e6e51

* Fri Nov  1 2024 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20241101git4133e2f
- Update to weserv/images@4133e2f

* Mon Aug 12 2024 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20240812git947dbc4
- Update to weserv/images@947dbc4

* Thu Jul 25 2024 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20240725git269e35e
- Update to weserv/images@269e35e
- Migrate to Catch2 v3 on F38 and EL9

* Fri Jun 30 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20230630gitca63088
- Update to weserv/images@ca63088

* Wed May 10 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20230510git5afbb7f
- Update to weserv/images@5afbb7f

* Tue Mar 21 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20230321git7757b18
- Update to weserv/images@7757b18

* Tue Jul 26 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20220726git6dcca50
- Update to weserv/images@6dcca50

* Sun Jul  3 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20220703git8df5dbc
- Update to weserv/images@8df5dbc

* Sun Jun 19 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20220619git4a6dd21
- Update to weserv/images@4a6dd21

* Thu Apr  7 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20220407git2b51dd8
- Update to weserv/images@2b51dd8

* Sun Mar 27 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20220327git34548db
- Update to weserv/images@34548db

* Sun Feb 13 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20220213gitc4d9a26
- Update to weserv/images@c4d9a26

* Thu Jan 27 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20220126git25a9b9d
- Update to weserv/images@25a9b9d

* Sun Dec 12 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20211211git6171702
- Update to weserv/images@6171702

* Sun Nov 21 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20211121git6e45d95
- Update to weserv/images@6e45d95

* Mon Nov  8 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20211108git49c4098
- Initial package
