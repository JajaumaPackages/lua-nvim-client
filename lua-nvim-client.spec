%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))")}
# for compiled modules
%global lualibdir %{_libdir}/lua/%{luaver}
# for arch-independent modules
%global luapkgdir %{_datadir}/lua/%{luaver}

%define vermagic1 0.0.1
%define vermagic2 26

Name:           lua-nvim-client
Version:        %{vermagic1}_%{vermagic2}
Release:        1%{?dist}
Summary:        Lua client for Neovim

License:        Apache 2.0
URL:            https://github.com/neovim/lua-client
Source0:        https://github.com/neovim/lua-client/archive/%{vermagic1}-%{vermagic2}.tar.gz

BuildRequires:  lua-devel >= %{luaver}
%if 0%{?rhel} == 6
Requires:       lua >= %{luaver}
Requires:       lua < 5.2
%else
Requires:       lua(abi) >= %{luaver}
%endif
Requires:       lua-luv
Requires:       lua-coxpcall
Requires:       lua-mpack

%description
%{summary}.


%prep
%setup -q -n lua-client-%{vermagic1}-%{vermagic2}


%build
pushd nvim
%{__cc} %{optflags} -fPIC -c native.c -o native.o
%{__cc} %{__global_ldflags} -shared -o native.so native.o
popd


%install
rm -rf %{buildroot}
install -d %{buildroot}%{lualibdir}/nvim/
install -p -m755 nvim/native.so %{buildroot}%{lualibdir}/nvim/

install -d %{buildroot}%{luapkgdir}/nvim/
install -p -m644 nvim/*.lua %{buildroot}%{luapkgdir}/nvim/


%files
%license LICENSE
%doc README.md
%{lualibdir}/*
%{luapkgdir}/*


%changelog
* Sun Aug 27 2017 Jajauma's Packages <jajauma@yandex.ru> - 0.0.1_26-1
- Update to latest upstream release

* Sat Jun 04 2016 Jajauma's Packages <jajauma@yandex.ru> - 0.0.1_24-1
- Public release
