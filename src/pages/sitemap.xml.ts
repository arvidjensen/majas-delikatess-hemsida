const SITE_URL = (import.meta.env.PUBLIC_SITE_URL ?? 'https://majasdelikatess.se').replace(/\/$/, '');

export const prerender = true;

export function GET() {
  const lastmod = '2026-02-28';
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${SITE_URL}/</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8'
    }
  });
}
