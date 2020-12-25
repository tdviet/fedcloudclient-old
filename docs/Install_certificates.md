If you don’t have the CA certificates installed in your machine, you can get them from
the [UMD EGI core Trust Anchor Distribution](http://repository.egi.eu/?category_name=cas)

Once installed, get the location of the requests CA bundle with:

```
python -m requests.certs
```

If the output of that command is `/etc/ssl/certs/ca-certificates.crt`, you can add EGI CAs by executing:

```
cd /usr/local/share/ca-certificates
for f in /etc/grid-security/certificates/*.pem ; do ln -s $f $(basename $f .pem).crt; done
update-ca-certificates
```

If the output is `/etc/pki/tls/certs/ca-bundle.crt` add the EGI CAs with:

```
cd /etc/pki/ca-trust/source/anchors
ln -s /etc/grid-security/certificates/*.pem .
update-ca-trust extract
```

Otherwise, you are using internal requests bundle, which can be augmented with the EGI CAs with:

```
cat /etc/grid-security/certificates/*.pem >> $(python -m requests.certs)
```
