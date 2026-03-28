# Understanding how to consume container values using the downward API

Your containers can consume API values by using environment variables or a volume plugin.

Depending on the method you choose, containers can consume:

- Pod name

- Pod project/namespace

- Pod annotations

- Pod labels

Annotations and labels are available using only a volume plugin.