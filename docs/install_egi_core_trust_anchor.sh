#!/bin/bash

# Install EGI Core Trust Anchor
curl http://repository.egi.eu/sw/production/cas/1/current/repo-files/egi-trustanchors.list \
         > /etc/apt/sources.list.d/egi-trustanchors.list \
    && curl https://dl.igtf.net/distribution/igtf/current/GPG-KEY-EUGridPMA-RPM-3 \
       | apt-key add - \
    && apt-get update \
    && apt-get install -y ca-policy-egi-core


# And add the certificates to Python requests bundle
cat /etc/grid-security/certificates/*.pem >> $(python -m requests.certs)