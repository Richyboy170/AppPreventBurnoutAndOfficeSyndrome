"""Gradio UI for Burnout Prevention App."""
import gradio as gr
from datetime import datetime
from typing import List, Tuple

from config import settings
from tools.database_tools import get_db
from agents.wellness_companion_agent import create_wellness_companion
from agents.stretch_coach_agent import create_stretch_coach
from agents.break_scheduler_agent import create_break_scheduler


class WellnessApp:
    """Main application UI."""

    def __init__(self):
        """Initialize the wellness app."""
        self.db = get_db()
        self.current_user = None
        self.wellness_agent = None
        self.stretch_coach = None
        self.break_scheduler = None

    def initialize_user(self, username: str) -> str:
        """Initialize or get user."""
        if not username:
            return "Please enter a username"

        # Check if user exists
        user = self.db.get_user_by_username(username)

        if not user:
            # Create new user
            user = self.db.create_user(username=username)
            message = f"Welcome to your wellness journey, {username}! 🌟"
        else:
            message = f"Welcome back, {username}! 👋"

        self.current_user = user

        # Initialize agents
        self.wellness_agent = create_wellness_companion(user.id)
        self.stretch_coach = create_stretch_coach(user.id)
        self.break_scheduler = create_break_scheduler(user.id)

        # Get stats
        stats = self.get_stats_display()

        return f"{message}\n\n{stats}"

    def get_stats_display(self) -> str:
        """Get formatted stats display."""
        if not self.current_user:
            return "Please log in first"

        user = self.db.get_user(self.current_user.id)
        pet = self.db.get_pet(user.id)
        stats = self.db.get_user_stats(user.id, days=7)

        display = f"""📊 **Your Wellness Stats**

**Overall Progress:**
- Current Streak: {user.current_streak} days 🔥
- Total Points: {user.total_points} 💎
- Total Breaks: {user.total_breaks_taken} ☕
- Total Stretches: {user.total_stretches_completed} 🤸

**This Week:**
- Breaks taken: {stats['breaks']}
- Stretches completed: {stats['stretches']}
- Points earned: {stats['points_earned']}

**Your Pet - {pet.name if pet else 'N/A'}:**
- Health: {f"{pet.health:.1f}/100 ❤️" if pet else 'N/A'}
- Happiness: {f"{pet.happiness:.1f}/100 😊" if pet else 'N/A'}
- Level: {pet.level if pet else 'N/A'}
- Stage: {pet.evolution_stage if pet else 'N/A'} 🐾
"""
        return display

    def chat_interface(self, message: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], str]:
        """Handle chat interaction."""
        if not self.current_user:
            return history + [(message, "Please log in first using the Setup tab.")], ""

        if not self.wellness_agent:
            self.wellness_agent = create_wellness_companion(self.current_user.id)

        # Get response
        result = self.wellness_agent.chat(message)
        response = result['response']

        # Update history
        history.append((message, response))

        return history, ""

    def take_break(self) -> str:
        """Record a break."""
        if not self.current_user:
            return "Please log in first"

        result = self.break_scheduler.record_break()

        message = f"""✅ **Break Recorded!**

You earned {result['points_earned']} points!

Your pet gained {settings.PET_HEALTH_GAIN_PER_BREAK} health! ❤️

Keep up the good work! Regular breaks are essential for preventing burnout.
"""
        return message

    def get_stretch_list(self) -> str:
        """Get list of available stretches."""
        if not self.current_user:
            return "Please log in first"

        stretches = self.stretch_coach.get_all_stretches()

        display = "**Available Stretches:**\n\n"

        for stretch in stretches[:10]:  # Show first 10
            display += f"**{stretch['name']}** ({stretch['difficulty']})\n"
            display += f"- Category: {stretch['category']}\n"
            display += f"- Duration: {stretch['duration_seconds']}s\n"
            display += f"- Points: {stretch['points']}\n"
            display += f"- Description: {stretch['description']}\n\n"

        return display

    def complete_stretch(self, stretch_id: str) -> str:
        """Complete a stretch."""
        if not self.current_user:
            return "Please log in first"

        if not stretch_id:
            return "Please enter a stretch ID"

        result = self.stretch_coach.complete_stretch(stretch_id)

        if 'error' in result:
            return f"Error: {result['error']}"

        message = f"""✅ **{result['stretch_name']} Completed!**

You earned {result['points_earned']} points! 💎

Your pet gained {settings.PET_HAPPINESS_GAIN_PER_STRETCH} happiness! 😊

{result['message']}
"""
        return message

    def get_achievements(self) -> str:
        """Get user achievements."""
        if not self.current_user:
            return "Please log in first"

        achievements = self.db.get_user_achievements(self.current_user.id)

        unlocked = [a for a in achievements if a['unlocked']]
        locked = [a for a in achievements if not a['unlocked']]

        display = f"**🏆 Achievements ({len(unlocked)}/{len(achievements)} unlocked)**\n\n"

        display += "**Unlocked:**\n"
        for ach in unlocked[:5]:  # Show first 5
            display += f"{ach['icon']} **{ach['name']}** ({ach['tier']})\n"
            display += f"  {ach['description']}\n\n"

        display += "\n**Locked:**\n"
        for ach in locked[:5]:  # Show first 5
            display += f"🔒 **{ach['name']}** ({ach['tier']})\n"
            display += f"  {ach['description']}\n\n"

        return display

    def build_ui(self) -> gr.Blocks:
        """Build the Gradio interface."""
        theme = gr.themes.Soft()
        with gr.Blocks(title="Wellness Companion", theme=theme) as app:
            gr.Markdown("# 🌟 Burnout & Office Syndrome Prevention App")
            gr.Markdown("Your AI-powered wellness companion for preventing burnout and staying healthy!")

            with gr.Tabs():
                # Setup Tab
                with gr.Tab("👤 Setup"):
                    gr.Markdown("## Welcome! Let's get you started.")
                    username_input = gr.Textbox(label="Username", placeholder="Enter your username")
                    login_btn = gr.Button("Start My Wellness Journey", variant="primary")
                    login_output = gr.Markdown()

                    login_btn.click(
                        fn=self.initialize_user,
                        inputs=[username_input],
                        outputs=[login_output]
                    )

                # Chat Tab
                with gr.Tab("💬 Wellness Companion"):
                    gr.Markdown("## Chat with your AI wellness companion")
                    chatbot = gr.Chatbot(height=400)
                    msg = gr.Textbox(
                        label="Your message",
                        placeholder="How are you feeling today?",
                        lines=2
                    )
                    send_btn = gr.Button("Send", variant="primary")

                    # Start conversation button
                    start_chat_btn = gr.Button("Start New Conversation")

                    def start_new_chat():
                        if self.wellness_agent:
                            greeting = self.wellness_agent.start_conversation()
                            return [(None, greeting)]
                        return []

                    start_chat_btn.click(fn=start_new_chat, outputs=[chatbot])

                    send_btn.click(
                        fn=self.chat_interface,
                        inputs=[msg, chatbot],
                        outputs=[chatbot, msg]
                    )
                    msg.submit(
                        fn=self.chat_interface,
                        inputs=[msg, chatbot],
                        outputs=[chatbot, msg]
                    )

                # Breaks Tab
                with gr.Tab("☕ Breaks"):
                    gr.Markdown("## Take Regular Breaks")
                    gr.Markdown("Remember: breaks are essential for productivity and wellbeing!")

                    break_btn = gr.Button("I Took a Break!", variant="primary", size="lg")
                    break_output = gr.Markdown()

                    break_btn.click(
                        fn=self.take_break,
                        outputs=[break_output]
                    )

                # Stretches Tab
                with gr.Tab("🤸 Stretches"):
                    gr.Markdown("## Complete Stretches")

                    with gr.Row():
                        with gr.Column():
                            list_btn = gr.Button("Show Available Stretches")
                            stretch_list = gr.Markdown()

                        with gr.Column():
                            stretch_id_input = gr.Textbox(
                                label="Stretch ID",
                                placeholder="e.g., neck_side_stretch"
                            )
                            complete_btn = gr.Button("Complete Stretch", variant="primary")
                            stretch_output = gr.Markdown()

                    list_btn.click(
                        fn=self.get_stretch_list,
                        outputs=[stretch_list]
                    )

                    complete_btn.click(
                        fn=self.complete_stretch,
                        inputs=[stretch_id_input],
                        outputs=[stretch_output]
                    )

                # Stats Tab
                with gr.Tab("📊 Stats"):
                    gr.Markdown("## Your Wellness Dashboard")

                    refresh_btn = gr.Button("Refresh Stats", variant="secondary")
                    stats_output = gr.Markdown()

                    refresh_btn.click(
                        fn=self.get_stats_display,
                        outputs=[stats_output]
                    )

                # Achievements Tab
                with gr.Tab("🏆 Achievements"):
                    gr.Markdown("## Your Achievements")

                    refresh_ach_btn = gr.Button("View Achievements", variant="secondary")
                    ach_output = gr.Markdown()

                    refresh_ach_btn.click(
                        fn=self.get_achievements,
                        outputs=[ach_output]
                    )

            gr.Markdown("""
---
**Tips for preventing burnout:**
- Take breaks every 45-60 minutes
- Do stretches to relieve physical tension
- Talk to your wellness companion when feeling stressed
- Track your progress and celebrate small wins
- Remember: your wellbeing is a priority! 💚
            """)

        return app


def create_app() -> gr.Blocks:
    """Create and return the Gradio app."""
    wellness_app = WellnessApp()
    return wellness_app.build_ui()


if __name__ == "__main__":
    app = create_app()
    app.launch(
        server_name=settings.GRADIO_SERVER_NAME,
        server_port=settings.GRADIO_SERVER_PORT,
        share=settings.SHARE_GRADIO
    )
