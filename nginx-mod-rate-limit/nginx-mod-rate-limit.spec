%global nginx_modname rate-limit
%global origname %{nginx_modname}-nginx-module

Name:           nginx-mod-rate-limit
Version:        1.0.0
Release:        1%{?dist}
Summary:        A Redis backed rate limit module for Nginx web servers

License:        BSD-3-Clause
URL:            https://github.com/weserv/rate-limit-nginx-module
Source0:        %{url}/archive/v%{version}/%{origname}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  nginx-mod-devel

Requires:       redis-rate-limiter

%description
%{summary}.

%prep
%autosetup -n %{origname}-%{version} -p1

%build
%nginx_modconfigure
%nginx_modbuild

%install
pushd %{_vpath_builddir}
install -dm 0755 %{buildroot}%{nginx_moddir}
install -pm 0755 ngx_http_rate_limit_module.so %{buildroot}%{nginx_moddir}
install -dm 0755 %{buildroot}%{nginx_modconfdir}
echo 'load_module "%{nginx_moddir}/ngx_http_rate_limit_module.so";' \
    > %{buildroot}%{nginx_modconfdir}/mod-rate-limit.conf
popd


%files
%license LICENSE
%doc README.md
%{nginx_moddir}/ngx_http_rate_limit_module.so
%{nginx_modconfdir}/mod-rate-limit.conf


%changelog
* Sat Jul 16 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.0.0-1
- Update to 1.0.0

* Tue Nov  9 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.0.0-1.20210814git6fffc05
- Initial package
