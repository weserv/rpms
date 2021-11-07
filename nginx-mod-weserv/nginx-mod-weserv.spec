%global nginx_modname weserv

%global commit c2e37494cd0be1b896a1a159bd786cc919279342
%global commitdate 20211104
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           nginx-mod-weserv
Version:        5.0.0
Release:        2.%{commitdate}git%{shortcommit}%{?dist}
Summary:        Nginx weserv module

License:        BSD
URL:            https://github.com/weserv/images
Source0:        %{url}/archive/%{commit}/images-%{shortcommit}.tar.gz

Patch0:         nginx-include-path.patch
Patch1:         rename-lib.patch
Patch2:         add-pc-file.patch
Patch3:         fix-tests.patch
Patch4:         warn-if-no-ssl.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  nginx-mod-devel
BuildRequires:  cmake(Catch2) >= 2.7.1
BuildRequires:  cmake(mpark_variant) >= 1.3.0
BuildRequires:  pkgconfig(vips-cpp) >= 8.9.0

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
%autosetup -n images-%{commit} -p1

%build
%cmake -DINSTALL_NGX_MODULE=OFF \
       -DBUILD_TESTS=ON \
       -DBUILD_TOOLS=ON
%cmake_build

# Ensure nginx finds the shared API library during module build
export RPM_LD_FLAGS="${RPM_LD_FLAGS} -L$(realpath lib)"

%nginx_modconfigure
%nginx_modbuild

%check
%ctest

%install
%cmake_install

pushd %{_vpath_builddir}
install -dm 0755 %{buildroot}%{nginx_moddir}
install -pm 0755 ngx_weserv_module.so %{buildroot}%{nginx_moddir}
install -dm 0755 %{buildroot}%{nginx_modconfdir}
echo 'load_module "%{nginx_moddir}/ngx_weserv_module.so";' \
    > %{buildroot}%{nginx_modconfdir}/mod-weserv.conf
popd


%files
%license LICENSE
%doc README.md
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
* Sun Nov  7 2021  Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-2.20211104gitc2e3749
- Add patch to warn when nginx was configured without --with-http_ssl_module

* Sun Nov  7 2021  Kleis Auke Wolthuizen <info@kleisauke.nl> - 5.0.0-1.20211104gitc2e3749
- Initial packaging
