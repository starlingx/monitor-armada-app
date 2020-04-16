%global sha 945017287598479ba8653d9baf3ff26f7fe31e50
%global helm_folder  /usr/lib/helm
%global helmchart_version 0.1.0
%global _default_patch_flags --no-backup-if-mismatch --prefix=/tmp/junk

Summary: Monitor-Helm-Elastic charts
Name: monitor-helm-elastic
Version: 1.0
Release: %{tis_patch_ver}%{?_tis_dist}
License: Apache-2.0
Group: base
Packager: Wind River <info@windriver.com>
URL: https://github.com/elastic/helm-charts/

Source0: helm-charts-elastic-%{sha}.tar.gz
Source1: repositories.yaml
Source2: index.yaml

BuildArch:     noarch

Patch01: 0001-add-makefile.patch
Patch02: 0002-use-oss-image.patch
Patch03: 0003-set-initial-masters-to-master-0.patch
Patch04: 0004-Update-Elastic-Apps-to-7.6.0-Releases.patch
Patch05: 0005-readiness-probe-enhancements.patch
Patch06: 0006-Metricbeat-nodeSelector-and-tolerations-config.patch
Patch07: 0007-Add-command-and-args-parameters-to-beats-and-logstash.patch
Patch08: 0008-Add-updateStrategy-parameter-to-beats-config.patch
Patch09: 0009-Add-hostNetworking-parameter-to-logstash-config.patch

BuildRequires: helm

%description
Monitor Helm elasticsearch charts

%prep
%setup -n helm-charts-elastic
%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1
%patch08 -p1
%patch09 -p1

%build
# initialize helm and build the toolkit
# helm init --client-only does not work if there is no networking
# The following commands do essentially the same as: helm init
%define helm_home %{getenv:HOME}/.helm
mkdir %{helm_home}
mkdir %{helm_home}/repository
mkdir %{helm_home}/repository/cache
mkdir %{helm_home}/repository/local
mkdir %{helm_home}/plugins
mkdir %{helm_home}/starters
mkdir %{helm_home}/cache
mkdir %{helm_home}/cache/archive

# Stage a repository file that only has a local repo
cp %{SOURCE1} %{helm_home}/repository/repositories.yaml

# Stage a local repo index that can be updated by the build
cp %{SOURCE2} %{helm_home}/repository/local/index.yaml

# Host a server for the charts
helm serve --repo-path . &
helm repo rm local
helm repo add local http://localhost:8879/charts

# Create the tgz files
rm elasticsearch/Makefile
rm kibana/Makefile
rm filebeat/Makefile
rm metricbeat/Makefile
rm logstash/Makefile
make elasticsearch
make kibana
make filebeat
make metricbeat
make logstash

# terminate helm server (the last backgrounded task)
kill %1

%install
install -d -m 755 ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 *.tgz ${RPM_BUILD_ROOT}%{helm_folder}

%files
%defattr(-,root,root,-)
%{helm_folder}/*
