# Creating a welcome page

Since Rails 4 no longer serves a static `public/index.html` page in production, you must create a new root page.

To have a custom welcome page must do following steps:

- Create a controller with an index action.
- Create a view page for the welcome controller index action.
- Create a route that serves applications root page with the created controller and view.

Rails offers a generator that completes all necessary steps for you.

.Procedure

1. Run Rails generator:
```bash
$ rails generate controller welcome index
```
All the necessary files are created.

1. edit line 2 in `config/routes.rb` file as follows:
root 'welcome#index'

1. Run the rails server to verify the page is available:
```bash
$ rails server
```
You should see your page by visiting http://localhost:3000 in your browser. If you do not see the page, check the logs that are output to your server to debug.