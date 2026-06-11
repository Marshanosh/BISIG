import httpx
import asyncio
import base64

class GemmaMatcher:
    def __init__(self, colab_url: str):
        self.colab_url = colab_url.rstrip("/")
        # LocalTunnel requires this header to bypass the 'reminder' page
        self.headers = {"bypass-tunnel-reminder": "true"}
        self.client = httpx.AsyncClient(timeout=30.0, headers=self.headers)

    async def find_match(self, frame_buffer, preferred_lang=None, threshold=0.3):
        if not frame_buffer:
            return None, 0.0, None, 0.0
            
        # Get the latest frame that HAS an image
        image_b64 = None
        for f in reversed(frame_buffer):
            if f.get("image"):
                image_b64 = f.get("image")
                break
        
        if not image_b64:
            return None, 0.0, "Blind (No Image)", 0.0
            
        try:
            # Extract pure base64 data
            image_raw = image_b64.split(",")[1]
            
            # Official Gemma 4 / llama-server multimodal format
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Describe this sign language gesture in one word."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_raw}"}}
                        ]
                    }
                ],
                "stream": False,
                "max_tokens": 10
            }
            
            response = await self.client.post(f"{self.colab_url}/v1/chat/completions", json=payload)
            
            if response.status_code == 200:
                prediction = response.json()["choices"][0]["message"]["content"].strip().lower()
                # Clean up punctuation
                prediction = "".join(e for e in prediction if e.isalnum() or e.isspace())
                return prediction, 0.9, prediction, 0.1
            else:
                print(f"Gemma 4 Server error: {response.status_code}")
                return None, 0.0, f"Error: {response.status_code}", 0.0
        except Exception as e:
            print(f"GemmaMatcher error: {e}")
            
        return None, 0.0, None, 0.0
