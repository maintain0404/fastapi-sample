# Architecture  
The repository follows a 4-layered architecture that is composed of the following components. If you need additional components, you can append them.


## domain
The domain directory contains subdirectories that handle the main business logic of the application. Each domain directory typically includes the following components, but additional components can be added as needed:
### Entity
This component includes the core domain model classes.

### Service
The service component implements key logic for each domain by using entities and repositories.

### Repo(Repository)
The repository component handles access to external infrastructure or services(database, API, etc, ...) and serves as the persistence layer in the layered architecture.


## core
The core directory contains a custom framework, basic codes for using libraries, and base classes for projects. This directory acts as a library or framework for the domain.

### base
All base classes for the entire project.

### var
The core/var directory contains application global variables.
#### config
This component provides the application's global configuration.
#### context
This components wraps python [ContextVar](https://docs.python.org/3/library/contextvars.html).


## common
The common directory includes common business logic that can be used for every domain. This component includes consts, data structures, and business logic that most domains use.


## handler
The handler directory includes protocols or a schedule runner to run the domain. Currently, this project only includes REST.
