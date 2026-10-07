-- ============================================================
-- TAXREADY BOOKS SUPABASE SETUP
-- Paste this whole file into Supabase > SQL Editor > New query.
-- ============================================================

create extension if not exists pgcrypto;

-- -----------------------------
-- Profiles / client accounts
-- -----------------------------
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text,
  role text not null default 'client' check (role in ('client','admin')),
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, full_name, role)
  values (new.id, coalesce(new.raw_user_meta_data->>'full_name',''), 'client')
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
after insert on auth.users
for each row execute procedure public.handle_new_user();

-- Users can see/update their own profile.
create policy "profiles_select_own"
on public.profiles for select
to authenticated
using (id = auth.uid() or exists (
  select 1 from public.profiles p where p.id=auth.uid() and p.role='admin'
));

create policy "profiles_update_own"
on public.profiles for update
to authenticated
using (id = auth.uid())
with check (id = auth.uid());

-- Admins can manage profiles.
create policy "profiles_admin_all"
on public.profiles for all
to authenticated
using (exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin'))
with check (exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin'));

-- -----------------------------
-- Public reviews
-- -----------------------------
create table if not exists public.reviews (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(name) between 1 and 80),
  email text not null,
  rating integer not null check (rating between 1 and 5),
  comment text not null check (char_length(comment) between 1 and 1000),
  approved boolean not null default false,
  created_at timestamptz not null default now()
);

alter table public.reviews enable row level security;

create policy "public_read_approved_reviews"
on public.reviews for select
to anon, authenticated
using (approved = true);

create policy "public_submit_reviews"
on public.reviews for insert
to anon, authenticated
with check (
  char_length(name) between 1 and 80
  and char_length(email) between 3 and 160
  and rating between 1 and 5
  and char_length(comment) between 1 and 1000
  and approved = false
);

create policy "admin_manage_reviews"
on public.reviews for all
to authenticated
using (exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin'))
with check (exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin'));

-- -----------------------------
-- Client documents
-- -----------------------------
create table if not exists public.documents (
  id uuid primary key default gen_random_uuid(),
  client_id uuid not null references public.profiles(id) on delete cascade,
  title text not null,
  description text,
  storage_path text not null,
  created_at timestamptz not null default now()
);

alter table public.documents enable row level security;

create policy "client_read_own_documents"
on public.documents for select
to authenticated
using (
  client_id = auth.uid()
  or exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin')
);

create policy "admin_manage_documents"
on public.documents for all
to authenticated
using (exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin'))
with check (exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin'));

-- -----------------------------
-- Portal messages
-- -----------------------------
create table if not exists public.messages (
  id uuid primary key default gen_random_uuid(),
  client_id uuid not null references public.profiles(id) on delete cascade,
  sender_role text not null check (sender_role in ('client','admin')),
  body text not null check (char_length(body) between 1 and 2000),
  created_at timestamptz not null default now()
);

alter table public.messages enable row level security;

create policy "client_read_own_messages"
on public.messages for select
to authenticated
using (
  client_id = auth.uid()
  or exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin')
);

create policy "client_send_own_messages"
on public.messages for insert
to authenticated
with check (client_id = auth.uid() and sender_role='client');

create policy "admin_manage_messages"
on public.messages for all
to authenticated
using (exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin'))
with check (exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin'));

-- -----------------------------
-- Private document storage
-- -----------------------------
insert into storage.buckets (id, name, public)
values ('client-documents','client-documents',false)
on conflict (id) do nothing;

create policy "clients_read_own_document_files"
on storage.objects for select
to authenticated
using (
  bucket_id='client-documents'
  and (
    (storage.foldername(name))[1] = auth.uid()::text
    or exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin')
  )
);

create policy "admins_insert_document_files"
on storage.objects for insert
to authenticated
with check (
  bucket_id='client-documents'
  and exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin')
);

create policy "admins_update_document_files"
on storage.objects for update
to authenticated
using (
  bucket_id='client-documents'
  and exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin')
)
with check (
  bucket_id='client-documents'
  and exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin')
);

create policy "admins_delete_document_files"
on storage.objects for delete
to authenticated
using (
  bucket_id='client-documents'
  and exists (select 1 from public.profiles p where p.id=auth.uid() and p.role='admin')
);

-- ============================================================
-- AFTER you create your admin account, run this:
--
-- update public.profiles
-- set role='admin'
-- where id = (select id from auth.users where email='YOUR-ADMIN-EMAIL');
--
-- Replace YOUR-ADMIN-EMAIL with the email you used for the admin account.
-- ============================================================


-- ============================================================
-- CLIENT FILE UPLOAD SUPPORT
-- Run this section in Supabase SQL Editor after the original setup.
-- ============================================================

create policy "client_insert_own_documents"
on public.documents for insert
to authenticated
with check (client_id = auth.uid());

create policy "clients_insert_own_document_files"
on storage.objects for insert
to authenticated
with check (
  bucket_id='client-documents'
  and (storage.foldername(name))[1] = auth.uid()::text
);

-- Keep messages and documents available to the portal in real time.
alter publication supabase_realtime add table public.messages;
alter publication supabase_realtime add table public.documents;
