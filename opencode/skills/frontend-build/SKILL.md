---
name: frontend-build
description: Modern frontend development with Next.js, React, TypeScript, and Tailwind CSS. Use when scaffolding projects, building components, implementing features, setting up routing, managing state, or optimizing performance. Covers project setup, component patterns, data fetching, form handling, animation, and deployment preparation.
---

# Frontend Build Skill

## Project Scaffolding

### Next.js + shadcn/ui Setup
```bash
npx create-next-app@latest project-name --typescript --tailwind --app --src-dir
npx shadcn@latest init
```

### Required Dependencies
```bash
npx shadcn add button card input label textarea select dialog sheet tabs accordion avatar badge separator skeleton switch toggle scroll-area dropdown-menu navigation-menu table
npm install framer-motion lucide-react react-hook-form zod @hookform/resolvers @tanstack/react-query zustand
```

## Component Patterns

### Page Section Component
```tsx
import { Button } from "@/components/ui/button";

interface HeroProps {
  title: string;
  subtitle: string;
  ctaText: string;
  ctaHref: string;
}

export function Hero({ title, subtitle, ctaText, ctaHref }: HeroProps) {
  return (
    <section className="relative py-20 lg:py-32">
      <div className="container mx-auto px-4 text-center">
        <h1 className="text-4xl font-bold tracking-tight lg:text-6xl">
          {title}
        </h1>
        <p className="mt-6 text-lg text-muted-foreground max-w-2xl mx-auto">
          {subtitle}
        </p>
        <Button asChild size="lg" className="mt-8">
          <a href={ctaHref}>{ctaText}</a>
        </Button>
      </div>
    </section>
  );
}
```

### Animated Section (Framer Motion)
```tsx
"use client";
import { motion } from "framer-motion";
import { ReactNode } from "react";

export function AnimatedSection({ children, className, delay = 0 }: {
  children: ReactNode; className?: string; delay?: number;
}) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.5, delay }}
      className={className}
    >
      {children}
    </motion.section>
  );
}
```

### API Route Handler
```tsx
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";

const contactSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  message: z.string().min(10),
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validated = contactSchema.parse(body);
    return NextResponse.json({ success: true });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({ error: "Validation failed", details: error.errors }, { status: 400 });
    }
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}
```

## Data Fetching Patterns

### Server Component Fetching
```tsx
async function getPosts() {
  const res = await fetch("https://api.example.com/posts", { next: { revalidate: 3600 } });
  if (!res.ok) throw new Error("Failed to fetch posts");
  return res.json();
}

export default async function BlogPage() {
  const posts = await getPosts();
  return <div>{posts.map((post: any) => <article key={post.id}><h2>{post.title}</h2></article>)}</div>;
}
```

### Client-Side with React Query
```tsx
import { useQuery } from "@tanstack/react-query";

export function usePosts() {
  return useQuery({
    queryKey: ["posts"],
    queryFn: async () => {
      const res = await fetch("/api/posts");
      if (!res.ok) throw new Error("Failed to fetch");
      return res.json();
    },
  });
}
```

## Animation Guidelines

- Use `transform` and `opacity` only (GPU-accelerated)
- Keep animations under 300ms for micro-interactions
- Use `layout` prop for layout animations
- Respect `prefers-reduced-motion`
- Stagger children with `staggerChildren: 0.1`

## Performance Checklist

- [ ] Images: Next.js Image with proper sizes
- [ ] Fonts: `next/font` with display: swap
- [ ] CSS: Tailwind purge working
- [ ] JS: Dynamic imports for heavy components
- [ ] API: Proper caching headers
- [ ] Build: Output export for static sites
