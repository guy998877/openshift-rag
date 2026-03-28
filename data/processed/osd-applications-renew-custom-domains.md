# Renewing a certificate for custom domains

You can renew certificates with the Custom Domains Operator (CDO) by using the `oc` CLI tool.

//s a customer of OSD/ROSA, I would like instructions on how to renew certificates with Custom Domains Operator (CDO).
.Prerequisites
- You have the latest version `oc` CLI tool installed.

.Procedure
1. Create new secret
```bash
$ oc create secret tls <secret-new> --cert=fullchain.pem --key=privkey.pem -n <my_project>
```

1. Patch CustomDomain CR
```bash
$ oc patch customdomain <company_name> --type='merge' -p '{"spec":{"certificate":{"name":"<secret-new>"}}}'
```

1. Delete old secret
```bash
$ oc delete secret <secret-old> -n <my_project>
```

.Troubleshooting
- link:https://access.redhat.com/solutions/5419501[Error creating TLS secret]