import sys
import os
from dotenv import load_dotenv
from utils.logger import section, info, stage, ok, error, dim, BOLD, RESET, YELLOW, GREEN, CYAN
from utils.validator import UserInput, SUPPORTED_PLATFORMS, SUPPORTED_STYLES
from pipeline import (
    hook_generator,
    script_generator,
    caption_generator,
    hashtag_generator,
    thumbnail_prompt_generator,
    viral_score_generator
)

# Load env vars
load_dotenv()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_input():
    section("AI CREATOR STUDIO PROTOTYPE")
    
    print(f"{BOLD}Enter Topic:{RESET} (e.g. The future of Quantum Computing)")
    topic = input("> ").strip()
    
    print(f"\n{BOLD}Select Niche:{RESET} (e.g. Tech, Finance, Fitness)")
    niche = input("> ").strip()
    
    print(f"\n{BOLD}Select Platform:{RESET} {dim(str(SUPPORTED_PLATFORMS))}")
    platform = input("> ").strip()
    if not platform: platform = SUPPORTED_PLATFORMS[0]
    
    print(f"\n{BOLD}Select Style:{RESET} {dim(str(SUPPORTED_STYLES))}")
    style = input("> ").strip()
    if not style: style = SUPPORTED_STYLES[0]
    
    try:
        user_data = UserInput(topic=topic, niche=niche, platform=platform, style=style)
        return user_data
    except Exception as e:
        error(f"Invalid input: {e}")
        sys.exit(1)

def run_pipeline(data: UserInput):
    results = {}
    
    stage("Stage 1: Generating Hook (Ollama)")
    results['hook_data'] = hook_generator.run(data.topic, data.niche, data.platform, data.style)
    ok(f"Hook Generated: {results['hook_data']['hook'][:50]}...")
    
    stage("Stage 2: Generating Script (Gemini)")
    results['script_data'] = script_generator.run(data.topic, data.niche, data.platform, data.style, results['hook_data']['hook'])
    ok(f"Script Generated: {results['script_data']['title']}")
    
    stage("Stage 3: Generating Captions (Ollama)")
    results['caption_data'] = caption_generator.run(data.topic, data.platform, data.style, results['hook_data']['hook'])
    ok("Captions Generated.")
    
    stage("Stage 4: Generating Hashtags (Ollama)")
    results['hashtag_data'] = hashtag_generator.run(data.topic, data.niche, data.platform)
    ok(f"Hashtags Generated: {len(results['hashtag_data']['tags'])} tags.")
    
    stage("Stage 5: Generating Thumbnail Prompt (Ollama)")
    results['thumbnail_data'] = thumbnail_prompt_generator.run(data.topic, data.style, results['hook_data']['hook'])
    ok("Thumbnail Prompt Generated.")
    
    stage("Stage 6: Analysing Viral Potential (Rule-based)")
    results['viral_data'] = viral_score_generator.run(
        results['hook_data']['hook'], 
        results['script_data']['script'], 
        results['script_data']['cta']
    )
    ok(f"Analysis Complete. Score: {results['viral_data']['score']}")
    
    return results

def display_results(results):
    clear_screen()
    section("GENERATED CONTENT RESULTS")
    
    print(f"\n{GREEN}=================================={RESET}")
    print(f"{BOLD}TITLE:{RESET} {results['script_data']['title']}")
    print(f"{GREEN}=================================={RESET}")
    
    print(f"\n{CYAN}--- HOOK ---{RESET}")
    print(f"{BOLD}Text:{RESET} {results['hook_data']['hook']}")
    print(f"{BOLD}Emotion:{RESET} {results['hook_data']['emotion']}")
    print(f"{BOLD}Visual Cue:{RESET} {results['hook_data']['visual_cue']}")
    
    print(f"\n{CYAN}--- SCRIPT ---{RESET}")
    print(results['script_data']['script'])
    
    print(f"\n{CYAN}--- SCENE BREAKDOWN ---{RESET}")
    for scene in results['script_data']['scene_breakdown']:
        print(f"[{scene['scene']}] {BOLD}Visual:{RESET} {scene['visual']}")
        print(f"    {BOLD}Audio:{RESET} {scene['narration']}")
    
    print(f"\n{CYAN}--- CAPTIONS ---{RESET}")
    print(f"{BOLD}Primary:{RESET} {results['caption_data']['primary']}")
    print(f"{BOLD}Secondary:{RESET} {results['caption_data']['secondary']}")
    
    print(f"\n{CYAN}--- HASHTAGS ---{RESET}")
    print(" ".join(results['hashtag_data']['tags']))
    
    print(f"\n{CYAN}--- THUMBNAIL PROMPT ---{RESET}")
    print(f"{BOLD}Prompt:{RESET} {results['thumbnail_data']['prompt']}")
    print(f"{BOLD}Style:{RESET} {results['thumbnail_data']['style_reference']}")
    print(f"{BOLD}Palette:{RESET} {results['thumbnail_data']['colour_palette']}")
    
    print(f"\n{YELLOW}=================================={RESET}")
    print(f"{BOLD}VIRAL SCORE:{RESET} {results['viral_data']['score']}/100 - {results['viral_data']['label']}")
    print(f"{YELLOW}=================================={RESET}")
    
    print(f"\n{BOLD}STRENGTHS:{RESET}")
    for s in results['viral_data']['strengths']: print(f" {GREEN}\u2713{RESET} {s}")
    
    print(f"\n{BOLD}WEAKNESSES:{RESET}")
    for w in results['viral_data']['weaknesses']: print(f" {RED}\u2717{RESET} {w}")

def main():
    try:
        user_data = get_user_input()
        results = run_pipeline(user_data)
        display_results(results)
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
