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


%global repo       logilab-common
%global repo_0     %(r=%{repo}; echo ${r:0:1})
%global pypkgname  python-%{repo}
%global grp        Development/Libraries
%global sum        Common libraries for Logilab projects
%global desc\
This package contains several modules providing low level functionality shared\
among some python projects developed by logilab.

%global testscript '\
import sys\
import os\
import warnings\
warnings.simplefilter("default", DeprecationWarning)\
sys.path.insert(0, os.getcwd())\
from logilab.common.pytest import run\
run()\
'

Name:           %{pypkgname}
Version:        1.4.1
Release:        1%{?dist}
Summary:        %{sum}

Group:          %{grp}

License:        LGPLv2+
URL:            https://www.logilab.org/project/logilab-common
Source0:        https://files.pythonhosted.org/packages/source/%{repo_0}/%{repo}/%{repo}-%{version}.tar.gz
Patch0:         %{pypkgname}-proper_PyColorize_import.patch
Patch1:         %{pypkgname}-do_not_depend_on_egenix_mx_base.patch
Patch2:         %{pypkgname}-do_not_depend_on_logilab_aspects.patch
Patch3:         %{pypkgname}-urllib2_compat.patch
Patch4:         %{pypkgname}-do_not_install_logilab-pytest.patch

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
BuildRequires:  python%%{-V:%%{-V*}}%%{!-V:2}-six >= 1.4.0\
BuildRequires:  python%%{-V:%%{-V*}}%%{!-V:2}-sphinx\
BuildRequires:  python%%{-V:%%{-V*}}%%{!-V:2}-kerberos\
# - imported by `test/unittest_date.py`\
# - imported by `test/unittest_modutils.py`\
BuildRequires:  python%%{-V:%%{-V*}}%%{!-V:2}-pytz\
\
# - for `pkg_resources` imported by `logilab/__init__.py`\
# - for `pkg_resources` imported by `logilab/common/__init__.py`\
# - for `pkg_resources` imported by `logilab/common/modutils.py`\
Requires:       python%%{-V:%%{-V*}}%%{!-V:2}-setuptools\
# - imported by `logilab/common/__init__.py`\
# - imported by `logilab/common/changelog.py`\
# - imported by `logilab/common/compat.py`\
# - imported by `logilab/common/configuration.py`\
# - imported by `logilab/common/daemon.py`\
# - imported by `logilab/common/date.py`\
# - imported by `logilab/common/logging_ext.py`\
# - imported by `logilab/common/modutils.py`\
# - imported by `logilab/common/optik_ext.py`\
# - imported by `logilab/common/registry.py`\
# - imported by `logilab/common/shellutils.py`\
# - imported by `logilab/common/table.py`\
# - imported by `logilab/common/tasksqueue.py`\
# - imported by `logilab/common/testlib.py`\
# - imported by `logilab/common/umessage.py`\
# - imported by `logilab/common/ureports/docbook_writer.py`\
# - imported by `logilab/common/ureports/html_writer.py`\
# - imported by `logilab/common/ureports/nodes.py`\
# - imported by `logilab/common/ureports/text_writer.py`\
# - imported by `test/unittest_configuration.py`\
# - imported by `test/unittest_deprecation.py`\
# - imported by `test/unittest_shellutils.py`\
# - imported by `test/unittest_table.py`\
# - imported by `test/unittest_testlib.py`\
# - imported by `test/unittest_umessage.py`\
Requires:       python%%{-V:%%{-V*}}%%{!-V:2}-six >= 1.4.0\
# - imported by `logilab/common/sphinx_ext.py`\
Requires:       python%%{-V:%%{-V*}}%%{!-V:2}-sphinx\
# - imported by `logilab/common/urllib2ext.py`\
Requires:       python%%{-V:%%{-V*}}%%{!-V:2}-kerberos\
\
# - occasionally imported by `logilab/common/date.py`\
# - occasionally imported by `logilab/common/optik_ext.py`\
# - occasionally imported by `logilab/common/umessage.py`\
# - occasionally imported by `test/unittest_date.py`\
# Note: python2 only package, do not depend on it\
#Recommends:     python%%{-V:%%{-V*}}%%{!-V:2}-egenix-mx-base\
# - occasionally imported by `logilab/common/debugger.py`\
Recommends:     python%%{-V:%%{-V*}}%%{!-V:2}-ipython\
# - occasionally imported by `logilab/common/pytest.py`\
# - occasionally imported by `logilab/common/testlib.py`\
Recommends:     python%%{-V:%%{-V*}}%%{!-V:2}-unittest2 >= 0.5.1\
# - occasionally imported by `logilab/common/pytest.py`\
Recommends:     python%%{-V:%%{-V*}}%%{!-V:2}-django\
# - occasionally imported by `logilab/common/pytest.py`\
# Note: python2 only package, do not depend on it\
#Recommends:     python%%{-V:%%{-V*}}%%{!-V:2}-logilab-aspects\
}


%description
%{desc}


%package -n python2-%{repo}
Summary:        %{sum}
Group:          %{grp}
%{?python_provide:%python_provide python2-%{repo}}

%pypkgdeps -V 2

%description -n python2-%{repo}
%{desc}


