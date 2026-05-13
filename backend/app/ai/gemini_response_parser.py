import json
import re
import logging

logger = logging.getLogger(__name__)

class GeminiResponseParser:
    @staticmethod
    def parse_json(text: str) -> dict:
        """
        Cleans and parses JSON from AI response.
        Handles markdown code blocks and common formatting issues.
        Includes resilience for schema mismatches.
        """
        try:
            # 1. Extract JSON string from response
            # First, try markdown code blocks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Fallback: Find the first '{' and the last '}'
                start_index = text.find('{')
                end_index = text.rfind('}')
                if start_index != -1 and end_index != -1 and end_index > start_index:
                    json_str = text[start_index:end_index+1]
                else:
                    json_str = text.strip()

            # 2. Parse JSON
            data = json.loads(json_str)
            
            # Post-processing: Deep Recursive Unwrapping
            # Handles cases like {'structured_data': {'content_analysis': {'score': ...}}}
            schema_keys = ['score', 'strengths', 'weaknesses', 'text', 'full_text', 'hook_text', 'title', 'scenes', 'tags', 'prompt']
            
            while isinstance(data, dict) and len(data) == 1:
                key = list(data.keys())[0]
                val = data[key]
                
                if isinstance(val, dict):
                    # If the nested dict has schema keys, we're likely there
                    if any(k in val for k in schema_keys):
                        data = val
                        break # Stop at the one that has the keys
                    else:
                        # Continue unwrapping deeper
                        data = val
                elif isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
                    # Handle cases like {'data': [{...}]}
                    if any(k in val[0] for k in schema_keys):
                        data = val[0]
                        break
                    else:
                        data = val[0]
                else:
                    # Can't unwrap further or it's a primitive
                    break
            
            # 3. Post-processing: Resilience for common schema mismatches
            # Detect single scene object and wrap in scenes list
            if 'scene_number' in data and 'visual' in data and 'scenes' not in data:
                # This is a single scene object, wrap it
                data = {'scenes': [data]}
            
            # Field Synonym Mapping
            if 'scenes' in data and isinstance(data['scenes'], list):
                for scene in data['scenes']:
                    if isinstance(scene, dict):
                        # Handle 'audio' synonyms
                        if 'audio' not in scene or scene['audio'] is None:
                            for syn in ['speech', 'voiceover', 'dialogue', 'narration', 'text']:
                                if syn in scene and scene[syn]:
                                    scene['audio'] = scene[syn]
                                    break
                        if 'audio' not in scene or scene['audio'] is None:
                            scene['audio'] = "" # Default to empty string to pass validation
                            
                        # Handle 'visual' synonyms
                        if 'visual' not in scene or scene['visual'] is None:
                            for syn in ['description', 'scene', 'video', 'visuals', 'image']:
                                if syn in scene and scene[syn]:
                                    scene['visual'] = scene[syn]
                                    break
                        if 'visual' not in scene or scene['visual'] is None:
                            scene['visual'] = "No visual description provided."

            # If a field expected to be a string (like full_text) is a list, flatten it
            string_fields = ['full_text', 'hook_text', 'primary_text', 'text', 'prompt']
            for field in string_fields:
                if field in data and isinstance(data[field], list):
                    flattened = []
                    for item in data[field]:
                        if isinstance(item, dict):
                            # Join dict values (e.g. {'role': 'A', 'spoke': 'B'} -> 'A: B')
                            flattened.append(": ".join([str(v) for v in item.values()]))
                        else:
                            flattened.append(str(item))
                    data[field] = "\n".join(flattened)
            
            # Handle ViralScore field synonym mapping
            if 'score' in data:
                # Handle 'strength' → 'strengths'
                if 'strength' in data and 'strengths' not in data:
                    strength_val = data['strength']
                    if isinstance(strength_val, list):
                        data['strengths'] = strength_val
                    else:
                        data['strengths'] = [strength_val]
                
                if 'strengths' not in data or not data['strengths']:
                    data['strengths'] = ['Strong content hook']  # Default
                
                # Handle 'weakness' → 'weaknesses'
                if 'weakness' in data and 'weaknesses' not in data:
                    weakness_val = data['weakness']
                    if isinstance(weakness_val, list):
                        data['weaknesses'] = weakness_val
                    else:
                        data['weaknesses'] = [weakness_val]
                
                if 'weaknesses' not in data or not data['weaknesses']:
                    data['weaknesses'] = ['Could be more original']  # Default
            
            return data
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse AI JSON: {str(e)}\nRaw text: {text[:500]}")
            raise ValueError(f"Malformed JSON response from AI: {str(e)}")
