-- TAXREADY BOOKS: VIDEO CALL SETUP
-- Run this ONE TIME in Supabase > SQL Editor.

alter table public.profiles add column if not exists email text;

create table if not exists public.call_invites (
  id uuid primary key default gen_random_uuid(),
  client_id uuid not null references public.profiles(id) on delete cascade,
  room text not null,
  initiated_by text not null check (initiated_by in ('admin','client')),
  status text not null default 'pending' check (status in ('pending','joined','dismissed')),
  created_at timestamptz not null default now()
);

alter table public.call_invites enable row level security;

drop policy if exists "clients_read_own_call_invites" on public.call_invites;
create policy "clients_read_own_call_invites"
on public.call_invites for select to authenticated
using (client_id = auth.uid());

drop policy if exists "clients_update_own_call_invites" on public.call_invites;
create policy "clients_update_own_call_invites"
on public.call_invites for update to authenticated
using (client_id = auth.uid())
with check (client_id = auth.uid());

drop policy if exists "clients_create_own_call_invites" on public.call_invites;
create policy "clients_create_own_call_invites"
on public.call_invites for insert to authenticated
with check (client_id = auth.uid() and initiated_by = 'client');

drop policy if exists "admin_manage_call_invites" on public.call_invites;
create policy "admin_manage_call_invites"
on public.call_invites for all to authenticated
using (exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin'))
with check (exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin'));

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_publication_tables
    WHERE pubname='supabase_realtime'
      AND schemaname='public'
      AND tablename='call_invites'
  ) THEN
    ALTER PUBLICATION supabase_realtime ADD TABLE public.call_invites;
  END IF;
END $$;