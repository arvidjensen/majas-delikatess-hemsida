const SITE_URL = (import.meta.env.PUBLIC_SITE_URL ?? 'https://majasdelikatess.se').replace(/\/$/, '');

export const prerender = true;

export function GET() {
  const body = `User-agent: *
Allow: /

Sitemap: ${SITE_URL}/sitemap.xml
`;

  return new Response(body, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8'
    }
  });
}
