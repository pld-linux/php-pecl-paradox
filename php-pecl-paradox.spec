%define		_modname	paradox
%define		_status		stable
Summary:	read and write Paradox files
Summary(pl.UTF-8):	odczyt i zapis z/do plików Paradox
Name:		php-pecl-%{_modname}
Version:	1.4.3
Release:	3
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	aab0bc4146bc2852a9623b635fa20c17
URL:		http://pecl.php.net/package/Paradox/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	pxlib-devel >= 0.6.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Paradox is an extension to read and write Paradox .DB and .PX files.
It can handle almost all field types and binary large objects stored
in .MB files.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Paradox to rozszerzenie pozwalające na dostęp w trybie odczyt/zapis do
plików .DB oraz .PX bazy Paradox. Rozszerzenie pozwala na obsługę
prawie wszystkich typów pól i dużych obiektów binarnych (ang. binary
large objects, blob) przechowywanych w plikach .MB.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
mv %{_modname}-%{version}/* .

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
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
