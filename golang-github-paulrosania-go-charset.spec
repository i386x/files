# If any of the following macros should be set otherwise,
# you can wrap any of them with the following conditions:
# - %%if 0%%{centos} == 7
# - %%if 0%%{?rhel} == 7
# - %%if 0%%{?fedora} == 23
# Or just test for particular distribution:
# - %%if 0%%{centos}
# - %%if 0%%{?rhel}
# - %%if 0%%{?fedora}
#
# Be aware, on centos, both %%rhel and %%centos are set. If you want to test
# rhel specific macros, you can use %%if 0%%{?rhel} && 0%%{?centos} == 0 condition.
# (Don't forget to replace double percentage symbol with single one in order to apply a condition)
# Generate devel rpm
%global with_devel 1
# Build project from bundled dependencies
%global with_bundled 0
# Build with debug info rpm
%global with_debug 0
# Run tests in check section
%global with_check 1
# Generate unit-test rpm
%global with_unit_test 1

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         paulrosania
%global repo            go-charset
# https://github.com/paulrosania/go-charset
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          621bb39fcc835dce592e682f5073025d0169587b
%global commitdate      20151028
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
# Package specific macros:
%global pkgdata_prefix  %{_datadir}/%{repo}
%global charset_dir     datafiles

Name:           golang-%{provider}-%{project}-%{repo}
Version:        0
Release:        0.1.%{commitdate}git%{shortcommit}%{?dist}
Summary:        Character set conversion for Go
License:        BSD
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Patch0:         charsetdir-fedora-fix.patch
Patch1:         sprintf-fatalf-invalid-args-fix.patch

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check}
%endif

Provides:      golang(%{import_path}/charset) = %{version}-%{release}
Provides:      golang(%{import_path}/charset/iconv) = %{version}-%{release}
Provides:      golang(%{import_path}/data) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}
%patch0 -p1
mv charset/file.go charset/file.go.in
sed -e "s,@_DATADIR@,%{_datadir},g" charset/file.go.in > charset/file.go
rm charset/file.go.in
%patch1 -p1

%build

%install
# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
# - skip ./cmd directory since there is nothing useful for us
# - skip ./%%{charset_dir} directory since we treat it later
for file in $(find . -iname "*.go" \! \( \
    -path "./cmd" -o -path "./cmd/*" \
    -o -path "./%{charset_dir}" -o -path "./%{charset_dir}/*" \
    -o -iname "*_test.go" \
\)) ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
# - now handle ./%%{charset_dir} (maybe worthless step since all the content of
#   ./%%{charset_dir} is included in ./data/*.go files, but since readFile use
#   %%{pkgdata_prefix}/%%{charset_dir} when it meets unregistered charset, we
#   install ./%%{charset_dir} to this directory to prevent some kinds of
#   unexpected errors, especially those caused by forgotten sync between ./data
#   and ./%%{charset_dir})
install -d -p %{buildroot}%{pkgdata_prefix}/
echo "%%dir %%{pkgdata_prefix}/." >> devel.file-list
for file in $(find . -path "./%{charset_dir}/*") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}%{pkgdata_prefix}/$dirprefix
    cp -pav $file %{buildroot}%{pkgdata_prefix}/$file
    echo "%%{pkgdata_prefix}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{pkgdata_prefix}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go" \! \( \
    -path "./cmd" -o -path "./cmd/*" \
    -o -path "./%{charset_dir}" -o -path "./%{charset_dir}/*" \
\)) ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}%{gopath}:%{gopath}
%else
# No dependency directories so far

export GOPATH=%{buildroot}%{gopath}:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/charset
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc README.md
%endif

%changelog
* Thu Feb 15 2018 Jiri Kucera <jkucera@redhat.com> - 0-0.1.20151028git621bb39
- First package for Fedora
  this package is required by golang-github-elazarl-goproxy package, which is
  a dependency of bettercap 2.0.0 (resolves #1540726);
  patch charsetdir-fedora-fix.patch changes /usr/local/lib/go-charset/datafiles
  to /usr/share/go-charset/datafiles to met the Fedora Packaging Guidelines
  requirements;
  patch sprintf-fatalf-invalid-args-fix.patch fixes ill-formed format string
  in fmt.Sprintf (charset/ascii.go)  and  forgotten  t.Fatalf  arguments
  (charset/charset_test.go)
