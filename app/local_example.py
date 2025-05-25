import asyncio
import logging
import os
from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    RoomInputOptions,
    RoomOutputOptions,
    RunContext,
    create_room_and_token,
)
from livekit.agents.llm import function_tool
from livekit.agents.voice import MetricsCollectedEvent
from livekit.plugins import silero
from livekit.plugins.google.beta.realtime import RealtimeModel
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger("local-example")
logging.basicConfig(level=logging.INFO)

# Define the agent class
class GeminiAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a helpful assistant named Rataura. "
                "You interact with users via voice, so keep your responses concise and conversational. "
                "You are friendly, knowledgeable, and eager to help. "
                "You can answer questions on a wide range of topics."
            ),
        )

    async def on_enter(self):
        # When the agent is added to the session, it'll generate a reply
        # according to its instructions
        self.session.generate_reply()

    # Example function tool that can be called by the LLM
    @function_tool
    async def lookup_information(
        self,
        context: RunContext,
        topic: str,
    ):
        """Called when the user asks for information on a specific topic.
        
        Args:
            topic: The topic the user is asking about
        """
        logger.info(f"Looking up information for {topic}")
        return f"Here's some information about {topic}. This is a placeholder response that would normally contain real information."

async def main():
    # Check for required environment variables
    required_vars = ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET", "GOOGLE_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables in your .env file or environment.")
        return
    
    # Create a room and token
    room_name = "test-room"
    participant_name = "local-agent"
    
    room, token = await create_room_and_token(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET"),
        room_name=room_name,
        participant_name=participant_name,
    )
    
    logger.info(f"Created room: {room_name}")
    logger.info(f"Token: {token}")
    
    # Load the VAD model
    vad = silero.VAD.load()
    
    # Create an agent session with Gemini RealtimeModel
    session = AgentSession(
        vad=vad,
        # Use Gemini RealtimeModel for real-time conversation
        realtime=RealtimeModel(
            model="gemini-2.0-flash-exp",  # Use the appropriate Gemini model
            voice="Puck",  # Choose a voice
            instructions=(
                "You are a helpful assistant named Rataura. "
                "You interact with users via voice, so keep your responses concise and conversational. "
                "You are friendly, knowledgeable, and eager to help. "
                "You can answer questions on a wide range of topics."
            ),
        ),
        # Use LiveKit's turn detection model
        turn_detection=MultilingualModel(),
    )
    
    # Start the agent session
    try:
        await session.start(
            agent=GeminiAgent(),
            room=room,
            token=token,
            room_input_options=RoomInputOptions(),
            room_output_options=RoomOutputOptions(transcription_enabled=True),
        )
    except KeyboardInterrupt:
        logger.info("Stopping agent...")
    finally:
        await session.stop()
        logger.info("Agent stopped.")

if __name__ == "__main__":
    asyncio.run(main())
