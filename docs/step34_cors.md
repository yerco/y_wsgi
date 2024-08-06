# CORS
CORS is a security feature implemented in browsers to prevent malicious websites from making requests
to other websites. It stands for Cross-Origin Resource Sharing. When a website makes a request to another website,
the **browser** checks if the request is allowed by the CORS policy of the target website. 
If the request is not allowed, the browser will block the request and display an error message.

There's a preflight request that the browser sends to the target website to check if the request is allowed.
The preflight request is an HTTP OPTIONS request that includes the `Origin` header with the domain of the website.
The target website responds with the allowed origins in the `Access-Control-Allow-Origin` header.
