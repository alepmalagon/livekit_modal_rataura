# Modal Setup Guide

This guide explains how to set up the necessary secrets in Modal for the LiveKit agent.

## Prerequisites

1. Make sure you have a Modal account and have installed the Modal CLI:
   ```bash
   pip install modal
   modal setup
   ```

2. Ensure you have the necessary API keys:
   - LiveKit URL, API Key, and API Secret
   - Google API Key for Gemini

## Setting Up Secrets in Modal

### LiveKit Secrets

Create a secret for LiveKit credentials:

```bash
modal secret create livekit-secrets \
  LIVEKIT_URL=wss://your-livekit-instance.livekit.cloud \
  LIVEKIT_API_KEY=your_api_key \
  LIVEKIT_API_SECRET=your_api_secret
```

### Google Secrets

Create a secret for Google API credentials:

```bash
modal secret create google-secrets \
  GOOGLE_API_KEY=your_google_api_key
```

## Verifying Secrets

You can verify that your secrets are set up correctly by running:

```bash
modal secret list
```

This should show both `livekit-secrets` and `google-secrets` in the list.

## Running the Agent

Once your secrets are set up, you can run the agent with:

```bash
modal run app/app.py
```

