Summary:	Technical stock analysis charting app based on the Qt toolkit
Summary(pl):	Program do analiz technicznych gie³dy oparty na bibliotece QT
Name:		qtstalker
Version:	0.26
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/qtstalker/%{name}-%{version}.tar.gz
# Source0-md5:	fce3b92f4ace89a6c5c8c4624d1b35a4
Source1:	Qtstalker.desktop
Source2:	%{name}.png
Patch0:		%{name}-db4.patch
URL:		http://qtstalker.sourceforge.net/
BuildRequires:	XFree86-libs
BuildRequires:	db-devel
BuildRequires:	libstdc++-devel
BuildRequires:	qt-devel >= 3.0
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
%setup -q 
%patch -p1

%build
export QMAKESPEC="%{_datadir}/qt/mkspecs/linux-g++/"
export QTDIR="%{_prefix}"
export INSTALL_ROOT=$RPM_BUILD_ROOT

%{__perl} -pi -e 's/^(QMAKE_CXXFLAGS \+= )-Os/$1%{rpmcflags}/' lib/*.pro
%{__perl} -pi -e 's/^(QMAKE_CXXFLAGS \+= )-Os/$1%{rpmcflags}/' plug*/*/*/*.pro
%{__perl} -pi -e 's/^(QMAKE_CXXFLAGS \+= )-Os/$1%{rpmcflags}/' qtstalker.pro
%{__perl} -pi -e 's/^(QMAKE_CXXFLAGS \+= )-Os/$1%{rpmcflags}/' src/*.pro

qmake -o Makefile qtstalker.pro

%{__make}


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/{chart,indicator,quote}}
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

install lib/libqtstalker.so.*.*.* $RPM_BUILD_ROOT%{_libdir}
install plugins/chart/*/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}/chart
install plugins/indicator/*/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}/indicator
install plugins/quote/*/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}/quote
install src/qtstalker $RPM_BUILD_ROOT%{_bindir}

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
%{_desktopdir}/*
%{_pixmapsdir}/*
