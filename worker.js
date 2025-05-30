/**
 * PawGrooming Static Site Worker
 * Serves static HTML files with clean URL routing using Cloudflare's new assets feature
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    let pathname = url.pathname;

    // Clean URL routing
    // Root path -> index.html
    if (pathname === '/') {
      pathname = '/index.html';
    }
    // Clean URLs for city pages: /austin -> /austin/index.html
    else if (!pathname.includes('.') && !pathname.endsWith('/')) {
      pathname = `${pathname}/index.html`;
    }
    // Trailing slash: /austin/ -> /austin/index.html
    else if (pathname.endsWith('/') && pathname !== '/') {
      pathname = `${pathname}index.html`;
    }

    // Try to fetch the static asset
    try {
      const assetRequest = new Request(new URL(pathname, request.url).toString(), request);
      const response = await env.ASSETS.fetch(assetRequest);

      if (response.status === 404) {
        // Return custom 404 page
        const notFoundHtml = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Not Found | PawGrooming</title>
    <style>
        body {
            font-family: 'Nunito', sans-serif;
            background: linear-gradient(135deg, #fff8dc 0%, #e6e6fa 100%);
            color: #2c2c2c;
            text-align: center;
            padding: 2rem;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .container {
            max-width: 600px;
            background: white;
            padding: 3rem;
            border-radius: 24px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        }
        h1 { color: #2d5016; margin-bottom: 1rem; }
        .emoji { font-size: 4rem; margin-bottom: 1rem; }
        .back-link {
            display: inline-block;
            margin-top: 2rem;
            padding: 1rem 2rem;
            background: linear-gradient(135deg, #a8c090 0%, #87ceeb 100%);
            color: white;
            text-decoration: none;
            border-radius: 16px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">🐕</div>
        <h1>Page Not Found</h1>
        <p>Sorry, we couldn't find the page you're looking for.</p>
        <p>Let's get you back to finding great pet groomers!</p>
        <a href="/" class="back-link">🏠 Back to Home</a>
    </div>
</body>
</html>`;

        return new Response(notFoundHtml, {
          status: 404,
          headers: { 'Content-Type': 'text/html' },
        });
      }

      // Add security and performance headers
      const headers = new Headers(response.headers);
      headers.set('X-Content-Type-Options', 'nosniff');
      headers.set('X-Frame-Options', 'DENY');
      headers.set('X-XSS-Protection', '1; mode=block');
      headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
      headers.set('Cache-Control', 'public, max-age=86400');

      return new Response(response.body, {
        status: response.status,
        headers,
      });

    } catch (error) {
      return new Response('Internal Server Error', { status: 500 });
    }
  },
};