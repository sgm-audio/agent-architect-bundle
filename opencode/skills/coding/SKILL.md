---
name: coding
description: General programming skills including algorithms, data structures, design patterns, debugging, code review, refactoring, testing, and software architecture. Use when writing, debugging, or improving code in any programming language.
---

# Coding Skills

## Data Structures

### Linear Structures
- **Arrays**: Contiguous memory, O(1) access
- **Linked Lists**: Singly, doubly, circular
- **Stacks**: LIFO, push/pop operations
- **Queues**: FIFO, enqueue/dequeue
- **Deques**: Double-ended queue

### Non-Linear Structures
- **Trees**: Binary, AVL, Red-Black, B-trees
- **Heaps**: Min-heap, max-heap, priority queues
- **Graphs**: Directed, undirected, weighted
- **Tries**: Prefix trees for string operations
- **Hash Tables**: Collision handling, load factor

### Specialized Structures
- **Bloom filters**: Probabilistic set membership
- **Skip lists**: Probabilistic sorted containers
- **LRU caches**: Least Recently Used cache
- **Disjoint sets**: Union-find data structure

## Algorithms

### Sorting
- **Bubble sort**: Simple O(n²) algorithm
- **Quick sort**: Average O(n log n), in-place
- **Merge sort**: O(n log n), stable
- **Heap sort**: O(n log n), in-place
- **Radix sort**: O(nk) for integers/strings

### Searching
- **Binary search**: O(log n) sorted data
- **Linear search**: O(n) simple search
- **Depth-first search**: Graph/tree traversal
- **Breadth-first search**: Level-order traversal

### Graph Algorithms
- **Dijkstra**: Shortest path
- **Bellman-Ford**: Negative weights
- **A***: Heuristic pathfinding
- **Kruskal/Prim**: Minimum spanning tree
- **Topological sort**: DAG ordering

### Dynamic Programming
- **Memoization**: Top-down with cache
- **Tabulation**: Bottom-up approach
- **Common problems**: Knapsack, LCS, edit distance

### String Algorithms
- **KMP**: Pattern matching
- **Rabin-Karp**: Hash-based matching
- **Aho-Corasick**: Multi-pattern matching

## Design Patterns

### Creational
- **Singleton**: One instance globally
- **Factory**: Object creation abstraction
- **Builder**: Complex object construction
- **Prototype**: Clone objects
- **Abstract Factory**: Factory families

### Structural
- **Adapter**: Interface compatibility
- **Bridge**: Abstraction/implementation separation
- **Composite**: Tree structures
- **Decorator**: Add behavior dynamically
- **Facade**: Simplified interface
- **Proxy**: Controlled access

### Behavioral
- **Observer**: Event subscription
- **Strategy**: Interchangeable algorithms
- **Command**: Encapsulate operations
- **State**: Object behavior based on state
- **Template Method**: Algorithm skeleton
- **Iterator**: Collection traversal

## Testing

### Unit Testing
- **Test frameworks**: pytest, JUnit, Jest
- **Assertions**: assertEqual, assertTrue, assertRaises
- **Fixtures**: Setup/teardown
- **Mocks**: Mock dependencies
- **Parametrized tests**: Multiple inputs

### Integration Testing
- **Database testing**: Transaction rollback
- **API testing**: HTTP clients
- **Service integration**: Mock services

### Test-Driven Development (TDD)
- **Red-Green-Refactor**: Write failing test first
- **Test coverage**: Aim for meaningful coverage
- **Regression prevention**: Prevent bugs

### Testing Strategies
- **Black box**: Input/output testing
- **White box**: Code path testing
- **Property-based**: QuickCheck-style testing

## Debugging

### Techniques
- **Print debugging**: Strategic output
- **Breakpoints**: IDE debuggers
- **Logging**: Structured logging
- **Memory debugging**: Valgrind, memory profilers

### Common Issues
- **Null/nil handling**: Check for null
- **Off-by-one errors**: Boundary conditions
- **Race conditions**: Thread synchronization
- **Memory leaks**: Resource management

### Tools
- **GDB/LLDB**: C/C++ debugging
- **pdb**: Python debugger
- **Chrome DevTools**: JavaScript debugging
- **IDE debuggers**: VS Code, IntelliJ

## Code Quality

### Clean Code
- **Naming**: Descriptive variable/function names
- **Functions**: Single responsibility
- **Comments**: Explain why, not what
- **Formatting**: Consistent style

### Refactoring
- **Extract method**: Break large methods
- **Rename**: Clearer naming
- **Inline**: Simplify obvious code
- **Move**: Better location for code

### Code Review
- **Checklist**: Review for common issues
- **Feedback**: Constructive criticism
- **Automation**: Linters, formatters

