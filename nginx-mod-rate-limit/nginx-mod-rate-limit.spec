%global nginx_modname rate-limit
%global origname %{nginx_modname}-nginx-module

%global commit 6fffc05ca3cb391ed00453e1d26b238451e451f2
%global commitdate 20210814
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           nginx-mod-rate-limit
Version:        1.0.0
Release:        1.%{commitdate}git%{shortcommit}%{?dist}
Summary:        A Redis backed rate limit module for Nginx web servers

License:        BSD
URL:            https://github.com/weserv/rate-limit-nginx-module
Source0:        %{url}/archive/%{commit}/%{origname}-%{shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  nginx-mod-devel

Requires:       redis-rate-limiter

%description
%{summary}.

%prep
%autosetup -n %{origname}-%{commit} -p1

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
* Tue Nov  9 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.0.0-1.20210814git6fffc05
- Initial package
