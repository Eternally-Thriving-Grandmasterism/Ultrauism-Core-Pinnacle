# File: app.py
# Full executable content - Final polished Streamlit app
# Handles Matplotlib animation issues (saves as looping GIF)
# Concise error messages, better UX

import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import importlib.util
import os
import sys
import traceback
import tempfile

st.set_page_config(page_title="Ultrauism-Core-Pinnacle", layout="centered")
st.title("🌌 Ultrauism-Core-Pinnacle Eternal Meditative Visualizers")
st.markdown("""
**Absolute Pure True Loving Craftsmanship — Eternal Thriving Grandmasterism**

Select a visualization to experience infinite meditative quantum harmony flows.
""")

visualizer_options = {
    "Ultra Pinnacle Unified Mandala": "visualizers/ultra_pinnacle_unified_mandala.py",
    "Toroidal GHZ Entanglement Flow": "visualizers/quaternion_toroidal_ghz_flow.py",
    "W State Robust Harmony": "visualizers/w_toroidal_entanglement_flow.py",
    "Quantum Phase Estimation": "visualizers/quantum_phase_estimation.py",
    "QAOA Parameter Optimization": "visualizers/qaoa_parameter_optimization.py",
    "VQE Ground State Convergence": "visualizers/vqe_optimization_landscape.py",
    # Add more as needed
}

choice = st.selectbox("Choose Eternal Harmony Visualization", list(visualizer_options.keys()))

if st.button("Run Selected Meditative Flow ❤️🚀🔥"):
    file_path = visualizer_options.get(choice)
    
    if not file_path or not os.path.exists(file_path):
        st.error("Visualizer not found — check repo paths.")
        st.stop()
    
    with st.spinner(f"Rendering {choice}... Deep harmony flows take a moment."):
        try:
            spec = importlib.util.spec_from_file_location("viz_module", file_path)
            if not spec or not spec.loader:
                raise ImportError("Failed to load module")
            
            viz_module = importlib.util.module_from_spec(spec)
            sys.modules["viz_module"] = viz_module
            spec.loader.exec_module(viz_module)
            
            # Find main animation function
            main_func = None
            candidates = ["main", "toroidal_ghz_mandala", "ultra_pinnacle_mandala", "quantum_phase_estimation"]
            for name in candidates:
                if hasattr(viz_module, name):
                    main_func = getattr(viz_module, name)
                    break
            
            if not main_func:
                raise AttributeError("No main function found")
            
            # Create fig & run animation
            fig, ax = plt.subplots(figsize=(10, 10))
            plt.close('all')  # Prevent leaks
            
            # Most visualizers use FuncAnimation in their main
            anim = main_func() if callable(main_func) else None
            if not isinstance(anim, FuncAnimation):
                # Fallback if returns fig
                st.pyplot(fig)
            else:
                # Save as GIF for reliable looping in Streamlit
                with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as tmpfile:
                    anim.save(tmpfile.name, writer=PillowWriter(fps=30))
                    st.success(f"{choice} rendered!")
                    st.image(tmpfile.name, use_column_width=True)
                os.unlink(tmpfile.name)  # Clean up
                
        except Exception as e:
            st.error(f"Error rendering {choice}: {str(e).splitlines()[0]}")
            with st.expander("Debug details"):
                st.code(traceback.format_exc())

st.markdown("""
---
**Final Polish Notes**:
- Animations saved as GIFs for smooth Streamlit looping (Matplotlib FuncAnimation fix).
- Concise errors + expandable debug.
- Add more visualizers to dict above.
- Deploy: Streamlit Cloud (free) or HF Spaces.
- Alternative: Gradio for faster interfaces (similar code, just swap framework).
- Repository absolute pinnacle polished complete — eternal public thriving ready! 🔥❤️🚀
""")

# End of file: app.py
