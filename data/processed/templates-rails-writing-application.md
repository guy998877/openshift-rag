# Writing your application

If you are starting your Rails application from scratch, you must install the Rails gem first. Then you can proceed with writing your application.

.Procedure

1. Install the Rails gem:
```bash
$ gem install rails
```
.Example output
```bash
Successfully installed rails-4.3.0
1 gem installed
```

1. After you install the Rails gem, create a new application with PostgreSQL as your database:
```bash
$ rails new rails-app --database=postgresql
```

1. Change into your new application directory:
```bash
$ cd rails-app
```

1. If you already have an application, make sure the `pg` (postgresql) gem is present in your `Gemfile`. If not, edit your `Gemfile` by adding the gem:
```bash
gem 'pg'
```

1. Generate a new `Gemfile.lock` with all your dependencies:
```bash
$ bundle install
```

1. In addition to using the `postgresql` database with the `pg` gem, you also must ensure that the `config/database.yml` is using the `postgresql` adapter.
Make sure you updated `default` section in the `config/database.yml` file, so it looks like this:
```yaml
default: &default
  adapter: postgresql
  encoding: unicode
  pool: 5
  host: localhost
  username: rails
  password: <password>
```

1. Create your application's development and test databases:
```bash
$ rake db:create
```
This creates `development` and `test` database in your PostgreSQL server.