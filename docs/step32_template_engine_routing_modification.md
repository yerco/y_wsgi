Changes:
- Management of assets at app level and templates at module level (without template scanner)
- Routing changes to accommodate the new structure
    - Removal of the old template scanner
    - `wrapper` Function:
      - This is the actual decorator that will wrap the handler function or class.
      - Determining `module_dir`:
        - The `handler` can be a function or a class.
        - If it’s a class, the path to its `__init__` method’s file is obtained.
        - If it’s a function, the path to its file is obtained.
        - `module_views_dir`: The directory where the handler (function or class) is defined.
        - `module_dir`: The parent directory of `module_views_dir`, which represents the module’s directory.
    - `wrapped_handler` Function:
      - This function is the actual handler that will be called when the route is accessed.
      - Setting `module_dir`:
        - `self.context.set_current_module_dir(module_dir)`: Sets the current module directory in the 
           application context.
        - Calling the Handler:
          - If the handler is a class, an instance of the class is created, and the `__call__` method is invoked.
          - If the handler is a function, it is directly called with the request context and additional arguments.
    - `self.router.add_route(path, module_dir, wrapped_handler, methods)`: Registers the route with the router.

