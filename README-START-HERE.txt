TAXREADY BOOKS — START HERE
==============================

You said you are new to this, so follow these steps in order.

WHAT IS IN THIS FOLDER
----------------------
1. index.html
   Your existing TaxReady Books website, preserved, with the Reviews area added.

2. client-portal.html
   Private client sign-in, documents, messages, and profile.

3. reviews-admin.html
   Private page for you to approve/delete public reviews.

4. supabase-setup.sql
   Creates the database tables, security rules, and private document storage.

IMPORTANT
---------
Do NOT delete your existing GitHub repository.

STEP 1 — GITHUB
---------------
Upload these files into the same GitHub repository as your website.

The main website file must be:
    index.html

The other files should sit beside it:
    client-portal.html
    reviews-admin.html

You can leave the SQL and README files in the repository too, or keep them on your computer.

STEP 2 — SUPABASE
-----------------
1. Go to Supabase and create/open your project.
2. Open SQL Editor.
3. Click New query.
4. Open supabase-setup.sql.
5. Copy everything in that file.
6. Paste it into Supabase SQL Editor.
7. Click Run.

STEP 3 — GET YOUR SUPABASE KEYS
--------------------------------
In Supabase, open:
Project Settings → API

Copy:
- Project URL
- Publishable/anon key (use the public browser key, NOT a service-role key)

You will paste those two values into THREE HTML files:
- index.html
- client-portal.html
- reviews-admin.html

Find:
    PASTE-YOUR-SUPABASE-URL-HERE

and replace it with your Project URL.

Find:
    PASTE-YOUR-SUPABASE-ANON-KEY-HERE

and replace it with your public anon/publishable key.

NEVER put a Supabase service_role/secret key into these HTML files.

STEP 4 — CREATE YOUR ADMIN ACCOUNT
-----------------------------------
Use Supabase Authentication → Users to create your owner/admin user.

Then in SQL Editor run:

update public.profiles
set role='admin'
where id = (select id from auth.users where email='YOUR-ADMIN-EMAIL');

Replace YOUR-ADMIN-EMAIL with your real admin email.

STEP 5 — CLIENT ACCOUNTS
------------------------
Clients can use client-portal.html to create an account.

Their account is automatically given the role "client".

STEP 6 — REVIEWS
----------------
Visitors use the Reviews section on index.html.

When somebody submits a review:
- it is saved privately in Supabase
- it is NOT public immediately
- you open reviews-admin.html
- sign in as your admin account
- click Approve
- then everybody can see that review on your website

STEP 7 — VERCEL
---------------
If your GitHub repository is already connected to Vercel, pushing/committing the files to GitHub should cause Vercel to redeploy automatically.

Your pages will be:
    yourdomain.com/
    yourdomain.com/client-portal.html
    yourdomain.com/reviews-admin.html

OPTIONAL
--------
You can add a visible "Client Portal" link to your website later.
The portal works even if you first visit its direct URL.

IF SOMETHING GOES WRONG
-----------------------
Most common causes:
1. Supabase URL/key was not pasted into all 3 HTML files.
2. supabase-setup.sql was not run completely.
3. Admin profile role was not changed to "admin".
4. The wrong Supabase key was used. Use the public anon/publishable key, never service_role.
