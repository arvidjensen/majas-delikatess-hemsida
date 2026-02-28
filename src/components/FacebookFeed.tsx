import { useState, useEffect, useRef } from 'react';

/* ═══════════════════════════════════════════════════════════
   FacebookFeed — Visar inlägg i Maja's Delikatess apoteksstil.

   Två lägen:
   1. Statiska inlägg (staticPosts prop) — visas direkt
   2. Facebook Graph API (accessToken prop) — hämtar dynamiskt

   Om accessToken finns försöker den hämta från API.
   Annars (eller vid fel) faller den tillbaka på staticPosts.
   ═══════════════════════════════════════════════════════════ */

interface FacebookPost {
  id: string;
  message?: string;
  full_picture?: string;
  created_time: string;
  permalink_url: string;
}

interface Props {
  pageId: string;
  accessToken?: string;
  staticPosts?: FacebookPost[];
}

// ───── Helpers ─────

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('sv-SE', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

function truncateText(text: string, maxLen: number): string {
  if (text.length <= maxLen) return text;
  const cut = text.substring(0, maxLen);
  const lastSpace = cut.lastIndexOf(' ');
  return (lastSpace > 0 ? cut.substring(0, lastSpace) : cut) + '\u2026';
}

// ───── Post Card ─────

function PostCard({ post, index, visible }: {
  post: FacebookPost;
  index: number;
  visible: boolean;
}) {
  const [hovered, setHovered] = useState(false);
  const [imgError, setImgError] = useState(false);
  const [baseHeight, setBaseHeight] = useState<number | null>(null);
  const cardRef = useRef<HTMLAnchorElement>(null);

  const hasImage = !!post.full_picture && !imgError;
  const fullText = post.message || '';
  const shortText = truncateText(fullText, hasImage ? 350 : 500);
  const isTruncated = shortText !== fullText;
  const showExpanded = hovered && isTruncated;

  // Mät kortets höjd i trunkerat läge (en gång)
  useEffect(() => {
    if (cardRef.current && baseHeight === null && visible) {
      setBaseHeight(cardRef.current.offsetHeight);
    }
  });

  const renderText = (text: string) =>
    text.split('\n').map((line, i) => (
      <span key={i}>
        {i > 0 && <br />}
        {line}
      </span>
    ));

  return (
    /* Wrapper behåller plats i gridet — stretch fyller radhöjden */
    <div
      style={{
        position: 'relative',
        minHeight: baseHeight ? `${baseHeight}px` : undefined,
        display: 'flex',
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <a
        ref={cardRef}
        href={post.permalink_url}
        target="_blank"
        rel="noopener noreferrer"
        style={{
          background: 'var(--cream-light)',
          border: '1px solid var(--brass)',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column' as const,
          width: '100%',
          textDecoration: 'none',
          opacity: visible ? 1 : 0,
          transform: visible
            ? (hovered ? 'translateY(-5px)' : 'translateY(0)')
            : 'translateY(24px) scale(0.97)',
          transition: 'opacity 0.7s ease, transform 0.5s ease, box-shadow 0.4s ease',
          transitionDelay: visible && !hovered ? `${index * 0.18}s` : '0s',
          boxShadow: showExpanded
            ? '0 24px 64px rgba(44,30,18,0.28), 0 8px 24px rgba(160,120,76,0.15)'
            : hovered
              ? '0 16px 48px rgba(44,30,18,0.18), 0 4px 12px rgba(160,120,76,0.1)'
              : '0 2px 8px rgba(44,30,18,0.06)',
          /* Vid expand: sväva ut som overlay */
          ...(showExpanded ? {
            position: 'absolute' as const,
            top: 0,
            left: 0,
            right: 0,
            zIndex: 10,
          } : {
            position: 'relative' as const,
            zIndex: 1,
          }),
        }}
      >
        {/* Inner brass border */}
        <div style={{
          position: 'absolute',
          top: '4px', left: '4px', right: '4px', bottom: '4px',
          border: '1px solid rgba(160,120,76,0.3)',
          pointerEvents: 'none',
          zIndex: 2,
          transition: 'border-color 0.6s ease',
          borderColor: hovered ? 'var(--brass)' : 'rgba(160,120,76,0.3)',
        }} />

        {/* Image */}
        {hasImage && (
          <div style={{ overflow: 'hidden', position: 'relative' }}>
            <img
              src={post.full_picture}
              alt=""
              onError={() => setImgError(true)}
              style={{
                width: '100%',
                height: '210px',
                objectFit: 'cover',
                display: 'block',
                filter: 'sepia(0.08) brightness(0.97)',
                transform: hovered ? 'scale(1.06)' : 'scale(1)',
                transition: 'transform 0.9s cubic-bezier(0.25, 0.46, 0.45, 0.94)',
              }}
            />
            <div style={{
              position: 'absolute',
              bottom: 0, left: 0, right: 0,
              height: '50px',
              background: 'linear-gradient(to top, var(--cream-light), transparent)',
              pointerEvents: 'none',
            }} />
          </div>
        )}

        {/* Content */}
        <div style={{
          padding: hasImage ? '1.2rem 1.6rem 1.6rem' : '2rem 1.8rem 1.8rem',
          position: 'relative',
          zIndex: 1,
          flex: 1,
          display: 'flex',
          flexDirection: 'column' as const,
        }}>
          {/* Text-only: decorative quotation mark */}
          {!hasImage && (
            <div style={{
              fontFamily: 'var(--font-display)',
              fontSize: '3.5rem',
              lineHeight: 1,
              color: 'var(--brass)',
              opacity: 0.25,
              marginBottom: '-0.2rem',
              marginTop: '-0.5rem',
            }}>
              {'\u201C'}
            </div>
          )}

          {/* Date */}
          <span style={{
            fontFamily: 'var(--font-script)',
            fontSize: '1.3rem',
            color: 'var(--brass)',
            display: 'block',
            marginBottom: '0.6rem',
            textShadow: '0 0 0.6px currentColor, 0 0 0.6px currentColor',
            WebkitTextStroke: '0.3px currentColor',
          }}>
            {formatDate(post.created_time)}
          </span>

          {/* Brass divider */}
          <div style={{
            height: '1px',
            background: 'var(--brass)',
            maxWidth: '36px',
            marginBottom: '0.9rem',
            opacity: 0.7,
          }} />

          {/* Post text */}
          <p style={{
            fontFamily: 'var(--font-body)',
            fontSize: hasImage ? '0.95rem' : '1.05rem',
            lineHeight: 1.75,
            color: 'var(--walnut-medium)',
            margin: 0,
            marginBlockEnd: '1.2rem',
          }}>
            {showExpanded ? renderText(fullText) : renderText(shortText)}
          </p>

          {/* Fade hint when truncated */}
          {isTruncated && !showExpanded && (
            <div style={{
              height: '20px',
              marginTop: '-32px',
              marginBottom: '12px',
              background: 'linear-gradient(to top, var(--cream-light), transparent)',
              position: 'relative',
              pointerEvents: 'none',
            }} />
          )}

          {/* Read more — alltid i botten */}
          <span style={{
            fontFamily: 'var(--font-display)',
            fontSize: '0.65rem',
            letterSpacing: '0.12em',
            textTransform: 'uppercase' as const,
            color: hovered ? 'var(--brass)' : 'var(--brass-dark)',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.4rem',
            transition: 'color 0.3s ease',
            marginTop: 'auto',
            paddingTop: '0.5rem',
          }}>
            L&auml;s mer p&aring; Facebook
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </span>
        </div>
      </a>
    </div>
  );
}

// ───── Loading Skeleton ─────

function LoadingSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {[0, 1, 2].map(i => (
        <div key={i} style={{
          background: 'var(--cream-light)',
          border: '1px solid var(--brass)',
          position: 'relative',
          overflow: 'hidden',
        }}>
          <div style={{
            position: 'absolute',
            top: '4px', left: '4px', right: '4px', bottom: '4px',
            border: '1px solid rgba(160,120,76,0.2)',
            pointerEvents: 'none',
            zIndex: 2,
          }} />
          <div style={{
            height: '210px',
            background: 'linear-gradient(90deg, rgba(240,232,216,0.6) 25%, rgba(247,242,232,0.9) 50%, rgba(240,232,216,0.6) 75%)',
            backgroundSize: '200% 100%',
            animation: 'fb-shimmer 2.5s infinite ease-in-out',
            animationDelay: `${i * 0.3}s`,
          }} />
          <div style={{ padding: '1.4rem 1.6rem 1.8rem' }}>
            <div style={{
              height: '12px', width: '40%', borderRadius: '2px', marginBottom: '0.9rem',
              background: 'linear-gradient(90deg, rgba(240,232,216,0.6) 25%, rgba(247,242,232,0.9) 50%, rgba(240,232,216,0.6) 75%)',
              backgroundSize: '200% 100%',
              animation: 'fb-shimmer 2.5s infinite ease-in-out',
              animationDelay: `${i * 0.3 + 0.15}s`,
            }} />
            <div style={{ height: '1px', background: 'rgba(160,120,76,0.15)', maxWidth: '36px', marginBottom: '0.9rem' }} />
            {[95, 80, 55].map((w, j) => (
              <div key={j} style={{
                height: '10px', width: `${w}%`, borderRadius: '2px', marginBottom: '0.55rem',
                background: 'linear-gradient(90deg, rgba(240,232,216,0.6) 25%, rgba(247,242,232,0.9) 50%, rgba(240,232,216,0.6) 75%)',
                backgroundSize: '200% 100%',
                animation: 'fb-shimmer 2.5s infinite ease-in-out',
                animationDelay: `${i * 0.3 + 0.2 + j * 0.08}s`,
              }} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
//  Main Component
// ═══════════════════════════════════════════════════════════

export default function FacebookFeed({ pageId, accessToken, staticPosts }: Props) {
  const [posts, setPosts] = useState<FacebookPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [visible, setVisible] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Om vi har en access token, försök hämta från API
    if (accessToken) {
      fetch(
        `https://graph.facebook.com/v21.0/${pageId}/posts?fields=message,full_picture,created_time,permalink_url&access_token=${accessToken}&limit=9`
      )
        .then(res => res.json())
        .then(data => {
          if (data.data) {
            const filtered = data.data
              .filter((p: FacebookPost) => p.message)
              .slice(0, 3);
            if (filtered.length > 0) {
              setPosts(filtered);
              setLoading(false);
              return;
            }
          }
          // API gav inget — fallback till statiska
          if (staticPosts && staticPosts.length > 0) {
            setPosts(staticPosts.slice(0, 3));
          }
          setLoading(false);
        })
        .catch(() => {
          // Nätverksfel — fallback till statiska
          if (staticPosts && staticPosts.length > 0) {
            setPosts(staticPosts.slice(0, 3));
          }
          setLoading(false);
        });
    } else if (staticPosts && staticPosts.length > 0) {
      // Ingen token — använd statiska direkt (ingen laddning)
      setPosts(staticPosts.slice(0, 3));
      setLoading(false);
    } else {
      // Varken token eller statiska inlägg
      setLoading(false);
    }
  }, [pageId, accessToken, staticPosts]);

  // Staggered reveal via IntersectionObserver
  useEffect(() => {
    if (loading || posts.length === 0) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (containerRef.current) {
      observer.observe(containerRef.current);
    }

    return () => observer.disconnect();
  }, [loading, posts]);

  return (
    <div ref={containerRef}>
      <style>{`
        @keyframes fb-shimmer {
          0% { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
      `}</style>

      {loading && <LoadingSkeleton />}

      {!loading && posts.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {posts.map((post, i) => (
            <PostCard key={post.id} post={post} index={i} visible={visible} />
          ))}
        </div>
      )}

      {!loading && posts.length === 0 && (
        <div style={{
          background: 'var(--cream-light)',
          border: '1px solid var(--brass)',
          position: 'relative',
          padding: '3.5rem 2rem',
          textAlign: 'center',
        }}>
          <div style={{
            position: 'absolute',
            top: '4px', left: '4px', right: '4px', bottom: '4px',
            border: '1px solid rgba(160,120,76,0.3)',
            pointerEvents: 'none',
          }} />
          <div style={{ marginBottom: '1.5rem', color: 'var(--brass)', opacity: 0.5 }}>
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24"
              fill="currentColor" style={{ margin: '0 auto' }}>
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
            </svg>
          </div>
          <p style={{
            fontFamily: 'var(--font-body)',
            fontSize: '1.1rem',
            lineHeight: 1.7,
            color: 'var(--walnut-medium)',
            maxWidth: '420px',
            margin: '0 auto 1.8rem',
          }}>
            F&ouml;lj med i vad som h&auml;nder hos oss &ndash; nyheter, erbjudanden och smakupplevelser publiceras l&ouml;pande p&aring; v&aring;r Facebook.
          </p>
          <a
            href={`https://www.facebook.com/${pageId}`}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.6rem',
              padding: '0.85rem 1.8rem',
              border: '1px solid var(--brass)',
              color: 'var(--brass-dark)',
              fontFamily: 'var(--font-display)',
              fontWeight: 400,
              fontSize: '0.75rem',
              letterSpacing: '0.1em',
              textDecoration: 'none',
              textTransform: 'uppercase' as const,
              background: 'transparent',
            }}
          >
            Bes&ouml;k oss p&aring; Facebook
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </a>
        </div>
      )}
    </div>
  );
}
