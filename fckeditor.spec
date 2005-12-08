# TODO
# - connectors subpackages
Summary:	The text editor for Internet
Name:		fckeditor
Version:	2.1.1
Release:	0.1
License:	LGPL v2.1
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/fckeditor/FCKeditor_%{version}.tar.gz
# Source0-md5:	c41f2eeb93757ed06a8556dc8f2a15a0
URL:		http://www.fckeditor.net/
BuildRequires:	sed >= 4.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/%{name}

%description
This HTML text editor brings to the web many of the powerful
functionalities of desktop editors like MS Word. It's lightweight and
doesn't require any kind of installation on the client computer.

%prep
%setup -q -n FCKeditor

# don't know if there's any interpreter for those on linux, so kill
rm -f fckeditor.{afp,asp,cfc,cfm,lasso}

# undos the source
sed -i -e 's,\r$,,' fckeditor.*
find '(' -name '*.js' -o -name '*.css' -o -name '*.txt' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

find -name '*.suspended' | xargs rm -v

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -a fckconfig.* $RPM_BUILD_ROOT%{_appdir}
cp -a editor $RPM_BUILD_ROOT%{_appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc _*
%{_appdir}
