Summary:	Technical analysis charting app based on the Qt toolkit
Summary(pl):	Program do analiz technicznych oparty na bibliotece QT
Name:		qtstalker
Version:	0.20
Release:	1
License:	GPL
Group:		Applications/Engineering
Source0:	http://dl.sourceforge.net/qtstalker/%{name}-%{version}.tar.gz
# Source0-md5:	902330c1addb856295fbb4569c278c20
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
%setup -q -n %{name}
%patch -p1

%build
export QMAKESPEC="%{_datadir}/qt/mkspecs/linux-g++/"
export QTDIR="/usr"

%{__perl} -pi -e 's/^(QMAKE_CXXFLAGS \+= )-Os/$1%{rpmcflags}/' Qtstalker.pro
qmake -o Makefile Qtstalker.pro

%{__make}

cd plugins/indicator
%{__perl} -pi -e 's/^(QMAKE_CXXFLAGS \+= )-Os/$1%{rpmcflags}/' *.pro
./compile

cd ../quote
%{__perl} -pi -e 's/^(QMAKE_CXXFLAGS \+= )-Os/$1%{rpmcflags}/' *.pro
./compile
cd ../..

cp -fpr plainitem.xpm qtstalker.xpm

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/plugins/{indicator,quote}} \
	$RPM_BUILD_ROOT{%{_applnkdir}/Office/Misc,%{_pixmapsdir}/hicolor/16x16/apps}

install qtstalker		$RPM_BUILD_ROOT%{_bindir}
install plugins/indicator/*.so	$RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/indicator
install plugins/quote/*.so	$RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/quote

install qtstalker.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/hicolor/16x16/apps

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Office/Misc
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/{AUTHORS,BUGS,CHANGELOG,TODO,*.html,*.png}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/%{name}
%{_applnkdir}/Office/Misc/*
%{_pixmapsdir}/hicolor/16x16/apps/*
