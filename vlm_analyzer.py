# /xauusd_bot/vlm_analyzer.py

import base64
import requests
import logging
import json
from config import OPENAI_API_KEY, VLM_PROMPT

class VLMTechnicalAnalyzer:
    """
    Uses OpenAI's Vision Language Model to analyze chart images.
    """
    def __init__(self):
        if not OPENAI_API_KEY or OPENAI_API_KEY == "sk-YOUR_OPENAI_API_KEY_HERE":
            raise ValueError("OpenAI API key is not configured in config.py")
        self.api_key = OPENAI_API_KEY
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def _encode_image(self, image_path):
        """Encodes an image file to a base64 string."""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logging.error(f"Error encoding image {image_path}: {e}")
            return None

    def analyze_chart(self, image_path):
        """
        Sends a chart image to the OpenAI VLM and returns the structured analysis.
        
        Returns:
            dict: The JSON analysis from the VLM, or None if an error occurred.
        """
        logging.info(f"Starting VLM analysis for chart: {image_path}")
        base64_image = self._encode_image(image_path)
        if not base64_image:
            return None

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": VLM_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1500
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=payload)
            response.raise_for_status()  # Raises an exception for 4XX/5XX errors
            
            response_text = response.json()['choices'][0]['message']['content']
            
            # Clean the response to ensure it's valid JSON
            # VLM can sometimes wrap the JSON in ```json ... ```
            if response_text.strip().startswith("```json"):
                response_text = response_text.strip()[7:-3]

            analysis_json = json.loads(response_text)
            logging.info("VLM analysis received and parsed successfully.")
            return analysis_json

        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            return None
        except (json.JSONDecodeError, KeyError) as e:
            logging.error(f"Failed to parse VLM response as JSON: {e}")
            logging.error(f"Raw response received: {response_text}")
            return None