
Summary:	Technical analysis charting app based on the Qt toolkit.
Summary(pl):	Program do analiz technicznych bazuj±cy na bibliotece QT.
Name:		qtstalker
Version:	0.15
Release:	1
License:	GPL
Group:		Office/Misc
######		Unknown group!
Source0:	http://cesnet.dl.sourceforge.net/sourceforge/qtstalker/%{name}-%{version}.tar.gz
URL:		http://qtstalker.sourceforge.net
BuildRequires:	qt-devel >= 2.2
BuildRequires:	glibc
BuildRequires:	libstdc++
BuildRequires:	qt
BuildRequires:	XFree86-libs
BuildRequires:	glibc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

#-%{version}-root-%(id -u -n)
%define _kdedir /usr/X11R6
%define _kdedatadir %{_kdedir}/share


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
export QMAKESPEC="%{_prefix}/X11R6/share/qt/mkspecs/linux-g++/"
tar zxvf db-2.7.7.tar.gz
cd db-2.7.7/build_unix
../dist/configure
%{__make}
cd ../../
qmake -o Makefile Qtstalker.pro
cat Makefile | sed -e "s/.(QTDIR)\/lib/\%{_prefix}\/X11R6\/lib\/qt/g" | sed -e "s/.(QTDIR)\/include/\%{_prefix}\/X11R6\/include\/qt/g"| sed -e "s/.(QTDIR)\/bin\/moc/\%{_prefix}\/X11R6\/bin\/moc/g"> Makefile.pld
mv Makefile.pld Makefile
%{__make}
cd plugins/indicator
rm -rf compile.pld
for line in `cat compile |sed -e "s/\ /__p_l_d__/g"`
do
	if [ "$line" == "make" ]; then
echo "cat Makefile | sed -e 's/.(QTDIR)\/lib/\%{_prefix}\/X11R6\/lib\/qt/g' | sed -e 's/.(QTDIR)\/include/\%{_prefix}\/X11R6\/include\/qt/g'| sed -e 's/.(QTDIR)\/bin\/moc/\%{_prefix}\/X11R6\/bin\/moc/g'> Makefile.pld" >> compile.pld
                echo "mv Makefile.pld Makefile" >> compile.pld
		echo "$line"|sed -e "s/__p_l_d__/\ /g" >> compile.pld
	else
		echo "$line"|sed -e "s/__p_l_d__/\ /g" >> compile.pld
	fi
done
chmod 750 compile.pld
./compile.pld
rm -rf compile.pld
cd ../quote
rm -rf compile.pld
for line in `cat compile |sed -e "s/\ /__p_l_d__/g"`
do
        if [ "$line" == "make" ]; then
echo "cat Makefile | sed -e 's/.(QTDIR)\/lib/\%{_prefix}\/X11R6\/lib\/qt/g' | sed -e 's/.(QTDIR)\/include/\%{_prefix}\/X11R6\/include\/qt/g'| sed -e 's/.(QTDIR)\/bin\/moc/\%{_prefix}\/X11R6\/bin\/moc/g'> Makefile.pld" >> compile.pld
		echo "mv Makefile.pld Makefile" >> compile.pld
                echo "$line"|sed -e "s/__p_l_d__/\ /g" >> compile.pld
        else
                echo "$line"|sed -e "s/__p_l_d__/\ /g" >> compile.pld
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
cat>>Qtstalker.desktop<<EOF
[Desktop Entry]
Name=Qtstalker
Name[pl]=Qtstalker
Comment=Qtstalker is a basic technical analysis charting app based on the Qt toolkit.
Comment[pl]=Qtstalker to program do przeprowadzania analiz technicznych bazuj±cy na bibliotece QT.
TryExec=qtstalker
Exec=qtstalker
Icon=qtstalker.xpm
Terminal=0
Type=Application

