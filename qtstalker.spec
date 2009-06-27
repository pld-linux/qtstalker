Summary:	Technical stock analysis charting app based on the Qt toolkit
Summary(pl.UTF-8):	Program do analiz technicznych giełdy oparty na bibliotece Qt
Name:		qtstalker
Version:	0.36
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/qtstalker/%{name}-%{version}.tar.gz
# Source0-md5:	599589c4e84e828bd888fce6be81dab3
Source1:	Qtstalker.desktop
Source2:	%{name}.png
Patch0:		%{name}-gcc43.patch
URL:		http://qtstalker.sourceforge.net/
BuildRequires:	db-devel >= 4.2
BuildRequires:	libstdc++-devel
BuildRequires:	qmake
BuildRequires:	qt-devel >= 1:3.0
BuildRequires:	sed >= 4.0
BuildRequires:	ta-lib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qtstalker is a basic end of day Technical Analysis package with many
features. It compares with similar commercial products like Metastock,
Superchartz, Tradestation (...maybe one day) etc. If you are familiar
with those, then you should be able to muddle along with Qtstalker.

The project has kept to a lean and simple design philosophy in order
to maximize speed, portability and resource usage.

%description -l pl.UTF-8
Qtstalker jest prostym programem do przeprowadzania analiz
technicznych, posiadającym wiele ciekawych rozwiązań. Jest
porównywalny do podobnych produktów komercyjnych jak Metastock,
Superchartz, Tradestation (...może któregoś dnia) itd. Jeśli jesteś
zaznajomiony z nimi, to powinieneś sobie także poradzić z Qtstalkerem.

Projekt jest utrzymywany z założeniem zachowania prostoty i
przejrzystości interfejsu obsługi, aby zmaksymalizować szybkość,
przenośność i zarządzanie zasobami.

%prep
%setup -q
%patch0 -p1

sed -i -e 's|/usr/local/|/usr/|' -e 's|/usr/lib/|%{_libdir}/|' \
	{plugins/quote/{Yahoo/Yahoo,NYBOT/NYBOT,CSV/CSV,CME/CME},docs/docs,src/src,lib/lib}.pro \
	{src/Qtstalker,lib/{Config,RcFile}}.cpp

sed -i -e 's/^\(CONFIG +=.* thread warn_on\) debug/\1/' lib/lib.pro src/src.pro

sed -i -e 's/^\(QMAKE_CXXFLAGS += -rdynamic -ffast-math\)/\1 %{rpmcflags}/' src/src.pro
sed -i -e 's/^\(QMAKE_CXXFLAGS += -ffast-math\)/\1 %{rpmcflags}/' lib/lib.pro plugin.config

sed -i -e 's|/usr/share/doc/qtstalker/html|%{_docdir}/%{name}-%{version}|' docs/docs.pro lib/Config.cpp

%build
export QMAKESPEC="%{_datadir}/qt/mkspecs/linux-g++/"
export QTDIR="%{_prefix}"
export INSTALL_ROOT=$RPM_BUILD_ROOT

qmake -o Makefile qtstalker.pro

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_libdir}}

sed -i -e 's|/usr/lib/|%{_libdir}/|' lib/Makefile
export QTDIR="%{_prefix}"
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc docs/{AUTHORS,BUGS,CHANGELOG-0.36,TODO,*.html,*.png,qtstalker.*s,indicator,pastchanges} misc/CUS_examples
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/quote
%attr(755,root,root) %{_libdir}/%{name}/quote/*.%{version}.so
%{_datadir}/%{name}
#%dir %{_datadir}/%{name}/i18n
#%{_datadir}/%{name}/i18n/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
