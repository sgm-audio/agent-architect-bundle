---
name: deployment-ops
description: Website deployment, hosting configuration, CI/CD setup, and infrastructure management. Use when deploying to Vercel/Netlify, setting up GitHub Actions, configuring domains, setting up CDN, managing environment variables, or troubleshooting production issues.
---

# Deployment & Operations Skill

## Platform Recommendations

### Vercel (Recommended for Next.js)
- Zero-config deployment, automatic previews for PRs, edge functions, analytics included

### Netlify (Recommended for static sites)
- Excellent form handling, edge functions, split testing, generous free tier

### Cloudflare Pages
- Unlimited bandwidth, edge deployment, workers integration, best for global performance

## Deployment Checklist

### Pre-deployment
- [ ] Environment variables configured
- [ ] Build passes locally (`npm run build`)
- [ ] TypeScript strict mode passes
- [ ] Tests passing
- [ ] Lighthouse score > 90
- [ ] Robots.txt configured
- [ ] Sitemap generated
- [ ] Favicon and OG images ready
- [ ] Analytics script added

### Domain Setup
1. Purchase domain (Namecheap/Cloudflare)
2. Add domain to hosting platform
3. Update DNS records (A/CNAME)
4. Enable HTTPS (auto on Vercel/Netlify)
5. Configure www redirect
6. Set up email forwarding if needed

### Environment Variables
```env
NEXT_PUBLIC_SITE_URL=https://example.com
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
RESEND_API_KEY=re_xxxxxxxx
DATABASE_URL=
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=
```

## GitHub Actions CI/CD

```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run test
      - run: npm run build
```

## Performance Monitoring

```tsx
import { GoogleAnalytics } from "@next/third-parties/google";
import { SpeedInsights } from "@vercel/speed-insights/next";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>{children}</body>
      <GoogleAnalytics gaId={process.env.NEXT_PUBLIC_GA_ID!} />
      <SpeedInsights />
    </html>
  );
}
```

## Backup & Recovery

- Git repository is the source of truth
- Database backups (if applicable): Daily automated
- Asset backups: Store originals in cloud storage
- Document rollback procedure
