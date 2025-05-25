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

   > **Note:** The requirements.txt file specifies pydantic 2.x as required by LiveKit Agents 1.0.

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

4. Add your secrets to Modal:
   ```bash
   modal secret create livekit-secrets LIVEKIT_URL=your_livekit_url LIVEKIT_API_KEY=your_livekit_api_key LIVEKIT_API_SECRET=your_livekit_api_secret
   modal secret create google-secrets GOOGLE_API_KEY=your_google_api_key
   ```

## Deploying the Agent

To deploy the agent to Modal:

```bash
# Deploy the agent to Modal
modal deploy app/app.py
```

This will deploy your LiveKit agent as a worker in Modal's cloud environment. The worker will connect to your LiveKit server and wait for participants to join.

## Running Locally for Testing

For local testing without deploying to Modal:

```bash
# Run the local example
python app/local_example.py
```

## How It Works

This project uses:
- LiveKit Agents 1.0 for creating and managing the agent
- Modal for serverless deployment
- Google's Gemini RealtimeModel for natural, human-like voice conversations

The agent connects to a LiveKit room, waits for participants to join, and then engages in conversation using the Gemini RealtimeModel.

## Testing Your Agent

1. Deploy your agent to Modal
2. Go to the LiveKit dashboard > Sandbox > Voice assistant
3. Use the LiveKit frontend sandbox to test your agent
4. Your agent will automatically connect to the sandbox using your LiveKit URL
