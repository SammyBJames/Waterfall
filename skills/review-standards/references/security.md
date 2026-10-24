# Security

Treat input from beyond the Quality bar's trust boundary as hostile: request bodies, query strings, headers, cookies, file names, file contents and metadata, plugin output, and stored data an untrusted user wrote.

- **Authentication and authorization.** Every new endpoint or action checks who the caller is and that they may touch *this* object. Look for IDOR (IDs taken from the request without an ownership or scope check), unguarded admin paths, and sessions or tokens still accepted after logout, rotation or revocation.
- **Injection.** SQL built by string formatting. Shell commands with interpolated arguments (use argument arrays). Path traversal (`..`, absolute paths, symlinks, odd encodings) when building file paths. HTML or JS injection (`{@html}`, `innerHTML`, `dangerouslySetInnerHTML`). Header injection, SSRF through user-supplied URLs, template injection, unsafe deserialization.
- **Secrets and crypto.** Secrets in code, logs, errors or client bundles. Low-entropy tokens, tokens compared with `==` instead of in constant time, or stored unhashed when they only need verifying. Home-made crypto, nonce or IV reuse, missing integrity checks.
- **Web.** CSRF on cookie-authenticated state changes. Cookie flags (`HttpOnly`, `Secure`, `SameSite`). Over-open CORS. Open redirects. Cache headers on private data.
- **Sandboxes and plugins.** Sandboxed or plugin code reaching the host, network, files or other users' data beyond its grant, or grants checked only at install time.
- **Supply chain.** A new dependency that isn't needed, maintained or pinned.
- **Information leaks.** Secrets, stack traces or other users' data in responses, logs or errors that untrusted users can see.

**Not reported unless the Quality bar makes it a concrete risk** (for example a public or multi-tenant service):

- denial of service and resource exhaustion: missing rate limits, size caps, timeouts and pagination caps;
- missing validation on fields that aren't security-relevant;
- leaks of no use to an attacker, such as internal IDs or timing on non-secret data;
- hardening a trusted component against its own operator, such as a local tool against its user.

For each finding, name the attacker, what they send, and what they gain.
