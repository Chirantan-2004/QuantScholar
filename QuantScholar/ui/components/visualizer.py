"""
QuantumScholar - 2D & 3D Quantum State & Bloch Sphere Visualizer
Renders interactive 3D Bloch Spheres, 2D phase diagrams, and density matrix heatmaps using Plotly.
"""

import numpy as np
import plotly.graph_objects as go
from typing import Dict, Any, Tuple

def create_3d_bloch_sphere(bloch_coords: Tuple[float, float, float], state_name: str = r"|\psi\rangle") -> go.Figure:
    """
    Renders a stunning 3D Bloch Sphere with wireframe, axes, basis poles, and the 3D statevector.
    """
    u, v, w = bloch_coords

    # 1. Sphere Surface Mesh
    phi_grid = np.linspace(0, 2 * np.pi, 50)
    theta_grid = np.linspace(0, np.pi, 50)
    phi_mesh, theta_mesh = np.meshgrid(phi_grid, theta_grid)

    x_sphere = np.sin(theta_mesh) * np.cos(phi_mesh)
    y_sphere = np.sin(theta_mesh) * np.sin(phi_mesh)
    z_sphere = np.cos(theta_mesh)

    fig = go.Figure()

    # Add semi-transparent sphere shell
    fig.add_trace(go.Surface(
        x=x_sphere, y=y_sphere, z=z_sphere,
        opacity=0.15,
        colorscale=[[0, '#00f2fe'], [1, '#4facfe']],
        showscale=False,
        hoverinfo='none'
    ))

    # 2. Equator & Meridian Circles
    equator_t = np.linspace(0, 2 * np.pi, 100)
    fig.add_trace(go.Scatter3d(
        x=np.cos(equator_t), y=np.sin(equator_t), z=np.zeros(100),
        mode='lines', line=dict(color='rgba(255,255,255,0.4)', width=3, dash='dash'),
        name='Equator (XY Plane)', hoverinfo='none'
    ))

    # 3. Coordinate Axes (X, Y, Z)
    axis_len = 1.3
    fig.add_trace(go.Scatter3d(
        x=[-axis_len, axis_len, None, 0, 0, None, 0, 0],
        y=[0, 0, None, -axis_len, axis_len, None, 0, 0],
        z=[0, 0, None, 0, 0, None, -axis_len, axis_len],
        mode='lines+text',
        line=dict(color='rgba(148, 163, 184, 0.7)', width=4),
        text=['-X', '+X (|+⟩)', '', '-Y', '+Y (|i⟩)', '', '-Z (|1⟩)', '+Z (|0⟩)'],
        textposition='top center',
        name='Bloch Axes',
        hoverinfo='text'
    ))

    # 4. Standard Basis State Poles
    poles_x = [0, 0, 1, -1, 0, 0]
    poles_y = [0, 0, 0, 0, 1, -1]
    poles_z = [1, -1, 0, 0, 0, 0]
    poles_labels = ['|0⟩ (Z+)', '|1⟩ (Z-)', '|+⟩ (X+)', '|-⟩ (X-)', '|+i⟩ (Y+)', '|-i⟩ (Y-)']

    fig.add_trace(go.Scatter3d(
        x=poles_x, y=poles_y, z=poles_z,
        mode='markers+text',
        marker=dict(size=5, color='#38bdf8'),
        text=poles_labels,
        textposition='bottom center',
        name='Basis Poles',
        hoverinfo='text'
    ))

    # 5. Statevector Vector (Line from Origin to (u, v, w))
    fig.add_trace(go.Scatter3d(
        x=[0, u], y=[0, v], z=[0, w],
        mode='lines+markers',
        line=dict(color='#ef4444', width=8),
        marker=dict(size=[0, 9], color=['#ef4444', '#f87171']),
        name=f'Statevector {state_name}',
        hovertext=[f'Origin', f'{state_name}<br>u (⟨X⟩): {u:.3f}<br>v (⟨Y⟩): {v:.3f}<br>w (⟨Z⟩): {w:.3f}']
    ))

    # 6. Projection Dashed Line to Equator
    fig.add_trace(go.Scatter3d(
        x=[u, u, 0], y=[v, v, 0], z=[w, 0, 0],
        mode='lines',
        line=dict(color='#facc15', width=3, dash='dot'),
        name='State Projections',
        hoverinfo='none'
    ))

    # Layout Styling
    fig.update_layout(
        title=dict(text=f"<b>3D Bloch Sphere Representation:</b> <code>({u:.3f}, {v:.3f}, {w:.3f})</code>", font=dict(size=15, color="#f8fafc")),
        scene=dict(
            xaxis=dict(range=[-1.4, 1.4], showgrid=False, zeroline=False, showticklabels=False, title='X'),
            yaxis=dict(range=[-1.4, 1.4], showgrid=False, zeroline=False, showticklabels=False, title='Y'),
            zaxis=dict(range=[-1.4, 1.4], showgrid=False, zeroline=False, showticklabels=False, title='Z'),
            aspectmode='cube',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        paper_bgcolor='rgba(15, 23, 42, 0.95)',
        legend=dict(font=dict(color='#94a3b8'), bgcolor='rgba(30, 41, 59, 0.7)')
    )
    return fig

def create_2d_density_matrix_plot(density_matrix: np.ndarray) -> go.Figure:
    """
    Renders 2D heatmap showing Real (populations) and Imaginary (coherences) parts of the density matrix.
    """
    dim = density_matrix.shape[0]
    labels = [f"|{bin(i)[2:].zfill(int(np.log2(dim)))}⟩" for i in range(dim)]

    real_part = np.real(density_matrix)
    imag_part = np.imag(density_matrix)

    fig = go.Figure(data=go.Heatmap(
        z=real_part,
        x=labels,
        y=labels,
        colorscale='Viridis',
        text=np.round(real_part, 3),
        texttemplate="%{text}",
        colorbar=dict(title="Re(ρ)")
    ))

    fig.update_layout(
        title="<b>2D Density Matrix Populations $\\text{Re}(\\rho)$</b>",
        xaxis_title="Basis State",
        yaxis_title="Basis State",
        margin=dict(l=40, r=40, b=40, t=50),
        paper_bgcolor='rgba(15, 23, 42, 0.95)',
        plot_bgcolor='rgba(15, 23, 42, 0.95)',
        font=dict(color="#f8fafc")
    )
    return fig

def create_2d_phase_polar_plot(statevector: np.ndarray) -> go.Figure:
    """
    Renders 2D Polar Phasor Plot displaying amplitude magnitudes and complex phases arg(c_k).
    """
    dim = len(statevector)
    labels = [f"|{bin(i)[2:].zfill(int(np.log2(dim)))}⟩" for i in range(dim)]
    magnitudes = np.abs(statevector)
    phases_deg = np.degrees(np.angle(statevector))

    fig = go.Figure()
    for i in range(dim):
        fig.add_trace(go.Barpolar(
            r=[magnitudes[i]],
            theta=[phases_deg[i]],
            name=f"Amplitude {labels[i]}",
            marker=dict(line=dict(color='white', width=1.5)),
            hovertext=f"{labels[i]}<br>Magnitude: {magnitudes[i]:.3f}<br>Phase: {phases_deg[i]:.1f}°"
        ))

    fig.update_layout(
        title="<b>2D Complex Phase & Amplitude Polar Diagram</b>",
        polar=dict(
            radialaxis=dict(range=[0, 1.1], showticklabels=True, ticks=''),
            angularaxis=dict(direction='counterclockwise', period=360)
        ),
        paper_bgcolor='rgba(15, 23, 42, 0.95)',
        font=dict(color="#f8fafc"),
        margin=dict(l=40, r=40, b=40, t=50)
    )
    return fig
