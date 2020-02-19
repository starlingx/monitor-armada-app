This repo is for
https://github.com/elastic/helm-charts/tree/master/elasticsearch
https://github.com/elastic/helm-charts/tree/master/filebeat
https://github.com/elastic/helm-charts/tree/master/kibana
https://github.com/elastic/helm-charts/tree/master/logstash
https://github.com/elastic/helm-charts/tree/master/metricbeat

Changes to this repo are needed for StarlingX and those changes are
not yet merged.
Rather than clone and diverge the repo, the repo is extracted at a particular
git SHA, and patches are applied on top.

As those patches are merged, the SHA can be updated and
the local patches removed.
