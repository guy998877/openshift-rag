# Creating an application from source code

With the `new-app` command you can create applications from source code in a local or remote Git repository.

The `new-app` command creates a build configuration, which itself creates a new application image from your source code. The `new-app` command typically also creates a `Deployment` object to deploy the new image, and a service to provide load-balanced access to the deployment running your image.

OpenShift Container Platform automatically detects whether the pipeline, source, or docker build strategy should be used, and in the case of source build, detects an appropriate language builder image.

## Local

To create an application from a Git repository in a local directory:

```bash
$ oc new-app /<path to source code>
```

> **NOTE:** If you use a local Git repository, the repository must have a remote named `origin` that points to a URL that is accessible by the OpenShift Container Platform cluster. If there is no recognized remote,  running the `new-app` command will create a binary build.

## Remote

To create an application from a remote Git repository:

```bash
$ oc new-app https://github.com/sclorg/cakephp-ex
```

To create an application from a private remote Git repository:

```bash
$ oc new-app https://github.com/youruser/yourprivaterepo --source-secret=yoursecret
```

> **NOTE:** If you use a private remote Git repository, you can use the `--source-secret` flag to specify an existing source clone secret that will get injected into your build config to access the repository.

You can use a subdirectory of your source code repository by specifying a `--context-dir` flag. To create an application from a remote Git repository and a context subdirectory:

```bash
$ oc new-app https://github.com/sclorg/s2i-ruby-container.git \
    --context-dir=2.0/test/puma-test-app
```

Also, when specifying a remote URL, you can specify a Git branch to use by appending `#<branch_name>` to the end of the URL:

```bash
$ oc new-app https://github.com/openshift/ruby-hello-world.git#beta4
```

## Build strategy detection

OpenShift Container Platform automatically determines which build strategy to use by detecting certain files:

- If a Jenkins file exists in the root or specified context directory of the source repository when creating a new application, OpenShift Container Platform generates a pipeline build strategy.
> **NOTE:** The `pipeline` build strategy is deprecated; consider using Red Hat OpenShift Pipelines instead.
- If a Dockerfile exists in the root or specified context directory of the source repository when creating a new application, OpenShift Container Platform generates a docker build strategy.
- If neither a Jenkins file nor a Dockerfile is detected, OpenShift Container Platform generates a source build strategy.

Override the automatically detected build strategy by setting the `--strategy` flag to `docker`, `pipeline`, or `source`.

```bash
$ oc new-app /home/user/code/myapp --strategy=docker
```

> **NOTE:** The `oc` command requires that files containing build sources are available in a remote Git repository. For all source builds, you must use `git remote -v`.

## Language detection

If you use the source build strategy, `new-app` attempts to determine the language builder to use by the presence of certain files in the root or specified context directory of the repository:

.Languages detected by `new-app`
[cols="4,8",options="header"]
|===

|Language |Files
|`dotnet`
|`project.json`, `pass:[*.csproj]`
|`jee`
|`pom.xml`

|`nodejs`
|`app.json`, `package.json`

|`perl`
|`cpanfile`, `index.pl`

|`php`
|`composer.json`, `index.php`

|`python`
|`requirements.txt`, `setup.py`

|`ruby`
|`Gemfile`, `Rakefile`, `config.ru`

|`scala`
|`build.sbt`

|`golang`
|`Godeps`, `main.go`
|===

After a language is detected, `new-app` searches the OpenShift Container Platform server for image stream tags that have a `supports` annotation matching the detected language, or an image stream that matches the name of the detected language. If a match is not found, `new-app` searches the [Docker Hub registry](https://registry.hub.docker.com) for an image that matches the detected language based on name.

You can override the image the builder uses for a particular source repository by specifying the image, either an image stream or container
specification, and the repository with a `~` as a separator. Note that if this is done, build strategy detection and language detection are not carried out.

For example, to use the `myproject/my-ruby` imagestream with the source in a remote repository:

```bash
$ oc new-app myproject/my-ruby~https://github.com/openshift/ruby-hello-world.git
```

To use the `openshift/ruby-20-centos7:latest` container image stream with the source in a local repository:

```bash
$ oc new-app openshift/ruby-20-centos7:latest~/home/user/code/my-ruby-app
```

> **NOTE:** Language detection requires the Git client to be locally installed so that your repository can be cloned and inspected. If Git is not available, you can avoid the language detection step by specifying the builder image to use with your repository with the `<image>~<repository>` syntax. The `-i <image> <repository>` invocation requires that `new-app` attempt to clone `repository` to determine what type of artifact it is, so this will fail if Git is not available. The `-i <image> --code <repository>` invocation requires `new-app` clone `repository` to determine whether `image` should be used as a builder for the source code, or deployed separately, as in the case of a database image.