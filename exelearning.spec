Name:           exelearning
Summary:        EXe eLearning XHTML editor

Url:            http://exelearning.org/
Version:        1.04.0.3532
License:        GPL
Group:          Publishing
Release:        4
Source0:        exe-%{version}-source.tar.bz2
Source1:	exe_ru.tar.gz
Patch0:         exe-1.02.0.3303-desktop.patch
#Patch1:         exe-1.04.0.3532-deprecated_md5.patch
BuildRequires:  python-devel unzip
BuildRequires:  fdupes
BuildRequires:  python-setuptools
Requires:       python-imaging 
Requires:       python-zope-interface
Requires:       firefox
Requires:       python-xmldiff
Suggests:     %{name}-manual = %{version}


%description
eXe, the eLearning XHTML editor, is an authoring environment which enables
teachers to publish web content in standard package formats (like IMS
Content Packages and SCORM) without the need to become proficient in HTML
or XML markup.  Content generated using eXe can be used by any Learning
Management System.


%package manual
Summary:        The complete manual for eXe

Group:          Books/Other
Recommends:     %{name} = %{version}

%description manual
This package contains the complete manual for eXe.

%package devel
Summary:        Development package for eXe based software

Group:          Development/Other
Requires:       %{name} = %{version}

%description devel
This package contains the header files and libraries needed to develop
programs that use eXe.


%prep
%setup -n exe -a 1
%patch0 
#patch1 -p0
# remove the other platform binaries
#rm -f exe/webui/templates/mimetex.64.cgi exe/webui/templates/mimetex.exe
rm -f exe/webui/templates/mimetex-darwin.cgi
rm -f exe/msvcr71.dll
rm -f twisted/spread/cBanana.so
rm -f twisted/protocols/_c_urlarg.so

#exclude file requires ugly arch dependensis
%ifarch i586
rm -f exe/webui/templates/mimetex.64.cgi
%endif
%ifarch x86_64
rm -f exe/webui/templates/mimetex.cgi
%endif

%build
python rpm-setup.py build

%install
export NO_BRP_CHECK_BYTECODE_VERSION="true"
python rpm-setup.py install --prefix=%{_prefix} --root=%{buildroot}
#
cp -a twisted nevow formless %{buildroot}%{_datadir}/exe
install -Dm644 exe.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/exe.png
install -Dm644 exe.desktop %{buildroot}%{_datadir}/applications/exe.desktop
install -Dm644 exe.xml     %{buildroot}%{_datadir}/mime/packages/exe.xml

chmod 755 %{buildroot}%{_datadir}/exe/twisted/web/test/test_distrib.py
chmod 755 %{buildroot}%{_datadir}/exe/twisted/trial/test/scripttest.py
chmod 755 %{buildroot}%{_datadir}/exe/twisted/pb/tokens.py
chmod 755 %{buildroot}%{_datadir}/exe/twisted/pb/test/test_schema.py 
chmod 755 %{buildroot}%{_datadir}/exe/twisted/pb/remoteinterface.py
chmod 755 %{buildroot}%{_datadir}/exe/twisted/pb/banana.py
chmod 755 %{buildroot}%{_datadir}/exe/twisted/internet/glib2reactor.py
chmod 755 %{buildroot}%{py_puresitedir}/exe/webui/webserver.py
chmod 755 %{buildroot}%{py_puresitedir}/exe/webui/browser.py
chmod 755 %{buildroot}%{py_puresitedir}/exe/engine/version.py
chmod 755 %{buildroot}%{py_puresitedir}/exe/engine/feedparser.py
chmod 755 %{buildroot}%{py_puresitedir}/exe/application.py
chmod 755 %{buildroot}%{_datadir}/exe/templates/mimetex*.cgi


%post
if [ -f usr/bin/update-mime-database ]; then
	usr/bin/update-mime-database /usr/share/mime &> /dev/null
fi

%postun
if [ -f usr/bin/update-mime-database ]; then
  usr/bin/update-mime-database /usr/share/mime > /dev/null
fi

%files 
%doc COPYING NEWS 
%{_bindir}/exe
%dir %{py_puresitedir}/exe
%{py_puresitedir}/exe/*
%dir %{_datadir}/exe
%{_datadir}/exe/*
%exclude %{_datadir}/exe/docs/manual/*
%{_datadir}/icons/hicolor
%{_datadir}/applications/exe.desktop
%config %{_datadir}/mime/packages/exe.xml
%exclude %{_datadir}/exe/twisted/spread/cBanana.c
%exclude %{_datadir}/exe/twisted/protocols/_c_urlarg.c
%exclude %{_datadir}/exe/twisted/internet/iocpreactor/_iocp.c
%exclude %{_datadir}/exe/twisted/internet/cfsupport/cfsupport.c

%{py_puresitedir}/exe-*.egg-info

%files manual
%dir %{_datadir}/exe/docs/manual
%{_datadir}/exe/docs/manual/*

%files devel
%{_datadir}/exe/twisted/spread/cBanana.c
%{_datadir}/exe/twisted/protocols/_c_urlarg.c
%{_datadir}/exe/twisted/internet/iocpreactor/_iocp.c
%{_datadir}/exe/twisted/internet/cfsupport/cfsupport.c


