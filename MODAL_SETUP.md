# Modal Setup Guide

This guide explains how to set up Modal for deploying your LiveKit agent.

## 1. Install Modal

First, install the Modal CLI:

```bash
pip install modal
```

## 2. Authenticate with Modal

Run the following command to authenticate with Modal:

```bash
modal setup
```

This will open a browser window where you can log in to your Modal account.

## 3. Create Secrets in Modal

You need to create secrets in Modal to store your LiveKit and Google API credentials:

```bash
# Create LiveKit secrets
modal secret create livekit-secrets \
  LIVEKIT_URL=your_livekit_url \
  LIVEKIT_API_KEY=your_livekit_api_key \
  LIVEKIT_API_SECRET=your_livekit_api_secret

# Create Google secrets
modal secret create google-secrets \
  GOOGLE_API_KEY=your_google_api_key
```

Replace the placeholder values with your actual credentials.

## 4. Deploy Your Agent

Deploy your agent to Modal:

```bash
modal deploy app/app.py
```

This will deploy your LiveKit agent as a worker in Modal's cloud environment. The worker will connect to your LiveKit server and wait for participants to join.

## 5. Verify Deployment

After deployment, Modal will provide a URL where you can view your deployment status. You can also check the status in the Modal dashboard.

## 6. Test Your Agent

1. Go to the LiveKit dashboard > Sandbox > Voice assistant
2. Use the LiveKit frontend sandbox to test your agent
3. Your agent will automatically connect to the sandbox using your LiveKit URL

## Troubleshooting

If you encounter issues:

1. Check that your secrets are correctly set up in Modal
2. Verify that your LiveKit URL and API credentials are correct
3. Check the Modal logs for any error messages
4. Ensure your Google API key has access to the Gemini API

For more information, see the [Modal documentation](https://modal.com/docs) and [LiveKit Agents documentation](https://docs.livekit.io/agents/).

