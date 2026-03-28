# Storing your application in Git

Building an application in OpenShift Container Platform usually requires that the source code be stored in a git repository, so you must install `git` if you do not already have it.

.Prerequisites

- Install git.

.Procedure

1. Make sure you are in your Rails application directory by running the `ls -1` command. The output of the command should look like:
```bash
$ ls -1
```
.Example output
```bash
app
bin
config
config.ru
db
Gemfile
Gemfile.lock
lib
log
public
Rakefile
README.rdoc
test
tmp
vendor
```

1. Run the following commands in your Rails app directory to initialize and commit your code to git:
```bash
$ git init
```
```bash
$ git add .
```
```bash
$ git commit -m "initial commit"
```
After your application is committed you must push it to a remote repository. GitHub account, in which you create a new repository.

1. Set the remote that points to your `git` repository:
```bash
$ git remote add origin git@github.com:<namespace/repository-name>.git
```

1. Push your application to your remote git repository.
```bash
$ git push
```