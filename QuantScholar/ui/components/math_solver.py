"""
QuantumScholar - UI Component: Quantum Math Equation Solver & Visualizer
Renders step-by-step mathematical work and interactive 3D/2D models for quantum equations.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from integrations.math_engine import QuantumMathEngine
from ui.components.visualizer import create_3d_bloch_sphere, create_2d_density_matrix_plot, create_2d_phase_polar_plot

math_engine = QuantumMathEngine()

def render_math_equation_solver_section():
    """Renders the dedicated Quantum Math Equation Solver & 2D/3D Model tab."""
    st.markdown("## 📐 Quantum Math Solver & 2D/3D State Visualizer")
    st.markdown(
        "Enter any quantum state, wave function, Pauli operator, or Hamiltonian equation. "
        "QuantumScholar will compute the **step-by-step mathematical derivation** of how the work is done, "
        "and generate interactive **3D Bloch Spheres**, **2D Density Matrix Heatmaps**, and **Complex Phase Polar Plots**."
    )

    # Preset equations
    preset_eq = st.selectbox(
        "💡 Quick Preset Equations & Quantum States:",
        [
            "Select an equation or type below...",
            "|psi> = 1/sqrt(2) (|0> + |1>)",
            "|Phi+> = 1/sqrt(2) (|00> + |11>)",
            "|Psi-> = 1/sqrt(2) (|01> - |10>)",
            "|i> = 1/sqrt(2) (|0> + i|1>)",
            "|-i> = 1/sqrt(2) (|0> - i|1>)",
            "|-> = 1/sqrt(2) (|0> - |1>)",
            "|psi> = 1/sqrt(3) |0> + sqrt(2/3) e^(i pi/4) |1>",
            "|1> (Excited State)",
            "|0> (Ground State)"
        ]
    )

    default_eq = "|psi> = 1/sqrt(2) (|0> + |1>)" if preset_eq == "Select an equation or type below..." else preset_eq
    user_eq = st.text_input("Enter Quantum Equation / State / Hamiltonian:", value=default_eq)

    solve_btn = st.button("⚡ Solve Math & Render 3D/2D Models", type="primary", use_container_width=True)

    if solve_btn or user_eq:
        with st.spinner("Executing Dirac algebraic expansion & computing 3D Bloch coordinates..."):
            res = math_engine.parse_and_solve_state(user_eq)

        st.markdown("---")
        
        # Two-column layout: Math Derivation on left, 3D/2D Visualizations on right
        col_math, col_vis = st.columns([1, 1])

        with col_math:
            st.markdown("### 📝 Step-by-Step Mathematical Derivation")
            st.info(f"**Target Equation:** {res['latex_representation']}")

            # Step-by-step accordion
            for i, step in enumerate(res["derivation_steps"], 1):
                with st.expander(f"📌 Step {i}: {step.splitlines()[0].replace('**', '')}", expanded=True):
                    st.markdown("\n".join(step.splitlines()[1:]))

            # Expectation values table
            st.markdown("#### 🎯 Observable Expectation Values")
            exp_df = pd.DataFrame([
                {"Observable": "Pauli X (σ_x)", "Expectation Value ⟨X⟩": f"{res['expectation_values']['X']:.4f}", "Physical Meaning": "Superposition bias in X-basis"},
                {"Observable": "Pauli Y (σ_y)", "Expectation Value ⟨Y⟩": f"{res['expectation_values']['Y']:.4f}", "Physical Meaning": "Phase coherence / imaginary component"},
                {"Observable": "Pauli Z (σ_z)", "Expectation Value ⟨Z⟩": f"{res['expectation_values']['Z']:.4f}", "Physical Meaning": "Population difference (|0⟩ vs |1⟩)"}
            ])
            st.dataframe(exp_df, use_container_width=True, hide_index=True)

        with col_vis:
            st.markdown("### 🌐 3D & 2D Quantum Models")
            
            # Sub-tabs for models
            model_tab1, model_tab2, model_tab3, model_tab4 = st.tabs([
                "🌐 3D Bloch Sphere",
                "📊 2D Density Matrix",
                "🌀 2D Phase Polar Plot",
                "📈 Measurement Probabilities"
            ])

            with model_tab1:
                if res["state_type"] == "single_qubit":
                    fig_3d = create_3d_bloch_sphere(res["bloch_coords"], state_name=user_eq)
                    st.plotly_chart(fig_3d, use_container_width=True)
                    st.markdown(
                        f"**Bloch Coordinates:** `u = {res['bloch_coords'][0]}`, `v = {res['bloch_coords'][1]}`, `w = {res['bloch_coords'][2]}` | "
                        f"**θ:** `{np.degrees(res['theta']):.1f}°`, **φ:** `{np.degrees(res['phi']):.1f}°`"
                    )
                else:
                    st.warning("⚠️ 3D Bloch Sphere is defined for 2-level single-qubit states. For composite 2-qubit entangled states, view the 4x4 Density Matrix and Measurement tabs!")

            with model_tab2:
                fig_rho = create_2d_density_matrix_plot(res["density_matrix"])
                st.plotly_chart(fig_rho, use_container_width=True)

            with model_tab3:
                fig_polar = create_2d_phase_polar_plot(res["statevector"])
                st.plotly_chart(fig_polar, use_container_width=True)

            with model_tab4:
                prob_df = pd.DataFrame([
                    {"Basis State": f"|{k}⟩", "Probability": f"{v*100:.2f}%", "Raw Amplitude": f"{np.abs(res['statevector'][i]):.3f}"}
                    for i, (k, v) in enumerate(res["probabilities"].items())
                ])
                fig_prob = px.bar(prob_df, x="Basis State", y=[float(v.replace("%","")) for v in prob_df["Probability"]], title="Born Rule Probability Distribution P(k)", color="Basis State", color_discrete_sequence=px.colors.qualitative.Prism)
                st.plotly_chart(fig_prob, use_container_width=True)
                st.dataframe(prob_df, use_container_width=True, hide_index=True)
