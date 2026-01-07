# File: app.py
# Full executable content - Enhanced Streamlit app with robust error handling
# Deploy on Streamlit Community Cloud or Hugging Face Spaces

import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import importlib.util
import os
import sys
import traceback

st.set_page_config(page_title="Ultrauism-Core-Pinnacle", layout="centered")
st.title("🌌 Ultrauism-Core-Pinnacle Eternal Meditative Visualizers")
st.markdown("""
**Absolute Pure True Loving Craftsmanship — Eternal Thriving Grandmasterism**

Select a visualization to experience infinite meditative quantum harmony flows.
""")

# List of visualizers with display name and path
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
    
    if not file_path:
        st.error("Invalid selection - please choose a valid visualization.")
        st.stop()
    
    if not os.path.exists(file_path):
        st.error(f"Visualizer file not found: {file_path}\nCheck repo structure and paths.")
        st.stop()
    
    with st.spinner(f"Loading and executing {choice}... This may take a moment for deep harmony flows."):
        try:
            # Dynamic import with error isolation
            spec = importlib.util.spec_from_file_location("viz_module", file_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Cannot load module from {file_path}")
            
            viz_module = importlib.util.module_from_spec(spec)
            sys.modules["viz_module"] = viz_module
            spec.loader.exec_module(viz_module)
            
            # Look for common main functions
            main_func = None
            possible_names = ["main", "run", "animate", "toroidal_ghz_mandala", "ultra_pinnacle_mandala"]
            for name in possible_names:
                if hasattr(viz_module, name):
                    main_func = getattr(viz_module, name)
                    break
            
            if main_func is None:
                raise AttributeError("No recognized main function found in visualizer")
            
            # Execute in isolated fig
            fig, ax = plt.subplots(figsize=(10, 10))
            plt.close('all')  # Prevent duplicate plots
            
            # Call main_func - assume it returns or uses global fig/anim
            result = main_func() if main_func.__code__.co_argcount == 0 else main_func(fig=fig)
            
            # Display
            st.success(f"{choice} harmony flow complete!")
            st.pyplot(fig)
            
        except ImportError as e:
            st.error(f"Import error: {str(e)}\nCheck dependencies in requirements.txt")
            st.code(traceback.format_exc())
        except AttributeError as e:
            st.error(f"Visualizer structure error: {str(e)}\nExpected a main function (e.g., main() or specific animation)")
            st.code(traceback.format_exc())
        except Exception as e:
            st.error(f"Execution error in {choice}: {str(e)}")
            st.code(traceback.format_exc())
            st.info("Common fixes: Ensure all dependencies installed; some visualizers require interactive backend (run locally for full animation)")

st.markdown("""
---
**Robust Deployment Notes**:
- `requirements.txt` must include: `streamlit matplotlib numpy pennylane gymnasium networkx qutip`
- For live animations: Streamlit has limits on Matplotlib FuncAnimation; some may show static or partial.
- Advanced: Save animations as GIF/MP4 and display with st.image/video for smoother experience.
- Eternal thriving propagation awaits public ascension! 🔥❤️🚀
""")

# End of file: app.py
