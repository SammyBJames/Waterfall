# Security

Treat every input from outside the process as hostile: request bodies, query strings, headers, cookies, file names, file contents and metadata, plugin output, environment, and anything read back from the database that a user wrote.

- **Authentication and authorization.** Does every new endpoint or action check who the caller is, and that they may touch *this* object? Look for IDOR: IDs taken from the request without checking ownership or scope (user, library, tenant). Check admin-only paths, and that a session or token is not still accepted after logout, rotation or revocation.
- **Injection.** SQL built with string formatting. Shell commands with interpolated arguments (prefer argument arrays). Path traversal (`..`, absolute paths, symlinks, odd encodings) in anything that builds a file path. HTML or JS injection in rendered output (`{@html}`, `innerHTML`, `dangerouslySetInnerHTML`). Header injection, SSRF through user-supplied URLs or hosts, template injection, unsafe deserialization.
- **Secrets and crypto.** Secrets in code, logs, error messages or client bundles. Tokens without enough entropy, compared with `==` instead of in constant time, or stored unhashed when they only need to be verified. Home-made crypto where a standard construction exists. Nonce or IV reuse. Missing integrity checks.
- **Limits.** Missing rate limits, size caps (bodies, uploads, JSON depth, decompressed size), timeouts, or pagination caps. Each gap is a denial-of-service path.
- **Web specifics.** CSRF on state-changing requests that use cookies. Cookie flags (`HttpOnly`, `Secure`, `SameSite`). CORS that is too open. Open redirects. Cache headers on private data.
- **Sandboxes and plugins.** Can sandboxed or plugin code reach the host, the network, files or other users' data beyond what it was granted? Is a grant checked at use time as well as at install time?
- **Supply chain.** Any new dependency: is it needed, maintained, and pinned?
- **Information leaks.** Stack traces, internal IDs, whether an account exists, timing differences.

For each finding, describe the attacker, what they send, and what they gain.
