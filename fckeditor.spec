# TODO
# - connectors subpackages (for language deps)
# - subpackage for _source (or don't package at all), used only when FCKConfig.Debug is set: LoadScript( '_source/internals/fckdebug.js' ) ;
Summary:	The text editor for Internet
Summary(pl.UTF-8):	Edytor tekstowy dla Internetu
Name:		fckeditor
Version:	2.6.3
Release:	0.7
License:	LGPL v2.1
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/fckeditor/FCKeditor_%{version}.tar.gz
# Source0-md5:	eb926332283376614ade9610f20b27d4
URL:		http://www.fckeditor.net/
BuildRequires:	rpmbuild(macros) > 1.268
BuildRequires:	sed >= 4.0
Requires:	webserver(access)
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/%{name}

%description
This HTML text editor brings to the web many of the powerful
functionalities of desktop editors like MS Word. It's lightweight and
doesn't require any kind of installation on the client computer.

%description -l pl.UTF-8
Ten edytor tekstu HTML udostępnia stronom WWW wiele potężnych funkcji
edytorów biurowych, takich jak MS Word. Jest lekki i nie wymaga żadnej
inicjalizacji na komputerze klienckim.

%prep
%setup -qc
mv fckeditor/* .
rmdir fckeditor
mv _samples samples

# don't know if there's any interpreter for those on linux, so kill
rm -f *.{afp,asp,cfc,cfm,lasso}

# undos the source
sed -i -e 's,\r$,,' fckeditor*
find '(' -name '*.js' -o -name '*.css' -o -name '*.txt' -o -name '*.html' -o -name '*.php' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

# apache1/apache2 conf
cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

# lighttpd conf
cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -a fckconfig.* $RPM_BUILD_ROOT%{_appdir}
cp -a fckeditor.* fckeditor_php4.php fckeditor_php5.php $RPM_BUILD_ROOT%{_appdir}
cp -a editor $RPM_BUILD_ROOT%{_appdir}
cp -a *.xml $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc _*
%{_appdir}

%{_examplesdir}/%{name}-%{version}
