<<<<<<< HEAD
This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
=======
A modern **Email Wake-Up Agent** with a complete full-stack implementation designed to simulate an autonomous recruiting assistant that can initiate conversations, manage negotiations, and schedule calls with prospects.

---

## Backend (FastAPI)

The backend is built using **FastAPI** and is responsible for handling the entire AI-driven email workflow. It includes:

* **CORS-enabled FastAPI server** configured for frontend communication (localhost:3000)
* **SQLite database** storing:

  * Prospects
  * Threads
  * Messages (full conversation history)

### Core Email Processing Pipeline:

1. Incoming email is received via API
2. AI service classifies intent (interested, negotiating, reschedule, decline, etc.)
3. Message is saved into thread history
4. AI generates contextual reply using a Gemini-based service
5. Reply is sent via SMTP email service
6. AI response is also stored in the database for memory continuity

---

## Backend APIs

### Prospects:

* `POST /threads/prospects` → Create prospect
* `GET /threads/prospects` → List prospects
* `GET /threads/prospects/{id}` → Get prospect details

### Threads:

* `POST /threads` → Create conversation thread
* `GET /threads` → List all threads
* `GET /threads/{id}` → Get full thread history
* `PATCH /threads/{id}` → Update thread state (active/booked/cancelled/rescheduled)

---

## Frontend (Next.js)

The frontend is built using **Next.js** with a modern dark-themed dashboard UI.

### Features:

* Create and manage prospects
* Create and track conversation threads
* Input incoming email content to trigger AI responses
* View AI-generated replies in real time
* Display full thread history with sender labels
* Status panel showing current thread state (active, booked, cancelled, etc.)

The UI is fully responsive, clean, and production-ready, and successfully builds using `npm run build`.

---

## End-to-End Flow

The system supports a complete autonomous loop:

1. Create prospect
2. Start a thread
3. Send incoming email content
4. AI classifies intent
5. System generates contextual reply
6. Email is sent via SMTP
7. Full conversation is stored and displayed in UI

---

## Outcome

This project demonstrates a **stateful AI email agent system** capable of maintaining memory, handling negotiation, and managing rescheduling flows while providing a full-stack dashboard for monitoring conversations.
>>>>>>> c7212aadee85da79e5e5d48409eee152c8cbb9a6
