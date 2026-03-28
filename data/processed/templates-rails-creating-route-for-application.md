# Creating a route for your application

You can expose a service to create a route for your application.

.Procedure

- Expose the frontend service by typing:
```bash
$ oc expose service rails-app
```

> **WARNING:** Ensure the hostname you specify resolves into the IP address of the router.