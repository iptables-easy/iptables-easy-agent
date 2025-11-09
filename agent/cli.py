import argparse
import asyncio
import aiohttp
import sys
import os
from datetime import datetime
import json


class AgentCLI:
    def __init__(self, backend_url: str, agent_token: str):
        self.backend_url = backend_url.rstrip('/')
        self.agent_token = agent_token
        self.node_id = None
    
    async def send_heartbeat(self):
        """Send heartbeat to backend"""
        try:
            async with aiohttp.ClientSession() as session:
                data = {
                    "agent_token": self.agent_token,
                    "status": "online",
                    "system_info": {
                        "platform": sys.platform,
                        "python_version": sys.version
                    }
                }
            
            async with session.post(
                f"{self.backend_url}/nodes/{self.node_id}/heartbeat",
                json=data,
                headers={"Authorization": f"Bearer {self.agent_token}"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"💓 Heartbeat sent at {datetime.utcnow()}")
                    return result
        except Exception as e:
            print(f"❌ Error sending heartbeat: {e}")
            return None
    
    async def start_heartbeat_loop(self):
        """Start the heartbeat loop"""
        print("🔄 Starting heartbeat loop...")
        while True:
            await self.send_heartbeat()
            await asyncio.sleep(30)  # Send heartbeat every 30 seconds


def main():
    parser = argparse.ArgumentParser(description="iptables-easy Agent")
    parser.add_argument("--backend-url", required=True, help="Backend API URL")
    parser.add_argument("--token", required=True, help="Agent authentication token")
    
    args = parser.parse_args()
    
    if not args.backend_url or not args.token:
        print("❌ Both --backend-url and --token are required")
        sys.exit(1)
    
    print(f"🔗 Connecting to backend: {args.backend_url}")
    print(f"🔑 Using token: {args.token[:8]}...")
    
    # Start the agent
    agent = AgentCLI(args.backend_url, args.token)
    
    try:
        # Start heartbeat loop
        asyncio.run(agent.start_heartbeat_loop())
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped")


if __name__ == "__main__":
    main()
