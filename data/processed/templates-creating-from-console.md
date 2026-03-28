# Creating an application by using the web console

You can use the web console to create an application from a template.

.Procedure

1. Navigate to your project and click *+Add*

1. Click *All services* in the *Developer Catalog* tile.

1. Click *Builder Images* under *Type* to see the available builder images.
> **NOTE:** Only image stream tags that have the `builder` tag listed in their annotations appear in this list, as demonstrated here:
```yaml
kind: "ImageStream"
apiVersion: "image.openshift.io/v1"
metadata:
  name: "ruby"
  creationTimestamp: null
spec:
# ...
  tags:
    - name: "2.6"
      annotations:
        description: "Build and run Ruby 2.6 applications"
        iconClass: "icon-ruby"
        tags: "builder,ruby" <1>
        supports: "ruby:2.6,ruby"
        version: "2.6"
# ...
```
<1> Including `builder` here ensures this image stream tag appears in the
web console as a builder.

1. Modify the settings in the new application screen to configure the objects
to support your application.