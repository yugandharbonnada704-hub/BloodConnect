-- Blood Donor Management System Database Schema
-- Run this in the Supabase SQL Editor as a superuser

-- 1. Enable UUID Extension
create extension if not exists "uuid-ossp";

-- 2. Drop existing triggers and functions if they exist
drop trigger if exists on_auth_user_created on auth.users;
drop function if exists public.handle_new_user();

-- 3. Create Profiles Table (extends auth.users)
create table if not exists public.profiles (
    id uuid references auth.users on delete cascade primary key,
    full_name text not null,
    email text not null unique,
    phone_number text,
    role text not null default 'donor' check (role in ('donor', 'admin')),
    age integer,
    gender text check (gender in ('Male', 'Female', 'Other')),
    blood_group text check (blood_group in ('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-')),
    country text not null default 'India',
    state text,
    district text,
    city text,
    village text,
    address text,
    availability_status text not null default 'Available' check (availability_status in ('Available', 'Not Available')),
    last_donation_date date,
    verification_status text not null default 'pending' check (verification_status in ('pending', 'verified', 'rejected')),
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 4. Create Locations Lookup Table
create table if not exists public.locations (
    id uuid default gen_random_uuid() primary key,
    country text not null default 'India',
    state text not null,
    district text not null,
    city text not null,
    village text,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 5. Create Blood Requests Table
create table if not exists public.blood_requests (
    id uuid default gen_random_uuid() primary key,
    user_id uuid references auth.users(id) on delete cascade not null,
    patient_name text not null,
    blood_group text not null check (blood_group in ('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-')),
    hospital_name text not null,
    country text not null default 'India',
    state text not null,
    district text not null,
    city text not null,
    village text,
    contact_number text not null,
    units_required integer not null default 1 check (units_required > 0),
    urgency_level text not null check (urgency_level in ('Critical', 'High', 'Medium', 'Low')),
    status text not null default 'Pending' check (status in ('Pending', 'Approved', 'Fulfilled', 'Cancelled')),
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 6. Create Blood Request Status History Table
create table if not exists public.blood_request_status_history (
    id uuid default gen_random_uuid() primary key,
    request_id uuid references public.blood_requests(id) on delete cascade not null,
    status text not null check (status in ('Pending', 'Approved', 'Fulfilled', 'Cancelled')),
    updated_by uuid references auth.users(id) on delete set null,
    notes text,
    changed_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 7. Create Donation History Table
create table if not exists public.donation_history (
    id uuid default gen_random_uuid() primary key,
    user_id uuid references auth.users(id) on delete cascade not null,
    donation_date date not null,
    hospital_name text not null,
    units_donated integer not null default 1 check (units_donated > 0),
    donation_type text not null check (donation_type in ('Voluntary', 'Emergency', 'Camp')),
    notes text,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Enable RLS for security (will bypass using service key in Flask, but keeps DB safe)
alter table public.profiles enable row level security;
alter table public.locations enable row level security;
alter table public.blood_requests enable row level security;
alter table public.blood_request_status_history enable row level security;
alter table public.donation_history enable row level security;

-- Policy to allow all operations for postgres admin (e.g., service role key)
create policy "Allow service key bypass" on public.profiles for all using (true) with check (true);
create policy "Allow service key bypass locations" on public.locations for all using (true) with check (true);
create policy "Allow service key bypass requests" on public.blood_requests for all using (true) with check (true);
create policy "Allow service key bypass history" on public.blood_request_status_history for all using (true) with check (true);
create policy "Allow service key bypass donation" on public.donation_history for all using (true) with check (true);

-- 8. Trigger Function to auto-create profile on Auth User Signup
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, full_name, email, phone_number, role, verification_status)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'full_name', ''),
    new.email,
    new.phone,
    coalesce(new.raw_user_meta_data->>'role', 'donor'),
    'pending'
  );
  return new;
end;
$$ language plpgsql security definer;

-- Trigger binding
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- 9. Insert Sample Hierarchical Locations
insert into public.locations (state, district, city, village) values
('Maharashtra', 'Mumbai', 'Mumbai', 'Worli'),
('Maharashtra', 'Mumbai', 'Mumbai', 'Bandra'),
('Maharashtra', 'Mumbai', 'Mumbai', 'Andheri'),
('Maharashtra', 'Pune', 'Pune', 'Shivaji Nagar'),
('Maharashtra', 'Pune', 'Pune', 'Kothrud'),
('Karnataka', 'Bangalore Urban', 'Bangalore', 'Koramangala'),
('Karnataka', 'Bangalore Urban', 'Bangalore', 'Indiranagar'),
('Karnataka', 'Bangalore Urban', 'Bangalore', 'Whitefield'),
('Delhi', 'New Delhi', 'Delhi', 'Connaught Place'),
('Delhi', 'New Delhi', 'Delhi', 'Karol Bagh'),
('Telangana', 'Hyderabad', 'Hyderabad', 'Gachibowli'),
('Telangana', 'Hyderabad', 'Hyderabad', 'Jubilee Hills'),
('Tamil Nadu', 'Chennai', 'Chennai', 'Adyar'),
('Tamil Nadu', 'Chennai', 'Chennai', 'Velachery'),
('West Bengal', 'Kolkata', 'Kolkata', 'Salt Lake');
