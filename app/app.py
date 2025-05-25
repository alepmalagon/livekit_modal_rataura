import logging
import os
from dotenv import load_dotenv
import modal

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    RoomOutputOptions,
    RunContext,
    WorkerOptions,
    cli,
    metrics,
)
from livekit.agents.llm import function_tool
from livekit.agents.voice import MetricsCollectedEvent
from livekit.plugins import silero
from livekit.plugins.google import RealtimeModel
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger("livekit-modal-agent")
logging.basicConfig(level=logging.INFO)

# Create a Modal app
app = modal.App("livekit-modal-agent")

# Create a Modal image with the necessary dependencies
image = modal.Image.debian_slim().pip_install(
    "livekit-agents>=1.0.0",
    "livekit-plugins-google",
    "livekit-plugins-silero",
    "python-dotenv",
)

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

# Function to prewarm the worker
def prewarm(proc: JobProcess):
    # Load the VAD model during prewarm to speed up agent initialization
    proc.userdata["vad"] = silero.VAD.load()

# Main entrypoint function for the Modal worker
@app.function(
    image=image,
    secrets=[
        modal.Secret.from_name("livekit-secrets"),
        modal.Secret.from_name("google-secrets"),
    ],
    timeout=3600,  # 1 hour timeout
)
async def entrypoint(ctx: JobContext):
    # Set up logging context
    ctx.log_context_fields = {
        "room": ctx.room.name,
        "user_id": "modal-agent",
    }
    
    # Connect to the LiveKit room
    await ctx.connect()
    
    # Create an agent session with Gemini RealtimeModel
    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
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
    
    # Set up metrics collection
    usage_collector = metrics.UsageCollector()
    
    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)
    
    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")
    
    # Add shutdown callback to log usage when the session ends
    ctx.add_shutdown_callback(log_usage)
    
    # Wait for a participant to join the room
    await ctx.wait_for_participant()
    
    # Start the agent session
    await session.start(
        agent=GeminiAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )

# Run the worker
@app.local_entrypoint()
def main():
    # Run the worker with the entrypoint function
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))

if __name__ == "__main__":
    main()

