%global module ratelimit

%global commit de3bced7e9038d9fb80d2e0c51d648e3ae0b5178
%global commitdate 20220715
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           redis-rate-limiter
Version:        0.0.1
Release:        1.%{commitdate}git%{shortcommit}%{?dist}
Summary:        Implementation of the GCR Algorithm in C as a Redis Module

License:        MIT
URL:            https://github.com/onsigntv/redis-rate-limiter
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  redis-devel
BuildRequires:  redis >= 4

Requires:       redis >= 4
Requires:       redis(modules_abi)%{?_isa} = %{redis_modules_abi}

%description
A Redis module that provides rate limiting in Redis as a single command.
Implements the fairly sophisticated generic cell rate algorithm which
provides a rolling time window and doesn't depend on a background drip
process.

%prep
%autosetup -n %{name}-%{commit} -p1

%build
%set_build_flags
%make_build LD="gcc" USE_MONOTONIC_CLOCK=1

%install
mkdir -p %{buildroot}%{redis_modules_dir}
install -pDm755 %{module}.so %{buildroot}%{redis_modules_dir}/%{module}.so


%files
%license LICENSE
%doc README.md
%{redis_modules_dir}/%{module}.so


%changelog
* Sat Jul 16 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.0.1-1.20220715gitde3bced
- Update to onsigntv/redis-rate-limiter@de3bced
- Drop patch merged upstream

* Tue Nov  9 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.0.1-1.20190128git3d31d9b
- Initial package
