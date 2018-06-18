# Define `python2_sitelib' if there is no one:
%{!?python2_sitelib:%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
# Enable Python 3 builds for Fedora and RHEL > 7:
%if 0%{?fedora} || 0%{?rhel} > 7
# Add `--without python3' option (enable python3 by default):
%bcond_without python3
# Define `python3_pkgversion' if there is no one:
%{!?python3_pkgversion:%global python3_pkgversion 3}
# Define `python3_sitelib' if there is no one:
%{!?python3_sitelib:%global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%else
# Add `--with python3' option (disable python3 by default):
%bcond_with python3
%endif


%global repo         pylint-plugin-utils
%global pypkgname    python-%{repo}
# 0.2.6 == 37a2c5d6307160839be64ecb78747676e2610c74 (not tagget yet)
%global commit       37a2c5d6307160839be64ecb78747676e2610c74
%global shortcommit  %(c=%{commit}; echo ${c:0:7})
%global grp          Development/Libraries
%global sum          Utilities and helpers for writing Pylint plugins


Name:           %{pypkgname}
Version:        0.2.6
Release:        1%{?dist}
Summary:        %{sum}

Group:          %{grp}

License:        GPLv2
URL:            https://github.com/landscapeio/pylint-plugin-utils
Source0:        https://github.com/PyCQA/%{repo}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
# Upstream changeset 9c522b590c66951306e837d89a214aaafb519076
Patch0:         %{pypkgname}-use_setuptools.patch
Patch1:         %{pypkgname}-do_not_depend_on_astroid.patch

BuildArch:      noarch


# Define common package dependencies.
#
# Parameters:
#
#   -V <version>  Python version.
#
%global pypkgdeps(V:) %%{expand:\
BuildRequires:  python%%{-V:%%{-V*}}%%{!-V:2}-devel\
BuildRequires:  python%%{-V:%%{-V*}}%%{!-V:2}-setuptools\
BuildRequires:  python%%{-V:%%{-V*}}%%{!-V:2}-pylint\
#BuildRequires:  python%%{-V:%%{-V*}}%%{!-V:2}-astroid\
\
# - imported by `pylint_plugin_utils/__init__.py`\
Requires:       python%%{-V:%%{-V*}}%%{!-V:2}-pylint\
# - noted in `setup.py`, but not used\
#Requires:       python%%{-V:%%{-V*}}%%{!-V:2}-astroid\
}


%description
%{sum}


%package -n python2-%{repo}
Summary:        %{sum}
Group:          %{grp}
%{?python_provide:%python_provide python2-%{repo}}

%pypkgdeps -V 2

%description -n python2-%{repo}
%{sum}


%if %{with python3}
%package -n python%{python3_pkgversion}-%{repo}
Summary:        %{sum}
Group:          %{grp}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{repo}}

%pypkgdeps -V %{python3_pkgversion}

%description -n python%{python3_pkgversion}-%{repo}
%{sum}
%endif


%prep
%autosetup -n %{repo}-%{commit} -p1


%build
%py2_build
%if %{with python3}
%py3_build
%endif


%install
%py2_install
%if %{with python3}
%py3_install
%endif


%files -n python2-%{repo}
%license LICENSE
%doc README.md
%{python2_sitelib}/*


%if %{with python3}
%files -n python%{python3_pkgversion}-%{repo}
%license LICENSE
%doc README.md
%{python3_sitelib}/*
%endif


%changelog
* Sun Jun 10 2018 Jiri Kucera <jkucera@redhat.com> - 0.2.6-1
- Initial package for Fedora
