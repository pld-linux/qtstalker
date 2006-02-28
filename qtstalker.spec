Summary:	Technical stock analysis charting app based on the Qt toolkit
Summary(pl):	Program do analiz technicznych gie³dy oparty na bibliotece Qt
Name:		qtstalker
Version:	0.32
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/qtstalker/%{name}-%{version}.tar.gz
# Source0-md5:	576907bd6299fe0cd9078334e4e5f7f3
Source1:	Qtstalker.desktop
Source2:	%{name}.png
URL:		http://qtstalker.sourceforge.net/
BuildRequires:	db-devel >= 4.2
BuildRequires:	libstdc++-devel
BuildRequires:	qt-devel >= 3.0
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qtstalker is a basic end of day Technical Analysis package with many
features. It compares with similar commercial products like Metastock,
Superchartz, Tradestation (...maybe one day) etc. If you are familiar
with those, then you should be able to muddle along with Qtstalker.

The project has kept to a lean and simple design philosophy in order
to maximize speed, portability and resource usage.

%description -l pl
Qtstalker jest prostym programem do przeprowadzania analiz
technicznych, posiadaj±cym wiele ciekawych rozwi±zañ. Jest
porównywalny do podobnych produktów komercyjnych jak Metastock,
Superchartz, Tradestation (...mo¿e którego¶ dnia) itd. Je¶li jeste¶
zaznajomiony z nimi, to powiniene¶ sobie tak¿e poradziæ z Qtstalkerem.

Projekt jest utrzymywany z za³o¿eniem zachowania prostoty i
przejrzysto¶ci interfejsu obs³ugi, aby zmaksymalizowaæ szybko¶æ,
przeno¶no¶æ i zarz±dzanie zasobami.

%prep
%setup -q -n %{name}

%build
export QMAKESPEC="%{_datadir}/qt/mkspecs/linux-g++/"
export QTDIR="%{_prefix}"
export INSTALL_ROOT=$RPM_BUILD_ROOT

for f in `find . -name \*.pro`; do
	sed -i -e 's/^\(QMAKE_CXXFLAGS += -ffast-math \)-Os/\1%{rpmcflags}/' $f
done
sed -i -e 's/^\(QMAKE_CXXFLAGS += -ffast-math \)-Os/\1%{rpmcflags}/'\
	 plugin.config

sed -i -e 's/qtstalker\/html/qtstalker-%{version}/' lib/Config.cpp

qmake -o Makefile qtstalker.pro

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_desktopdir},%{_pixmapsdir}}
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/{chart,co,db,indicator,quote}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/i18n

install lib/libqtstalker.so.*.*.* $RPM_BUILD_ROOT%{_libdir}
install plugins/chart/*/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}/chart
install plugins/co/*/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}/co
install plugins/db/*/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}/db
install plugins/indicator/*/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}/indicator
install plugins/quote/*/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}/quote
install src/qtstalker $RPM_BUILD_ROOT%{_bindir}
install i18n/*qm $RPM_BUILD_ROOT%{_datadir}/%{name}/i18n

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc docs/{AUTHORS,BUGS,CHANGELOG,TODO,*.html,*.png}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/i18n
%{_datadir}/%{name}/i18n/*
%{_desktopdir}/*
%{_pixmapsdir}/*
