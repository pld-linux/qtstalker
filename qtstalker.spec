Summary:	Technical analysis charting app based on the Qt toolkit
Summary(pl):	Program do analiz technicznych bazuj±cy na bibliotece QT
Name:		qtstalker
Version:	0.15
Release:	2
License:	GPL
Group:		Applications/Engineering
Source0:	http://dl.sourceforge.net/sourceforge/qtstalker/%{name}-%{version}.tar.gz
Source1:	Qtstalker.desktop
Source2:	%{name}.png
URL:		http://qtstalker.sourceforge.net
BuildRequires:	qt-devel >= 2.2
BuildRequires:	glibc
BuildRequires:	libstdc++
BuildRequires:	qt
BuildRequires:	XFree86-libs
BuildRequires:	glibc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix			/usr/X11R6
%define		_noautocompressdoc 	*.xpm

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
tar zxvf db-2.7.7.tar.gz
cd db-2.7.7/build_unix
../dist/configure
%{__make}
cd ../../
qmake -o Makefile Qtstalker.pro
cat Makefile | sed -e "s:.(QTDIR)/lib:%{_libdir}/qt:g" |\
	sed -e "s:.(QTDIR)/include:%{_includedir}/qt:g"|\
	sed -e "s:.(QTDIR)/bin/moc:%{_bindir}/moc:g"> Makefile.pld
mv Makefile.pld Makefile
%{__make}
cd plugins/indicator
rm -rf compile.pld
for line in `cat compile |sed -e "s/ /__p_l_d__/g"`
do
	if [ "$line" == "make" ]; then
		echo "cat Makefile |\
		  sed -e 's:.(QTDIR)/lib:%{_libdir}/qt:g' |\
		  sed -e 's:.(QTDIR)/include:%{_includedir}/qt:g'|\
		  sed -e 's:.(QTDIR)/bin/moc:%{_bindir}/moc:g'> Makefile.pld" >> compile.pld
                echo "mv Makefile.pld Makefile" >> compile.pld
		echo "$line"|sed -e "s/__p_l_d__/ /g" >> compile.pld
	else
		echo "$line"|sed -e "s/__p_l_d__/ /g" >> compile.pld
	fi
done
chmod 750 compile.pld
./compile.pld
rm -rf compile.pld
cd ../quote
rm -rf compile.pld
for line in `cat compile |sed -e "s/ /__p_l_d__/g"`
do
        if [ "$line" == "make" ]; then
echo "cat Makefile | sed -e 's:.(QTDIR)/lib:%{_libdir}/qt:g' |\
   sed -e 's:.(QTDIR)/include:%{_includedir}/qt:g'|\
   sed -e 's:.(QTDIR)/bin/moc:%{_bindir}/moc:g'> Makefile.pld" >> compile.pld
		echo "mv Makefile.pld Makefile" >> compile.pld
                echo "$line"|sed -e "s/__p_l_d__/ /g" >> compile.pld
        else
                echo "$line"|sed -e "s/__p_l_d__/ /g" >> compile.pld
        fi
done
chmod 750 compile.pld
./compile.pld
rm -rf compile.pld
cd ../..
cp -fpr plainitem.xpm qtstalker.xpm
#cd docs
#for file in `ls -1 *.html`
#do
#	cat $file |sed -e "s/src=\"\.\.\//src=\"/g" > $file.pldtmp
#	mv $file.pldtmp $file
#done
#cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/plugins/{indicator,quote}} \
	$RPM_BUILD_ROOT{%{_applnkdir}/Office/Misc,/tmp/HTML/HTML} \
	$RPM_BUILD_ROOT%{_pixmapsdir}/hicolor/16x16/apps

install qtstalker		$RPM_BUILD_ROOT%{_bindir}
install plugins/indicator/*.so	$RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/indicator
install plugins/quote/*.so	$RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/quote

install qtstalker.xpm $RPM_BUILD_ROOT/%{_pixmapsdir}/hicolor/16x16/apps

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Office/Misc
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

install *.xpm		$RPM_BUILD_ROOT/tmp/HTML
install docs/*.html	$RPM_BUILD_ROOT/tmp/HTML/HTML
install docs/*.png	$RPM_BUILD_ROOT/tmp/HTML/HTML

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/{AUTHORS,BUGS,CHANGELOG,COPYING,INSTALL,README,TODO}
%doc $RPM_BUILD_ROOT/tmp/HTML
%attr(755,root,root) %{_bindir}/*
%{_libdir}/%{name}
%{_applnkdir}/Office/Misc/*
%{_pixmapsdir}/hicolor/16x16/apps/*
