import openai
from openai import OpenAI
import time
import logging
from typing import Dict, Optional, List

class QuestionProcessor:
    def __init__(self, config: Dict) -> None:
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.client = OpenAI(api_key=config['openai']['api_key'])
        self.model = config['openai']['model']
        self.retries = config['processing']['retries']
        self.delay = config['processing']['delay_between_retries']
        self.prompt_template = config['prompt']['template']
        self.system_message = config['prompt']['system_message']

    def process_batch(self, questions: List[Dict]) -> List[Dict]:
        results = []
        for q in questions:
            if q is not None:
                result = self.reformulate_question(q)
                if result:
                    results.append(result)
                    self.logger.info(f"Successfully processed question: {q.get('Question', '')[:50]}...")
        return results

    def reformulate_question(self, question_data: Dict) -> Optional[Dict]:
        prompt = self._create_prompt(question_data)
        self.logger.debug(f"Generated prompt: {prompt}")

        for attempt in range(self.retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_message},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.config['openai']['temperature'],
                    max_tokens=self.config['openai']['max_tokens']
                )
                parsed = self._parse_response(response.choices[0].message.content)
                if parsed:
                    self.logger.debug(f"Parsed response: {parsed}")
                return parsed
            except Exception as e:
                self.logger.warning(f"Attempt {attempt+1} failed: {str(e)}")
                if attempt < self.retries - 1:
                    time.sleep(self.delay)
                else:
                    self.logger.error(f"Failed all attempts for question: {question_data.get('Question', 'Unknown')}")
                    return None


    def _create_prompt(self, data: Dict) -> str:
        try:
            # Debug logging
            self.logger.debug(f"Input data: {data}")
            formatted = self.prompt_template.format(**data)
            self.logger.debug(f"Formatted prompt: {formatted}")
            return formatted
        except KeyError as e:
            self.logger.error(f"Missing key in data: {e}")
            self.logger.error(f"Available keys: {data.keys()}")
            raise

    def _parse_response(self, response_text: str) -> Optional[Dict]:
        try:
            parsed = {}
            for line in response_text.splitlines():
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('Question:'):
                    parsed['Question'] = line[9:].strip()
                elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                    option = line[0]
                    parsed[option] = line[2:].strip()
                elif line.startswith('Correct Answer:'):
                    parsed['Correct_Answer'] = line[-1].upper()
            
            if not parsed:
                self.logger.error(f"No data parsed from response: {response_text}")
            return parsed
        except Exception as e:
            self.logger.error(f"Error parsing response: {str(e)}\nResponse text: {response_text}")
            return None