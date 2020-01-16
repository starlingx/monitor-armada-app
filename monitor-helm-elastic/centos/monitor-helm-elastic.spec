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
Patch10: 0010-Fix-esConfig-checksum-annotation.patch
Patch11: 0011-Fix-Elasticsearch-readiness-probe-http-endpoint.patch
Patch12: 0012-Add-logstash-ingress.patch

BuildRequires: helm
BuildRequires: chartmuseum

%description
Monitor Helm elasticsearch charts

%prep
%setup -n %(tar tf %SOURCE0 | head -1)
%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1
%patch08 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

%build
# Host a server for the charts
chartmuseum --debug --port=8879 --context-path='/charts' --storage="local" --storage-local-rootdir="." &
sleep 2
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
