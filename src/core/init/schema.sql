CREATE TABLE public.formulas (
  version integer PRIMARY KEY,
  weights jsonb NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE public.receipts (
  id uuid PRIMARY KEY,
  student_id text NOT NULL,
  exam_id text NOT NULL,
  idempotency_key text NOT NULL,
  sequence integer NOT NULL CHECK (sequence >= 0),
  answers jsonb NOT NULL,
  status text NOT NULL DEFAULT 'pending',
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (student_id, exam_id, idempotency_key)
);
CREATE INDEX receipts_pending ON public.receipts (created_at) WHERE status = 'pending';
CREATE TABLE public.plugin_registry (
  name text PRIMARY KEY,
  enabled boolean NOT NULL DEFAULT false
);
INSERT INTO public.plugin_registry(name) VALUES ('qr');
CREATE TABLE public.attendance (
  student_id text NOT NULL,
  course_id text NOT NULL,
  code text NOT NULL,
  at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (student_id, course_id, code)
);
CREATE TABLE public.autosaves (
  student_id text NOT NULL,
  exam_id text NOT NULL,
  sequence integer NOT NULL CHECK (sequence >= 0),
  answers jsonb NOT NULL,
  updated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (student_id, exam_id)
);
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
