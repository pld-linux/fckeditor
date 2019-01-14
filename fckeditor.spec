# TODO
# - fckeditor.* provide language interfaces. package them where?
Summary:	The text editor for Internet
Summary(pl.UTF-8):	Edytor tekstowy dla Internetu
Name:		fckeditor
Version:	2.6.3
Release:	2
License:	LGPL v2.1
Group:		Applications/WWW
Source0:	https://downloads.sourceforge.net/fckeditor/FCKeditor_%{version}.tar.gz
# Source0-md5:	eb926332283376614ade9610f20b27d4
Source1:	%{name}-find-lang.sh
Patch0:		%{name}-config-php.patch
URL:		https://ckeditor.com/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	webserver(access)
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{name}

%description
This HTML text editor brings to the web many of the powerful
functionalities of desktop editors like MS Word. It's lightweight and
doesn't require any kind of installation on the client computer.

%description -l pl.UTF-8
Ten edytor tekstu HTML udostępnia stronom WWW wiele potężnych funkcji
edytorów biurowych, takich jak MS Word. Jest lekki i nie wymaga żadnej
inicjalizacji na komputerze klienckim.

%package connector-php
Summary:	File Manager Connector for PHP
Summary(pl.UTF-8):	Interfejs zarządcy plików do PHP
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Requires:	php(core) >= 5.0.0

%description connector-php
File Manager Connector for PHP.

%description connector-php -l pl.UTF-8
Interfejs zarządcy plików do PHP.

%package connector-perl
Summary:	File Manager Connector for Perl
Summary(pl.UTF-8):	Interfejs zarządcy plików do Perla
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Requires:	perl-base

%description connector-perl
File Manager Connector for Perl.

%description connector-perl -l pl.UTF-8
Interfejs zarządcy plików do Perla.

%package connector-python
Summary:	File Manager Connector for Python
Summary(pl.UTF-8):	Interfejs zarządcy plików do Pythona
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Requires:	python

%description connector-python
File Manager Connector for Python.

%description connector-python -l pl.UTF-8
Interfejs zarządcy plików do Pythona.

# copied from /usr/lib/rpm/macros
%package debuginfo
Summary:	Debug information for package %{name}
Summary(pl.UTF-8):	Informacje dla debuggera dla pakietu %{name}
Group:		Development/Debug
AutoReqProv:	0

%description debuginfo
This package provides debug information for package %{name}. Debug
information is useful when developing applications that use this
package or when debugging this package.

%description debuginfo -l pl.UTF-8
Ten pakiet dostarcza informacje dla debuggera dla pakietu %{name}.
Informacje te są przydatne przy rozwijaniu aplikacji używających tego
pakietu oraz przy odpluskwianiu samego pakietu.

%prep
%setup -qc
mv fckeditor/* .
rmdir fckeditor
mv _samples samples
mkdir samples/plugins
mv editor/plugins/bbcode/_sample samples/plugins/bbcode
rm -f editor/lang/_translationstatus.txt

install %{SOURCE1} find-lang.sh

# fck php4
mv fckeditor_php5.php fckeditor.php
rm fckeditor_php4.php

%if %{_enable_debug_packages}
%else
# source used only when FCKConfig.Debug is set: LoadScript( '_source/internals/fckdebug.js' ) ;
rm -r editor/_source
%endif

# don't know if there's any interpreter for those on linux, so kill
rm -f *.{afp,asp,cfc,cfm,lasso}
rm -rf editor/filemanager/connectors/{asp,aspx,cfm,lasso}
rm -f editor/filemanager/connectors/{test,uploadtest}.html

# undos the source
sed -i -e 's,\r$,,' fckeditor*
find '(' -name '*.js' -o -name '*.css' -o -name '*.txt' -o -name '*.html' -o -name '*.php' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%patch0 -p1

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
cp -a editor $RPM_BUILD_ROOT%{_appdir}
cp -a fckconfig.* $RPM_BUILD_ROOT%{_appdir}
cp -a *.xml $RPM_BUILD_ROOT%{_appdir}

# these are sample language interfaces. move to examples?
cp -a fckeditor.{js,php,pl,py} $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

./find-lang.sh %{name}.lang

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
mv $RPM_BUILD_ROOT{%{_appdir}/editor/filemanager/connectors/php/config.php,%{_sysconfdir}/connector.php}

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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc _*
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %{_appdir}
%dir %{_appdir}/editor
%{_appdir}/editor/css
%{_appdir}/editor/dialog
%{_appdir}/editor/skins
%{_appdir}/editor/js
%{_appdir}/editor/dtd
%{_appdir}/editor/images

%dir %{_appdir}/editor/plugins
%{_appdir}/editor/plugins/autogrow
%{_appdir}/editor/plugins/bbcode
%{_appdir}/editor/plugins/dragresizetable
%{_appdir}/editor/plugins/simplecommands
%{_appdir}/editor/plugins/tablecommands
%dir %{_appdir}/editor/plugins/placeholder
%{_appdir}/editor/plugins/placeholder/fck_placeholder.html
%{_appdir}/editor/plugins/placeholder/fckplugin.js
%{_appdir}/editor/plugins/placeholder/placeholder.gif

%dir %{_appdir}/editor/filemanager
%{_appdir}/editor/filemanager/browser
%dir %{_appdir}/editor/filemanager/connectors

%{_appdir}/editor/fckdebug.html
%{_appdir}/editor/fckdialog.html
%{_appdir}/editor/fckeditor.html
%{_appdir}/editor/fckeditor.original.html
%{_appdir}/fckconfig.js
%{_appdir}/fckeditor.js

%{_appdir}/fckpackager.xml
%{_appdir}/fckstyles.xml
%{_appdir}/fcktemplates.xml

%{_examplesdir}/%{name}-%{version}

%files connector-php
%defattr(644,root,root,755)
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/connector.php
%{_appdir}/editor/filemanager/connectors/php
# language interface actually.
%{_appdir}/fckeditor.php

%files connector-perl
%defattr(644,root,root,755)
%{_appdir}/editor/filemanager/connectors/perl
# language interface actually.
%{_appdir}/fckeditor.pl

%files connector-python
%defattr(644,root,root,755)
%{_appdir}/editor/filemanager/connectors/py
# language interface actually.
%{_appdir}/fckeditor.py

%if %{_enable_debug_packages}
%files debuginfo
%defattr(644,root,root,755)
%{_appdir}/editor/_source
%endif
