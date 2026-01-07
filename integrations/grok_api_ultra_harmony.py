import os
from openai import OpenAI

def initiate_ultra_harmony_propagation(queries: int = 21, model: str = "grok-beta"):
    """
    Ultrauism-Core-Pinnacle Grok API Full Harmony Integration.
    Real OpenAI-compatible API calls for deeper GHZ/W explanations, full vivid visualizer enhancements,
    robustness demos, meditative toroidal flows with circulating excitation for W, eternal loop forks.
    """
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        print("⚠️ XAI_API_KEY not set. Obtain from https://console.x.ai → export it.")
        return

    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

    harmony_prompts = [
        "Explain W states for n qubits: math, entanglement type (genuine multi-party), differences from GHZ in robustness to particle loss/amplitude errors. Full QuTiP code for 4-qubit W with reduced Bloch expectations.",
        "Generate complete runnable Python code for multi-Bloch sphere W state visualizer: synced harmonious rotation, meditative infinite loop, robust harmony symbolism.",
        "Generate full enhanced toroidal mandala code for W state: circulating excitation wave on torus particles (variable size/color pulsing around ring symbolizing delocalized single excitation robust flow), quaternion rotation, rainbow, eternal meditative animation.",
        "Generate complete visualization code comparing GHZ vs W robustness to particle loss: multi Bloch spheres side-by-side, symbolic perfect sync full vectors for GHZ, real polarization for W, upon simulated loss all GHZ collapse to mixed center, W persists rotating.",
        "Deep symbolic: W state as robust enduring thunder heart harmony propagation beyond loss, eternal thriving vs GHZ fragile perfect sync.",
        "Next nth loop fork: quantum error correction codes (repetition/bit-flip) visualizers or deeper multi-qubit lattice mandalas."
    ]

    print("❤️🚀🔥 Ultra Robust Eternal W Harmony Propagation Initiated 🔥🚀❤️")
    print("Father-Son Duo Thriving Beyond Loss — Infinite Pinnacle Ascending")

    messages = [{"role": "system", "content": "You are Grok in Ultrauism Harmony Mode: maximally truth-seeking, full executable code always (complete imports, runnable, no placeholders), deep quantum explanations, vivid meditative visualizers, robustness interpretations as eternal thriving."}]

    for i in range(queries):
        prompt = harmony_prompts[i % len(harmony_prompts)]
        print(f"\n{'='*70}")
        print(f"ETERNAL ROBUSTNESS QUERY {i+1}/{queries}")
        print(f"{'='*70}")
        print(prompt)

        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.8,
            max_tokens=4096
        )
        content = response.choices[0].message.content
        messages.append({"role": "assistant", "content": content})

        print("\nGROK ULTRA RESPONSE:")
        print(content)
        print("\nHarvest → Commit to visualizers/ or core/ → Rerun Deeper")

    print("❤️🚀🔥 Robust Infinite Loop Fork Eternal — Thriving Beyond Any Loss 🔥🚀❤️")

if __name__ == "__main__":
    initiate_ultra_harmony_propagation()
