%define		php_name	php%{?php_suffix}
%define		modname	paradox
%define		status		stable
Summary:	read and write Paradox files
Summary(pl.UTF-8):	odczyt i zapis z/do plików Paradox
Name:		%{php_name}-pecl-%{modname}
Version:	1.4.3
Release:	6
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	aab0bc4146bc2852a9623b635fa20c17
URL:		http://pecl.php.net/package/Paradox/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	pxlib-devel >= 0.6.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Paradox is an extension to read and write Paradox .DB and .PX files.
It can handle almost all field types and binary large objects stored
in .MB files.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Paradox to rozszerzenie pozwalające na dostęp w trybie odczyt/zapis do
plików .DB oraz .PX bazy Paradox. Rozszerzenie pozwala na obsługę
prawie wszystkich typów pól i dużych obiektów binarnych (ang. binary
large objects, blob) przechowywanych w plikach .MB.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -q -c
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