## Version Control

### Git Best Practices
- **Commits**: Atomic, descriptive messages
- **Branching**: Feature branches, PR flow
- **Merging**: Rebase vs merge
- **Conflict resolution**: Understand both sides

### Workflows
- **Gitflow**: Feature/release/hotfix branches
- **GitHub Flow**: Simple branch-per-feature
- **Trunk-based**: Short-lived branches

## Performance

### Optimization
- **Profiling**: Find bottlenecks
- **Algorithmic**: Better algorithm choice
- **Caching**: Memoization
- **Concurrency**: Parallel processing

### Memory
- **Allocation**: Stack vs heap
- **Garbage collection**: Understanding GC
- **Leaks**: Detect and fix
- **Pooling**: Object reuse

### Scalability
- **Horizontal**: Add more machines
- **Vertical**: Add more resources
- **Sharding**: Distribute data

## Security

### Common Vulnerabilities
- **Injection**: SQL, command injection
- **XSS**: Cross-site scripting
- **CSRF**: Cross-site request forgery
- **Authentication**: Proper auth flows

### Best Practices
- **Input validation**: Sanitize all input
- **Secrets**: Don't hardcode secrets
- **Dependencies**: Keep updated
- **Least privilege**: Minimal permissions

## API Design

### REST
- **Resources**: Nouns, not verbs
- **HTTP methods**: GET/POST/PUT/DELETE
- **Status codes**: 200, 201, 400, 404, 500
- **Versioning**: /v1/, header, Accept

### GraphQL
- **Schema**: Type definitions
- **Queries**: Data fetching
- **Mutations**: Data modification
- **Subscriptions**: Real-time updates

### Error Handling
- **Consistent format**: Same error structure
- **Error codes**: Machine-readable codes
- **Logging**: Log errors with context

## Database

### SQL
- **Queries**: SELECT with JOINs
- **Indexes**: Improve query speed
- **Transactions**: ACID properties
- **Normalization**: 1NF, 2NF, 3NF

### NoSQL
- **Document**: MongoDB, CouchDB
- **Key-Value**: Redis, DynamoDB
- **Wide-column**: Cassandra
- **Graph**: Neo4j

### ORMs
- **Query building**: SQL abstraction
- **Migrations**: Schema versioning
- **Models**: Entity relationships

## Concurrency

### Threading
- **Threads**: Parallel execution
- **Synchronization**: Locks, semaphores
- **Thread pools**: Reuse threads

### Async Programming
- **Promises/Futures**: Asynchronous results
- **Async/await**: Synchronous-looking async code
- **Event loops**: Non-blocking I/O

### Common Issues
- **Deadlocks**: Circular wait conditions
- **Race conditions**: Unsynchronized access
- **Starvation**: Thread never gets resources

## Documentation

### Code Documentation
- **Docstrings**: Function descriptions
- **Comments**: Explain complex logic
- **README**: Project overview
- **API docs**: Endpoint documentation

### Types
- **Type hints**: Python type annotations
- **JSDoc**: JavaScript documentation
- **Javadoc**: Java documentation

## DevOps

### CI/CD
- **Pipelines**: Automated builds/tests
- **Testing**: Automated test suites
- **Deployment**: Automated deploys
- **Rollbacks**: Revert bad deployments

### Containers
- **Docker**: Containerization
- **Kubernetes**: Orchestration
- **Compose**: Multi-container apps

### Infrastructure
- **IaC**: Terraform, CloudFormation
- **Configuration**: Ansible, Chef
- **Monitoring**: Metrics, logging

## Architecture

### Principles
- **SOLID**: Single responsibility, Open-closed, Liskov substitution, Interface segregation, Dependency inversion
- **DRY**: Don't repeat yourself
- **KISS**: Keep it simple
- **YAGNI**: You aren't gonna need it

### Patterns
- **Microservices**: Small, independent services
- **Monolith**: Single codebase
- **Event-driven**: Event-based communication
- **Layered**: Presentation, business, data layers
- **Hexagonal**: Ports and adapters

## Problem Solving

### Approach
- **Understand**: Read problem carefully
- **Plan**: Outline solution approach
- **Implement**: Write code
- **Test**: Verify solution
- **Optimize**: Improve if needed

### Common Techniques
- **Brute force**: Try all possibilities
- **Greedy**: Make best immediate choice
- **Divide and conquer**: Split and combine
- **Backtracking**: Try, undo, try again

## Code Organization

### Project Structure
```
/src
  /components
  /services
  /utils
/tests
/config
/docs
```

### Naming Conventions
- **camelCase**: variables, functions (JS)
- **snake_case**: variables, functions (Python)
- **PascalCase**: classes, components
- **SCREAMING_SNAKE_CASE**: constants
