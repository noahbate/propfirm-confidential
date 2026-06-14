export const dynamic = 'force-dynamic';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export async function GET() {
  try {
    const res = await fetch(`${BACKEND_URL}/api/prop-firms`, { cache: 'no-store' });
    if (!res.ok) return new Response(JSON.stringify([]), { status: 200, headers: { 'content-type': 'application/json' } });
    const data = await res.json();
    return new Response(JSON.stringify(data), { status: 200, headers: { 'content-type': 'application/json' } });
  } catch (err) {
    return new Response(JSON.stringify([]), { status: 200, headers: { 'content-type': 'application/json' } });
  }
}
