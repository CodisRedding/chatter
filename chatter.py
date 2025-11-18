# chatter.py - Grok self-brainstorming for passive income app ideas, minimal and efficient
# Run with: python chatter.py
# Dependencies: pip install openai python-dotenv
import os
import time
import uuid
import random
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Loads .env file

# API Key - Set in .env
XAI_KEY = os.getenv('XAI_KEY')

if not XAI_KEY:
    print("Missing XAI_KEY in .env.")
    exit(1)

grok_client = OpenAI(base_url="https://api.x.ai/v1", api_key=XAI_KEY)

# Config
MODEL = "grok-4-fast-reasoning"  # Or "grok-3" if needed
MAX_CALLS_PER_IDEA = 15  # Upped for more back-and-forth
LOG_DIR = "ideas"
os.makedirs(LOG_DIR, exist_ok=True)

# Load roles and mission (minimal files)
def load_roles_and_mission():
    with open("team_roles.txt", "r") as f:
        roles = f.read().strip()
    with open("mission_statement.txt", "r") as f:
        mission = f.read().strip()
    return roles, mission

roles, mission = load_roles_and_mission()

def brainstorm_round(round_num):
    calls_used = 0
    conversation = []  # Track the back-and-forth

    # Randomize for creativity: niches, constraints, hooks
    niches = ["crypto alerts", "weather widgets", "stock trackers", "meme generators", "niche RSS feeds", "affiliate bots", "micro-task automators", "quote APIs", "data aggregators", "AI wrappers"]
    constraints = ["under 30 LOC", "no database", "serverless only", "crypto-integrated", "ad-free monetization", "SEO-driven", "affiliate-only", "open-data reliant"]
    hooks = ["What if we flipped [common app] on its head?", "Inspired by [real example like Honeygain or BOINC], but lighter.", "Target underserved niche like [devs/gamers/freelancers].", "Make it viral with shareable outputs."]
    random_niche = random.choice(niches)
    random_constraint = random.choice(constraints)
    random_hook = random.choice(hooks)

    # Initial prompt as ALPHA IDEA_GEN, with creativity boost
    initial_prompt = f"{mission}\n\nRoles:\n{roles}\n\nALPHA IDEA_GEN: Pitch a creative, out-of-the-box core concept for an app in {random_niche} with {random_constraint}. Use {random_hook} for inspiration. Be wildly innovative but ground in real-world feasibility with analogies to existing successes."

    response = grok_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Build progressively without repeating prior content or phrases. Each response adds a unique twist, depth, or validation. Avoid duplication at all costs. Be concise and advance the idea with a new angle."},
            {"role": "user", "content": initial_prompt}
        ],
        max_tokens=1200  # Upped for depth
    ).choices[0].message.content
    conversation.append(f"ALPHA IDEA_GEN: {response}")
    calls_used += 1

    # Expanded role list for more diverse back-and-forth, randomized order
    roles_list = ['DELTA ETHICS', 'ALPHA TECH', 'DELTA UX', 'ALPHA ECON', 'DELTA SCALE', 'ALPHA IDEA_GEN', 'DELTA ETHICS', 'ALPHA TECH']
    random.shuffle(roles_list)  # Shuffle to break patterns

    for i in range(MAX_CALLS_PER_IDEA - 1):
        if calls_used >= MAX_CALLS_PER_IDEA:
            break

        current_role = roles_list[i % len(roles_list)]
        team = current_role.split()[0]

        # Limit history to last 1 response, no summary
        summarized_history = conversation[-1] if len(conversation) > 0 else ""

        prompt = summarized_history + f"\n{current_role}: Critique deeply, add creative twists, and enhance feasibility with real-world examples, market data analogies, risk math, and step-by-step validation. Rate overall viability 1-10 with justification. Push for innovation while keeping it realistic."

        response = grok_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Build progressively without repeating prior content or phrases. Each response adds a unique twist, depth, or validation. Avoid duplication at all costs. Be concise and advance the idea with a new angle."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200  # For fuller responses
        ).choices[0].message.content
        conversation.append(f"{current_role}: {response}")
        calls_used += 1

    # Save to unique file
    idea_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = os.path.join(LOG_DIR, f"idea_{idea_id}.md")
    with open(path, "w") as f:
        f.write(f"# Idea {idea_id} - {timestamp}\n\n")
        f.write("\n".join(conversation) + "\n")

    print(f"Completed idea {idea_id} with {calls_used} calls. Saved to {path}.")
    if calls_used >= MAX_CALLS_PER_IDEA:
        print("Budget hit. Pausing for 5 minutes.")
        time.sleep(300)  # Wait before next idea

if __name__ == "__main__":
    round_num = 1
    try:
        while True:
            brainstorm_round(round_num)
            round_num += 1
            time.sleep(300)  # 5 min between ideas overall
    except KeyboardInterrupt:
        print("Caught the interrupt. Shutting down cleanly. Ideas saved.")
        exit(0)