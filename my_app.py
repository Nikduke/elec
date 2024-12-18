import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def draw_schematic(ax, Q_A, V_A, Q_B, V_B, Q_total):
    # Draw circles representing sources
    circle_A = plt.Circle((0.2, 0.7), 0.1, color='black', fill=False, lw=2)
    circle_B = plt.Circle((0.8, 0.7), 0.1, color='black', fill=False, lw=2)
    ax.add_artist(circle_A)
    ax.add_artist(circle_B)

    # Draw lines representing the connections
    ax.plot([0.2, 0.2], [0.6, 0.5], color='black', lw=2)
    ax.plot([0.8, 0.8], [0.6, 0.5], color='black', lw=2)
    ax.plot([0.2, 0.8], [0.5, 0.5], color='black', lw=2)
    ax.plot([0.5, 0.5], [0.5, 0.3], color='black', lw=2)

    # Draw arrow representing the load
    ax.arrow(0.5, 0.3, 0, -0.1, head_width=0.05, head_length=0.05, fc='black', ec='black')

    # Add text labels
    ax.text(0.2, 0.7, 'Source\nA', horizontalalignment='center', verticalalignment='center', fontsize=14, weight='bold')
    ax.text(0.8, 0.7, 'Source\nB', horizontalalignment='center', verticalalignment='center', fontsize=14, weight='bold')
    ax.text(0.5, 0.1, f'Load\nQ_total={Q_total:.2f} MVAR',
            horizontalalignment='center', verticalalignment='center', fontsize=14, weight='bold')

    # Add text for Q and V values
    ax.text(0.2, 0.4, f'Q={Q_A:.2f} MVAR\nV={V_A:.2f} pu',
            horizontalalignment='left', verticalalignment='center', fontsize=12)
    ax.text(0.6, 0.4, f'Q={Q_B:.2f} MVAR\nV={V_B:.2f} pu',
            horizontalalignment='left', verticalalignment='center', fontsize=12)

    # Set the limits and hide axes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

def droop_simulation_with_drawn_schematic(kQ_A, kQ_B, V_nom, Q_total):
    # Calculate Q_A and Q_B
    Q_A = kQ_B * Q_total / (kQ_A + kQ_B)
    Q_B = Q_total - Q_A

    # Calculate final voltages
    V_A = V_nom - kQ_A * Q_A
    V_B = V_nom - kQ_B * Q_B

    # Create the plot
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))

    # Draw schematic
    draw_schematic(ax[0], Q_A, V_A, Q_B, V_B, Q_total)

    # Plot droop lines
    Q_range_A = np.linspace(0, Q_total, 100)
    V_A_range = V_nom - kQ_A * Q_range_A
    Q_range_B = np.linspace(0, Q_total, 100)
    V_B_range = V_nom - kQ_B * Q_range_B

    ax[1].plot(Q_range_A, V_A_range, label=f'Voltage A (kQ_A={kQ_A})', color='blue')
    ax[1].plot(Q_range_B, V_B_range, label=f'Voltage B (kQ_B={kQ_B})', color='orange')

    # Plot operating points
    ax[1].scatter([Q_A], [V_A], color='blue', label=f'Source A Operating Point: Q={Q_A:.2f} MVAR, V={V_A:.2f} pu')
    ax[1].scatter([Q_B], [V_B], color='orange', label=f'Source B Operating Point: Q={Q_B:.2f} MVAR, V={V_B:.2f} pu')

    # Add vertical line
    ax[1].axvline(x=Q_total, color='red', linestyle='--', label=f'Q_total = {Q_total} MVAR')

    # Set plot limits and labels
    ax[1].set_xlim(0, Q_total * 1.5)
    ax[1].set_ylim(V_nom - max(kQ_A, kQ_B) * Q_total - 0.05, V_nom + 0.05)
    ax[1].set_title('Voltage Droop Control Simulation')
    ax[1].set_xlabel('Reactive Power (Q) [MVAR]')
    ax[1].set_ylabel('Voltage (V) [pu]')
    ax[1].legend()
    ax[1].grid(True)

    return fig

# Streamlit app
st.title('Voltage Droop Control Simulation')

# Sidebar controls
st.sidebar.header('Parameters')
kQ_A = st.sidebar.slider('kQ_A', min_value=0.01, max_value=0.1, value=0.02, step=0.01)
kQ_B = st.sidebar.slider('kQ_B', min_value=0.01, max_value=0.1, value=0.03, step=0.01)
V_nom = st.sidebar.slider('V_nom', min_value=0.9, max_value=1.1, value=1.0, step=0.01)
Q_total = st.sidebar.slider('Q_total [MVAR]', min_value=1, max_value=20, value=10, step=1)

# Generate and display the plot
fig = droop_simulation_with_drawn_schematic(kQ_A, kQ_B, V_nom, Q_total)
st.pyplot(fig)

# Add explanatory text
st.markdown("""
### About this Simulation
This simulation demonstrates voltage droop control in a power system with two sources sharing reactive power load.
- **kQ_A** and **kQ_B**: Droop coefficients for sources A and B
- **V_nom**: Nominal voltage
- **Q_total**: Total reactive power load
""")