EOF


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_bindir}
install qtstalker $RPM_BUILD_ROOT/%{_bindir}
install -d $RPM_BUILD_ROOT/%{_libdir}
install -d $RPM_BUILD_ROOT/%{_libdir}/%{name}
install -d $RPM_BUILD_ROOT/%{_libdir}/%{name}/plugins
install -d $RPM_BUILD_ROOT/%{_libdir}/%{name}/plugins/indicator
install plugins/indicator/*.so $RPM_BUILD_ROOT/%{_libdir}/%{name}/plugins/indicator
install -d $RPM_BUILD_ROOT/%{_libdir}/%{name}/plugins/quote
install plugins/quote/*.so $RPM_BUILD_ROOT/%{_libdir}/%{name}/plugins/quote

install -d $RPM_BUILD_ROOT/%{_kdedir}
install -d $RPM_BUILD_ROOT/%{_kdedatadir}
install -d $RPM_BUILD_ROOT/%{_kdedatadir}/pixmaps/
install -d $RPM_BUILD_ROOT/%{_kdedatadir}/pixmaps/hicolor
install -d $RPM_BUILD_ROOT/%{_kdedatadir}/pixmaps/locolor
install -d $RPM_BUILD_ROOT/%{_kdedatadir}/pixmaps/hicolor/16x16
install -d $RPM_BUILD_ROOT/%{_kdedatadir}/pixmaps/locolor/16x16
install -d $RPM_BUILD_ROOT/%{_kdedatadir}/pixmaps/hicolor/16x16/apps
install -d $RPM_BUILD_ROOT/%{_kdedatadir}/pixmaps/locolor/16x16/apps
install qtstalker.xpm $RPM_BUILD_ROOT/%{_kdedatadir}/pixmaps/hicolor/16x16/apps
install qtstalker.xpm $RPM_BUILD_ROOT/%{_kdedatadir}/pixmaps/locolor/16x16/apps

install -d $RPM_BUILD_ROOT/%{_kdedatadir}/applnk
install -d $RPM_BUILD_ROOT/%{_kdedatadir}/applnk/Office
install -d $RPM_BUILD_ROOT/%{_kdedatadir}/applnk/Office/Misc
install Qtstalker.desktop $RPM_BUILD_ROOT/%{_kdedatadir}/applnk/Office/Misc

install -d $RPM_BUILD_ROOT/%{_datadir}
install -d $RPM_BUILD_ROOT/%{_datadir}/doc
install -d $RPM_BUILD_ROOT/%{_datadir}/doc/%{name}-%{version}
install -d $RPM_BUILD_ROOT/%{_datadir}/doc/%{name}-%{version}/HTML
install *.xpm $RPM_BUILD_ROOT/%{_datadir}/doc/%{name}-%{version}/HTML/

install -d $RPM_BUILD_ROOT/%{_datadir}/doc/%{name}-%{version}/HTML/HTML
install docs/*.html $RPM_BUILD_ROOT/%{_datadir}/doc/%{name}-%{version}/HTML/HTML/
install docs/*.png $RPM_BUILD_ROOT/%{_datadir}/doc/%{name}-%{version}/HTML/HTML/

install docs/AUTHORS docs/BUGS docs/CHANGELOG docs/COPYING docs/INSTALL docs/README docs/TODO $RPM_BUILD_ROOT/%{_datadir}/doc/%{name}-%{version}
gzip -S .gz -9 $RPM_BUILD_ROOT/%{_datadir}/doc/%{name}-%{version}/{AUTHORS,BUGS,CHANGELOG,COPYING,INSTALL,README,TODO}




%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/%{name}/plugins/indicator/*.so
%{_libdir}/%{name}/plugins/quote/*.so
%{_kdedatadir}/pixmaps/hicolor/16x16/apps/*
%{_kdedatadir}/pixmaps/locolor/16x16/apps/*
%{_kdedatadir}/applnk/Office/Misc/*
%attr(755,root,root) %{_bindir}/*
