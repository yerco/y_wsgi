# Builder

- Context: We could use the Bridge pattern to decouple the logic of building different types of HTTP responses
(e.g., JSON, HTML, XML) from the actual HTTP response object.
- Implementation Idea: Implement an HTTPResponseBuilder interface, with different concrete builders for each type
of response (e.g., `JSONResponseBuilder`, `HTMLResponseBuilder`)
