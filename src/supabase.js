import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = "https://zqiyxgwzxjsbdcbzdnyr.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpxaXl4Z3d6eGpzYmRjYnpkbnlyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0Mjc1MTMsImV4cCI6MjA3NTAwMzUxM30.N_3LhHt-AlkjvBK81jVfQcUO1hyst_WsGHnc30Dq0Qw";

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
