%define	pkgname	haskeline
Summary:	A command-line interface for user input, written in Haskell
Name:		ghc-%{pkgname}
Version:	0.6.2.2
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	c23a8ffbcff7cb42f0ee6ca6946285bb
URL:		http://hackage.haskell.org/package/%{pkgname}/
BuildRequires:	ghc >= 6.10
BuildRequires:	ghc-utf8-string >= 0.3.6
%requires_eq	ghc
Requires:	ghc-utf8-string >= 0.3.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		libsubdir	ghc-%(/usr/bin/ghc --numeric-version)/%{pkgname}-%{version}

%description
Haskeline provides a user interface for line input in
command-line programs. This library is similar in purpose
to readline, but since it is written in Haskell it is
(hopefully) more easily used in other Haskell programs. 

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--libsubdir=%{libsubdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{libsubdir}/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/ghc-pkg update %{_libdir}/%{libsubdir}/%{pkgname}.conf

%postun
if [ "$1" = "0" ]; then
	/usr/bin/ghc-pkg unregister %{pkgname}-%{version}
fi

%files
%defattr(644,root,root,755)
%doc CHANGES
%doc %{name}-%{version}-doc/html
%{_libdir}/%{libsubdir}
