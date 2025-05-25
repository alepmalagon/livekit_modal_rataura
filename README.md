# LiveKit Modal Rataura

A proof-of-concept generic LiveKit 1.0 agent whose worker runs in [Modal](https://modal.com). This project demonstrates how to create a LiveKit agent using the Gemini RealtimeModel.

## Prerequisites

To run this project, you'll need:

1. A [LiveKit](https://livekit.io) account
2. A [Modal](https://modal.com) account
3. A [Google Cloud](https://cloud.google.com) account with access to the Gemini API

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment variables in a `.env` file:
   ```
   LIVEKIT_URL=your_livekit_url
   LIVEKIT_API_KEY=your_livekit_api_key
   LIVEKIT_API_SECRET=your_livekit_api_secret
   GOOGLE_API_KEY=your_google_api_key
   ```

3. Set up Modal:
   ```bash
   modal setup
   ```

## Running the Agent

To run the agent:

```bash
modal run app/app.py
```

## How It Works

This project uses:
- LiveKit Agents 1.0 for creating and managing the agent
- Modal for serverless deployment
- Google's Gemini RealtimeModel for natural, human-like voice conversations

The agent connects to a LiveKit room, waits for participants to join, and then engages in conversation using the Gemini RealtimeModel.

