-- Migration: 00005_n8n_crawler_schema
-- Description: Creates the unified content schema (content_items) and system health logs for n8n crawlers.

-- 1. Create content_items table for unified crawler data (GitHub, Arxiv, Blogs)
CREATE TABLE IF NOT EXISTS public.content_items (
    id UUID DEFAULT extensions.gen_random_uuid() PRIMARY KEY,
    source_platform TEXT NOT NULL, -- e.g., 'github', 'arxiv', 'blog'
    source_id TEXT NOT NULL, -- Unique ID from the source platform (e.g., github repo id)
    type TEXT NOT NULL, -- e.g., 'repository', 'article', 'issue', 'pr'
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT, -- Markdown or plain text content / abstract
    author JSONB, -- { name: string, url?: string, avatar_url?: string }
    tags TEXT[] DEFAULT '{}'::TEXT[],
    metadata JSONB DEFAULT '{}'::JSONB, -- Specific data like stars, arxiv categories, etc.
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    -- Ensure we don't duplicate items from the same source
    UNIQUE(source_platform, source_id)
);

-- Indéxation pour les recherches et les filtres
CREATE INDEX IF NOT EXISTS content_items_source_platform_idx ON public.content_items(source_platform);
CREATE INDEX IF NOT EXISTS content_items_type_idx ON public.content_items(type);
CREATE INDEX IF NOT EXISTS content_items_published_at_idx ON public.content_items(published_at DESC);

-- Enable RLS
ALTER TABLE public.content_items ENABLE ROW LEVEL SECURITY;

-- Policy: Everyone can read content items
CREATE POLICY "Content items are viewable by everyone" 
ON public.content_items FOR SELECT 
USING (true);

-- Policy: Only service_role can insert/update/delete (used by n8n)
CREATE POLICY "Service role can manage content items" 
ON public.content_items FOR ALL 
USING (current_setting('request.jwt.claims', true)::jsonb ->> 'role' = 'service_role');


-- 2. Create system_health_logs for n8n workflows monitoring
CREATE TABLE IF NOT EXISTS public.system_health_logs (
    id UUID DEFAULT extensions.gen_random_uuid() PRIMARY KEY,
    service TEXT NOT NULL, -- e.g., 'n8n_github_crawler', 'n8n_arxiv_crawler'
    status TEXT NOT NULL CHECK (status IN ('info', 'warning', 'error', 'critical')),
    message TEXT NOT NULL,
    details JSONB DEFAULT '{}'::JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Index for querying logs
CREATE INDEX IF NOT EXISTS system_health_logs_service_status_idx ON public.system_health_logs(service, status);
CREATE INDEX IF NOT EXISTS system_health_logs_created_at_idx ON public.system_health_logs(created_at DESC);

-- Enable RLS
ALTER TABLE public.system_health_logs ENABLE ROW LEVEL SECURITY;

-- Policy: Authenticated users can read health logs (potentially restricted to admins later)
CREATE POLICY "Authenticated users can view health logs" 
ON public.system_health_logs FOR SELECT 
TO authenticated 
USING (true);

-- Policy: Only service_role can insert logs (used by n8n or Edge Functions)
CREATE POLICY "Service role can insert health logs" 
ON public.system_health_logs FOR INSERT 
WITH CHECK (current_setting('request.jwt.claims', true)::jsonb ->> 'role' = 'service_role');


-- 3. Update the updated_at trigger for content_items
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc'::text, now());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_content_items_updated_at ON public.content_items;
CREATE TRIGGER set_content_items_updated_at
    BEFORE UPDATE ON public.content_items
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();

-- Add n8n schema if it doesn't exist to isolate its internal workings (optional but recommended in docs)
CREATE SCHEMA IF NOT EXISTS n8n;
-- Grant usage to authenticator and postgres roles
GRANT USAGE ON SCHEMA n8n TO postgres, authenticated, anon, service_role;
