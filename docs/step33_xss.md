# Cross-Site Scripting (XSS)

Cross-Site Scripting (XSS) is a type of security vulnerability that allows attackers to inject malicious scripts
into web pages viewed by other users. The attacker can use XSS to steal sensitive information, 
such as login credentials, or perform other malicious actions on behalf of the victim.

## Content Security Policy (CSP)
Content Security Policy (CSP) is a security feature that helps prevent various types of attacks, 
including Cross-Site Scripting (XSS) and data injection attacks, by controlling which resources
(e.g., scripts, styles, images) a web page can load.
CSP allows us to define approved sources of content and helps to mitigate the risk of malicious content 
being executed on our web pages.

### How CSP Works
CSP is implemented via the Content-Security-Policy HTTP header. 
This header contains a series of directives that define the policy. 
Each directive specifies which type of content the policy applies to and which sources are allowed
for that type of content.

#### Key Directives

Here are some of the key directives used in CSP:
- `default-src`: Serves as a fallback for other directives that you do not specify. If you don’t specify
`script-src`, `style-src`, etc., they will use the source values defined in `default-src`.
- `script-src`: Defines valid sources for JavaScript.
- `style-src`: Defines valid sources for CSS.
- `img-src`: Defines valid sources for images.
- `object-src`: Defines valid sources for `<object>`, `<embed>`, and `<applet>` elements.
- `frame-src`: Defines valid sources for nested browsing contexts like `<iframe>`.
- `font-src`: Defines valid sources for fonts.
- `connect-src`: Defines valid sources for AJAX, WebSocket, and EventSource connections.
- `media-src`: Defines valid sources for media like audio and video.

Here’s an example of a CSP header that allows resources only from the same origin and trusted sources:
```
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted.cdn.com; 
style-src 'self' https://trusted.cdn.com; img-src 'self' https://images.example.com; object-src 'none';
```

## X-XSS-Protection header
It works by enabling the built-in XSS protection filter found in most modern web browsers.
- `0`: Disables the XSS filter.
  - Example: `X-XSS-Protection: 0`
- `1`: Enables the XSS filter.
  - Example: `X-XSS-Protection: 1`
- `1; mode=block`: Enables the XSS filter and, instead of attempting to sanitize the page, 
   the browser will prevent rendering of the page if an attack is detected.
  - Example: `X-XSS-Protection: 1; mode=block`

## Problem faced at browser
```
Refused to apply inline style because it violates the following Content Security Policy directive: 
"default-src 'self'". Either the 'unsafe-inline' keyword, a hash 
('sha256-4Su6mBWzEIFnH4pAGMOuaeBrstwJN4Z3pq/s1Kn4/KQ='), or a nonce ('nonce-...') is required to enable 
inline execution. Note that hashes do not apply to event handlers, style attributes and javascript: 
navigations unless the 'unsafe-hashes' keyword is present. Note also that 'style-src' was not explicitly
set, so 'default-src' is used as a fallback.
```
Solution 1: Add 'unsafe-inline' keyword to the style-src directive
Solution 2: A more secure approach is to use nonces or hashes for inline styles and scripts