%if %{with python3}
%package -n python%{python3_pkgversion}-%{repo}
Summary:        %{sum}
Group:          %{grp}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{repo}}

%pypkgdeps -V %{python3_pkgversion}

%description -n python%{python3_pkgversion}-%{repo}
%{desc}
%endif


%prep
%autosetup -n %{repo}-%{version} -p1


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


%check
%{__python2} -c %{testscript}
%if %{with python3}
%{__python3} -c %{testscript}
%endif


%files -n python2-%{repo}
%license COPYING COPYING.LESSER
%doc ChangeLog README
%{python2_sitelib}/*


%if %{with python3}
%files -n python%{python3_pkgversion}-%{repo}
%license COPYING COPYING.LESSER
%doc ChangeLog README
%{python3_sitelib}/*
%endif


%changelog
* Thu Jun 14 2018 Jiri Kucera <jkucera@redhat.com> - 1.4.1-1
- Unretiring package
  update to upstream 1.4.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.63.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.63.2-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63.2-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.63.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 0.63.2-4
- Rebuilt for Python3.5 rebuild
- Turn off tests as they only cause import error

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 29 2015 Brian C. Lane <bcl@redhat.com> 0.63.2-2
- Add python-six dependency

* Wed Jan 28 2015 Brian C. Lane <bcl@redhat.com> 0.63.2-1
- Upstream 0.63.2
  Switched source url from ftp to pypi.python.org

* Fri Oct 03 2014 Brian C. Lane <bcl@redhat.com> 0.62.1-1
- Upstream 0.62.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.61.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.61.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Feb 27 2014 Brian C. Lane <bcl@redhat.com> 0.61.0-1
- Upstream 0.61.0
  Fixes CVE-2014-1838 and CVE-2014-1839

* Thu Oct 24 2013 Brian C. Lane <bcl@redhat.com> 0.60.0-2
- Switching on python3 support

* Tue Aug 13 2013 Brian C. Lane <bcl@redhat.com> 0.60.0-1
- Upstream 0.60.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Brian C. Lane <bcl@redhat.com> 0.58.3-1
- Upstream 0.58.3
- Add python3-logilab-common subpackage to spec. Not ready to turn it on yet
  due to this upstream bug: http://www.logilab.org/ticket/110213

* Fri Aug 03 2012 Brian C. Lane <bcl@redhat.com> 0.58.2-1
- Upstream 0.58.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.57.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.57.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Brian C. Lane <bcl@redhat.com> - 0.57.1-1
- Upstream 0.57.1

* Fri Jul 29 2011 Brian C. Lane <bcl@redhat.com> - 0.56.0-1
- Upstream 0.56.0

* Mon Mar 28 2011 Brian C. Lane <bcl@redhat.com> - 0.55.1-1
- Upstream 0.55.1
- Add unit tests to spec

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.53.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 29 2010 Brian C. Lane <bcl@redhat.com> - 0.53.0-1
- Upstream 0.53.0

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.50.3-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 08 2010 Brian C. Lane <bcl@brdhat.com> - 0.50.3-1
- Upstream 0.50.3

* Fri Mar 26 2010 Brian C. Lane <bcl@redhat.com> - 0.49.0-2
- Add python-setuptools to BuildRequires

* Thu Mar 25 2010 Brian C. Lane <bcl@redhat.com> - 0.49.0-1
- Upstream 0.49.0

* Sun Aug 30 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.45.0-1
- Upstream 0.45.0 (small enhancements and bugfixes)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.41.0-2
- Upstream 0.41.0
- Bugfixes and a few minor new features

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.38.0-1
- Upstream 0.38.0

* Tue Dec 30 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.37.0-1
- Upstream 0.37.0

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.32.0-2
- Rebuild for Python 2.6

* Mon Jun 30 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.32.0-1
- Upstream 0.32.0

* Sun Feb 17 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.28.0-1
- Upstream 0.28.0

* Thu Jan 17 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.26.1-1
- Upstream 0.26.1
- Package egg-info and other files.

* Mon Dec 24 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.25.2-1
- Upstream 0.25.2

* Sun Nov 18 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.24.0-1
- Upstream 0.24.0
- Adjust license to the new standard

* Sun Apr 01 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.21.2-1
- Upstream 0.21.2

* Sun Dec 17 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.21.0-1
- Upstream 0.21.0
- Include COPYING with docs

* Tue Sep 26 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.19.2-1
- Upstream 0.19.2
- Ghostbusting
- Require mx

* Mon May 01 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.15.0-1
- Version 0.15.0

* Sun Mar 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.14.1-2
- Also handle __init__.pyc and __init__.pyo

* Sun Mar 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.14.1-1
- Version 0.14.1

* Thu Jan 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.13.0-1
- Version 0.13.0
- astng no longer part of the package

* Thu Nov 17 2005 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.12.0-1
- Version 0.12.0

* Mon Jun 13 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.10.0-1
- Version 0.10.0.
- Disttagging.

* Thu May 05 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.9.3-3
- Fix paths.

* Tue Apr 26 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.9.3-2
- Ghost .pyo files.
- Get rid of test, which doesn't do anything.

* Fri Apr 22 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.9.3-1
- Initial packaging.
