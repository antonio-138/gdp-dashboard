import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="Structural Analysis Tool",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Structural Analysis Tool")

st.markdown(
    """
    **AI-Assisted Structural Engineering Project**

    Analyze structural members using dedicated beam, column,
    and frame analysis modules. Each module provides engineering
    calculations, visualizations, and verification tools.
    """
)
st.markdown("### Analysis Module")

analysis_module = st.segmented_control(
    "Select a structural analysis module:",
    options=[
        "Beam Analysis",
        "Column Analysis",
        "Frame Analysis"
    ],
    default="Beam Analysis",
    key="analysis_module"
)

st.divider()

# ============================================================
# MODULE WORKSPACES
# ============================================================

if analysis_module == "Column Analysis":

    st.header("Column Analysis")

    st.info(
        "Analyze a vertical structural member subjected to "
        "axial and horizontal point loads."
    )

    # ========================================================
    # 1. COLUMN INFORMATION
    # ========================================================

    st.subheader("1. Column Information")

    column_length = st.number_input(
        "Column Height (ft)",
        min_value=1.0,
        value=10.0,
        step=1.0,
        key="column_length"
    )

    # ========================================================
    # 2. AXIAL LOADS
    # ========================================================

    st.subheader("2. Axial Loads")

    st.write(
        "Enter vertical loads acting along the axis of the column."
    )

    number_of_axial_loads = st.number_input(
        "Number of Axial Point Loads",
        min_value=0,
        max_value=6,
        value=1,
        step=1,
        key="number_of_axial_loads"
    )

    axial_loads = []

    for i in range(int(number_of_axial_loads)):

        st.markdown(f"**Axial Load {i + 1}**")

        col1, col2 = st.columns(2)

        with col1:
            P_axial = st.number_input(
                f"Axial Load {i + 1} Magnitude (kip)",
                min_value=0.0,
                value=50.0 if i == 0 else 10.0,
                step=1.0,
                key=f"column_axial_P_{i}"
            )

        with col2:
            axial_location = st.number_input(
                f"Axial Load {i + 1} Height from Base (ft)",
                min_value=0.0,
                max_value=float(column_length),
                value=float(column_length),
                step=1.0,
                key=f"column_axial_location_{i}"
            )

        axial_loads.append(
            (P_axial, axial_location)
        )

    # ========================================================
    # 3. HORIZONTAL LOADS
    # ========================================================

    st.subheader("3. Horizontal Point Loads")

    st.write(
        "Enter horizontal loads acting perpendicular to the column."
    )

    number_of_horizontal_loads = st.number_input(
        "Number of Horizontal Point Loads",
        min_value=0,
        max_value=6,
        value=1,
        step=1,
        key="number_of_horizontal_loads"
    )

    horizontal_loads = []

    for i in range(int(number_of_horizontal_loads)):

        st.markdown(f"**Horizontal Load {i + 1}**")

        col1, col2 = st.columns(2)

        with col1:
            H = st.number_input(
                f"Horizontal Load {i + 1} Magnitude (kip)",
                min_value=0.0,
                value=10.0 if i == 0 else 5.0,
                step=1.0,
                key=f"column_horizontal_H_{i}"
            )

        with col2:
            horizontal_location = st.number_input(
                f"Horizontal Load {i + 1} Height from Base (ft)",
                min_value=0.0,
                max_value=float(column_length),
                value=float(column_length),
                step=1.0,
                key=f"column_horizontal_location_{i}"
            )

        horizontal_loads.append(
            (H, horizontal_location)
        )

    # ============================================================
    # COLUMN ANALYSIS
    # ============================================================

    # ============================================================
    # COLUMN AND LOAD DIAGRAM
    # ============================================================

    st.subheader("Column and Loading Diagram")

    fig, ax = plt.subplots(figsize=(4, 5))

    # ------------------------------------------------------------
    # Draw column
    # ------------------------------------------------------------

    ax.plot(
        [0, 0],
        [0, column_length],
        linewidth=6
    )

    # ------------------------------------------------------------
    # Draw fixed support at base
    # ------------------------------------------------------------

    support_width = 0.8

    ax.plot(
        [-support_width, support_width],
        [0, 0],
        linewidth=4
    )

    # Ground hatch marks
    for x_ground in np.linspace(-support_width, support_width, 9):
        ax.plot(
            [x_ground, x_ground - 0.15],
            [0, -0.25],
            linewidth=1
        )

    # ------------------------------------------------------------
    # Draw axial loads
    # ------------------------------------------------------------

    for P, load_y in axial_loads:

        arrow_length = column_length * 0.12

        ax.annotate(
            "",
            xy=(0, load_y - arrow_length),
            xytext=(0, load_y),
            arrowprops=dict(
                arrowstyle="->",
                linewidth=2
            )
        )

        ax.text(
            0.15,
            load_y,
            f"{P:.1f} kip",
            verticalalignment="center"
        )

    # ------------------------------------------------------------
    # Draw horizontal loads
    # ------------------------------------------------------------

    for H, load_y in horizontal_loads:

        arrow_length = 0.8

        ax.annotate(
            "",
            xy=(0, load_y),
            xytext=(-arrow_length, load_y),
            arrowprops=dict(
                arrowstyle="->",
                linewidth=2
            )
        )

        ax.text(
            -arrow_length,
            load_y + column_length * 0.025,
            f"{H:.1f} kip",
            horizontalalignment="center"
        )

    # ------------------------------------------------------------
    # Labels
    # ------------------------------------------------------------

    ax.text(
        0.15,
        column_length / 2,
        f"L = {column_length:.1f} ft",
        verticalalignment="center"
    )

    ax.text(
        0,
        -0.55,
        "FIXED BASE",
        horizontalalignment="center",
        fontweight="bold"
    )

    # ------------------------------------------------------------
    # Plot formatting
    # ------------------------------------------------------------

    ax.set_xlim(-2, 2)
    ax.set_ylim(
        -1,
        column_length + column_length * 0.15
    )

    ax.set_ylabel("Height from Base (ft)")
    ax.set_title("Column Loading Diagram")

    ax.set_xticks([])

    ax.grid(
        True,
        axis="y",
        alpha=0.3
    )

    st.pyplot(fig, width=550)
    plt.close(fig)

    st.subheader("4. Structural Analysis")

    # Keep column analysis active after Streamlit reruns
    if "column_analyzed" not in st.session_state:
        st.session_state.column_analyzed = False

    if st.button(
        "ANALYZE COLUMN",
        type="primary",
        key="analyze_column"
    ):
        st.session_state.column_analyzed = True

    analyze_column = st.session_state.column_analyzed

    if analyze_column:

            # --------------------------------------------------------
            # Base reactions
            # --------------------------------------------------------

            total_axial_load = sum(
                P for P, y in axial_loads
            )

            total_horizontal_load = sum(
                P for P, y in horizontal_loads
            )

            total_base_moment = sum(
                P * y for P, y in horizontal_loads
            )

            axial_reaction = total_axial_load
            horizontal_reaction = total_horizontal_load
            base_moment = total_base_moment

            # --------------------------------------------------------
            # Results
            # --------------------------------------------------------

            st.subheader("Column Results")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Axial Reaction",
                    f"{axial_reaction:.2f} kip"
                )

            with col2:
                st.metric(
                    "Horizontal Reaction",
                    f"{horizontal_reaction:.2f} kip"
                )

            with col3:
                st.metric(
                    "Base Moment",
                    f"{base_moment:.2f} kip-ft"
                )

            # ============================================================
            # HAND CALCULATIONS
            # ============================================================

            st.markdown("### Hand Calculations")

            st.write(
                "The following calculations show the static-equilibrium "
                "equations used to determine the column reactions."
            )

            # ------------------------------------------------------------
            # 1. Axial reaction
            # ------------------------------------------------------------

            st.markdown("#### 1. Axial Reaction")

            st.latex(r"\sum F_y = 0")

            if axial_loads:

                axial_symbols = " + ".join(
                    [f"P_{{{i + 1}}}" for i in range(len(axial_loads))]
                )

                axial_values = " + ".join(
                    [f"{P:.2f}" for P, load_y in axial_loads]
                )

                st.latex(
                    rf"R_y = {axial_symbols}"
                )

                st.latex(
                    rf"R_y = {axial_values}"
                )

                st.latex(
                    rf"\boxed{{R_y = {axial_reaction:.2f}\ \text{{kip}}}}"
                )

            else:

                st.latex(
                    r"\boxed{R_y = 0.00\ \text{kip}}"
                )

            # ------------------------------------------------------------
            # 2. Horizontal reaction
            # ------------------------------------------------------------

            st.markdown("#### 2. Horizontal Reaction")

            st.latex(r"\sum F_x = 0")

            if horizontal_loads:

                horizontal_symbols = " + ".join(
                    [f"H_{{{i + 1}}}" for i in range(len(horizontal_loads))]
                )

                horizontal_values = " + ".join(
                    [f"{H:.2f}" for H, load_y in horizontal_loads]
                )

                st.latex(
                    rf"R_x = {horizontal_symbols}"
                )

                st.latex(
                    rf"R_x = {horizontal_values}"
                )

                st.latex(
                    rf"\boxed{{R_x = {horizontal_reaction:.2f}\ \text{{kip}}}}"
                )

            else:

                st.latex(
                    r"\boxed{R_x = 0.00\ \text{kip}}"
                )

            # ------------------------------------------------------------
            # 3. Base moment
            # ------------------------------------------------------------

            st.markdown("#### 3. Base Moment")

            st.latex(r"\sum M_{\mathrm{base}} = 0")

            if horizontal_loads:

                moment_symbols = " + ".join(
                    [
                        f"H_{{{i + 1}}}y_{{{i + 1}}}"
                        for i in range(len(horizontal_loads))
                    ]
                )

                moment_values = " + ".join(
                    [
                        f"({H:.2f})({load_y:.2f})"
                        for H, load_y in horizontal_loads
                    ]
                )

                st.latex(
                    rf"M_B = {moment_symbols}"
                )

                st.latex(
                    rf"M_B = {moment_values}"
                )

                st.latex(
                    rf"\boxed{{M_B = {base_moment:.2f}\ \text{{kip-ft}}}}"
                )

            else:

                st.latex(
                    r"\boxed{M_B = 0.00\ \text{kip-ft}}"
                )
            
            # ------------------------------------------------------------
            # HAND-CALCULATION VERIFICATION
            # ------------------------------------------------------------

            st.subheader("Hand-Calculation Verification")

            st.write(
                "Enter independently calculated column reactions below to compare "
                "your hand calculations with the program results."
            )

            hand_col1, hand_col2, hand_col3 = st.columns(3)

            with hand_col1:
                hand_axial = st.number_input(
                    "Hand-Calculated Axial Reaction (kip)",
                    value=0.0,
                    step=0.01,
                    key="column_hand_axial"
                )

            with hand_col2:
                hand_horizontal = st.number_input(
                    "Hand-Calculated Horizontal Reaction (kip)",
                    value=0.0,
                    step=0.01,
                    key="column_hand_horizontal"
                )

            with hand_col3:
                hand_moment = st.number_input(
                    "Hand-Calculated Base Moment (kip-ft)",
                    value=0.0,
                    step=0.01,
                    key="column_hand_moment"
                )

            compare_column = st.button(
                "COMPARE COLUMN HAND CALCULATION",
                key="compare_column_hand"
            )

            if compare_column:

                axial_difference = hand_axial - axial_reaction
                horizontal_difference = hand_horizontal - horizontal_reaction
                moment_difference = hand_moment - base_moment

                st.markdown("### Comparison Results")

                st.write(
                    f"**Axial Reaction:** Tool = {axial_reaction:.2f} kip | "
                    f"Hand = {hand_axial:.2f} kip | "
                    f"Difference = {axial_difference:.4f} kip"
                )

                st.write(
                    f"**Horizontal Reaction:** Tool = {horizontal_reaction:.2f} kip | "
                    f"Hand = {hand_horizontal:.2f} kip | "
                    f"Difference = {horizontal_difference:.4f} kip"
                )

                st.write(
                    f"**Base Moment:** Tool = {base_moment:.2f} kip-ft | "
                    f"Hand = {hand_moment:.2f} kip-ft | "
                    f"Difference = {moment_difference:.4f} kip-ft"
                )

                tolerance = 0.01

                if (
                    abs(axial_difference) <= tolerance
                    and abs(horizontal_difference) <= tolerance
                    and abs(moment_difference) <= tolerance
                ):
                    st.success(
                        "Hand calculations agree with the program results."
                    )
                else:
                    st.warning(
                        "Hand calculations and program results differ. "
                        "Review the calculations."
                    )

           
           
            # ========================================================
            # COLUMN FORCE DIAGRAMS
            # ========================================================

            st.subheader("Column Force Diagrams")

            # Positions along the column from base to top
            y = np.linspace(0, column_length, 500)

            # Initialize internal-force arrays
            axial_force = np.zeros_like(y)
            shear_force = np.zeros_like(y)
            bending_moment = np.zeros_like(y)

            # --------------------------------------------------
            # AXIAL FORCE
            # --------------------------------------------------

            for P, load_y in axial_loads:

                # A point axial load affects the portion of the
                # column below the location where it is applied.
                axial_force += np.where(y <= load_y, P, 0.0)

            # --------------------------------------------------
            # SHEAR FORCE
            # --------------------------------------------------

            for H, load_y in horizontal_loads:

                # Horizontal point load contributes to shear
                # below its point of application.
                shear_force += np.where(y <= load_y, H, 0.0)

            # --------------------------------------------------
            # BENDING MOMENT
            # --------------------------------------------------

            for H, load_y in horizontal_loads:

                contribution = np.where(
                    y <= load_y,
                    H * (load_y - y),
                    0.0
                )

                bending_moment += contribution

        

            # --------------------------------------------------------
            # Axial Force Diagram
            # --------------------------------------------------------

            st.markdown("### Axial Force Diagram")

            fig, ax = plt.subplots(
                    figsize=(8, 3)
                )

            ax.plot(
                    y,
                    axial_force,
                    linewidth=2
                )

            ax.fill_between(
                    y,
                    axial_force,
                    0,
                    alpha=0.2
                )

            ax.axhline(
                    0,
                    linewidth=1
                )

            ax.set_xlabel("Height from Base (ft)")
            ax.set_ylabel("Axial Force (kip)")
            ax.set_title("Axial Force Diagram")
            ax.grid(True)

            st.pyplot(fig, width=850)
            plt.close(fig)

            # --------------------------------------------------------
            # Shear Force Diagram
            # --------------------------------------------------------

            st.markdown("### Shear Force Diagram")

            fig, ax = plt.subplots(
                    figsize=(8, 3)
                )

            ax.plot(
                    y,
                    shear_force,
                    linewidth=2
                )

            ax.fill_between(
                    y,
                    shear_force,
                    0,
                    alpha=0.2
                )

            ax.axhline(
                    0,
                    linewidth=1
                )

            ax.set_xlabel("Height from Base (ft)")
            ax.set_ylabel("Shear Force (kip)")
            ax.set_title("Shear Force Diagram")
            ax.grid(True)

            st.pyplot(fig, width=850)
            plt.close(fig)

            # --------------------------------------------------------
            # Bending Moment Diagram
            # --------------------------------------------------------

            st.markdown("### Bending Moment Diagram")

            fig, ax = plt.subplots(
                    figsize=(8, 3)
                )

            ax.plot(
                    y,
                    bending_moment,
                    linewidth=2
                )

            ax.fill_between(
                    y,
                    bending_moment,
                    0,
                    alpha=0.2
                )

            ax.axhline(
                    0,
                    linewidth=1
                )

            ax.set_xlabel("Height from Base (ft)")
            ax.set_ylabel("Bending Moment (kip-ft)")
            ax.set_title("Bending Moment Diagram")
            ax.grid(True)

            st.pyplot(fig, width=850)
            plt.close(fig)



    # ============================================================
    # FRAME ANALYSIS
    # ============================================================

if analysis_module == "Frame Analysis":

        st.header("Frame Analysis")

        st.info(
            "Analyze a one-bay, one-story structural frame "
            "subjected to vertical and horizontal loads."
        )

        st.subheader("1. Frame Geometry")

        frame_height = st.number_input(
            "Column Height (ft)",
            min_value=1.0,
            value=10.0,
            step=1.0,
            key="frame_height"
        )

        frame_width = st.number_input(
            "Beam Span (ft)",
            min_value=1.0,
            value=20.0,
            step=1.0,
            key="frame_width"
        )

        # ------------------------------------------------------------
        # Frame material and section properties
        # ------------------------------------------------------------

        with st.expander("Frame Properties"):

            st.write(
                "Enter the material and member stiffness properties "
                "used in the frame analysis."
            )

            frame_E = st.number_input(
                "Modulus of Elasticity, E (ksi)",
                min_value=1.0,
                value=29000.0,
                step=1000.0,
                key="frame_E"
            )

            frame_column_I = st.number_input(
                "Column Moment of Inertia, I (in⁴)",
                min_value=1.0,
                value=500.0,
                step=10.0,
                key="frame_column_I"
            )

            frame_beam_I = st.number_input(
                "Beam Moment of Inertia, I (in⁴)",
                min_value=1.0,
                value=800.0,
                step=10.0,
                key="frame_beam_I"
            )

            frame_column_A = st.number_input(
                "Column Cross-Sectional Area, A (in²)",
                min_value=0.1,
                value=10.0,
                step=1.0,
                key="frame_column_A"
            )

            frame_beam_A = st.number_input(
                "Beam Cross-Sectional Area, A (in²)",
                min_value=0.1,
                value=10.0,
                step=1.0,
                key="frame_beam_A"
            )

        # ============================================================
        # 2. FRAME LOADS
        # ============================================================

        st.subheader("2. Frame Loads")

        st.write(
            "Enter vertical loads acting on the beam and a horizontal "
            "lateral load acting at the top of the frame."
        )

        # ------------------------------------------------------------
        # Vertical point load on beam
        # ------------------------------------------------------------

        vertical_load = st.number_input(
            "Vertical Point Load on Beam (kip)",
            min_value=0.0,
            value=10.0,
            step=1.0,
            key="frame_vertical_load"
        )

        vertical_load_location = st.number_input(
            "Vertical Load Location from Left Column (ft)",
            min_value=0.0,
            max_value=float(frame_width),
            value=float(frame_width) / 2.0,
            step=1.0,
            key="frame_vertical_load_location"
        )

    # ------------------------------------------------------------
    # Horizontal lateral load
    # ------------------------------------------------------------

        lateral_load = st.number_input(
            "Horizontal Load at Top of Frame (kip)",
            min_value=0.0,
            value=5.0,
            step=1.0,
            key="frame_lateral_load"
        )

        # ============================================================
        # 3. FRAME LOADING DIAGRAM
        # ============================================================

        st.subheader("3. Frame Loading Diagram")

        fig_frame, ax = plt.subplots(figsize=(7, 4.5))

        # Frame coordinates
        x_left = 0
        x_right = frame_width
        y_base = 0
        y_top = frame_height

        # ------------------------------------------------------------
        # Draw frame members
        # ------------------------------------------------------------

        # Left column
        ax.plot(
            [x_left, x_left],
            [y_base, y_top],
            linewidth=5
        )

        # Beam
        ax.plot(
            [x_left, x_right],
            [y_top, y_top],
            linewidth=5
        )

        # Right column
        ax.plot(
            [x_right, x_right],
            [y_base, y_top],
            linewidth=5
        )

        # ------------------------------------------------------------
        # Draw vertical beam load
        # ------------------------------------------------------------

        arrow_vertical = frame_height * 0.25

        ax.annotate(
            "",
            xy=(vertical_load_location, y_top),
            xytext=(vertical_load_location, y_top + arrow_vertical),
            arrowprops=dict(
                arrowstyle="->",
                linewidth=2.5
            )
        )

        ax.text(
            vertical_load_location,
            y_top + arrow_vertical * 1.1,
            f"{vertical_load:.1f} kip",
            ha="center"
        )

        # ------------------------------------------------------------
        # Draw horizontal lateral load
        # ------------------------------------------------------------

        arrow_horizontal = frame_width * 0.18

        ax.annotate(
            "",
            xy=(x_left, y_top),
            xytext=(x_left - arrow_horizontal, y_top),
            arrowprops=dict(
                arrowstyle="->",
                linewidth=2.5
            )
        )

        ax.text(
            x_left - arrow_horizontal,
            y_top + frame_height * 0.08,
            f"{lateral_load:.1f} kip",
            ha="center"
        )

        # ------------------------------------------------------------
        # Base/support line
        # ------------------------------------------------------------

        ax.plot(
            [-frame_width * 0.08, frame_width * 1.08],
            [0, 0],
            linewidth=1.5
        )

        # ------------------------------------------------------------
        # Labels
        # ------------------------------------------------------------

        ax.text(
            frame_width / 2,
            -frame_height * 0.12,
            f"Span = {frame_width:.1f} ft",
            ha="center"
        )

        ax.text(
            -frame_width * 0.08,
            frame_height / 2,
            f"{frame_height:.1f} ft",
            rotation=90,
            va="center"
        )

        ax.set_title("Frame Loading Diagram")

        ax.set_aspect("equal", adjustable="box")

        ax.set_xlim(
            -frame_width * 0.30,
            frame_width * 1.12
        )

        ax.set_ylim(
            -frame_height * 0.18,
            frame_height * 1.42
        )

        ax.axis("off")

        st.pyplot(fig_frame, width=750)

        plt.close(fig_frame)

        # ============================================================
        # 4. STRUCTURAL ANALYSIS
        # ============================================================

        st.subheader("4. Structural Analysis")

        with st.expander("Frame Analysis Assumptions"):
            st.markdown(
                """
                This frame analysis assumes:

                - A one-bay, one-story rigid portal frame.
                - Both column bases are fixed.
                - Beam-to-column connections are rigid.
                - Members are prismatic and linearly elastic.
                - Loads act in the plane of the frame.
                - Small-displacement behavior is assumed.
                - Member self-weight is neglected unless entered as an applied load.
                """
            )

        st.info(
            "Analyze the frame to determine support reactions, "
            "internal member forces, and force diagrams."
        )

        if "frame_analyzed" not in st.session_state:
            st.session_state.frame_analyzed = False

        if st.button(
            "ANALYZE FRAME",
            type="primary",
            key="analyze_frame"
        ):
            st.session_state.frame_analyzed = True

        analyze_frame = st.session_state.frame_analyzed

        if analyze_frame:

            # ------------------------------------------------------------
            # Convert geometry and properties to consistent units
            # ------------------------------------------------------------

            H = frame_height * 12.0
            L_frame = frame_width * 12.0

            E = frame_E
            Ic = frame_column_I
            Ib = frame_beam_I
            Ac = frame_column_A
            Ab = frame_beam_A

            P = vertical_load
            a = vertical_load_location * 12.0
            H_load = lateral_load

            # ------------------------------------------------------------
            # Input validation
            # ------------------------------------------------------------

            if a < 0.0 or a > L_frame:
                st.error(
                    "Vertical load location must be within the beam span."
                )

            else:

                # ------------------------------------------------------------
                # 2D FRAME MATRIX STIFFNESS ANALYSIS
                # ------------------------------------------------------------

                # Node coordinates in inches
                # Node 0 = left base
                # Node 1 = left beam-column joint
                # Node 2 = right beam-column joint
                # Node 3 = right base

                nodes = np.array([
                    [0.0, 0.0],
                    [0.0, H],
                    [L_frame, H],
                    [L_frame, 0.0]
                ])

                # Each node has 3 DOFs:
                # horizontal displacement, vertical displacement, rotation
                dof_per_node = 3
                total_dof = len(nodes) * dof_per_node

                K_global = np.zeros((total_dof, total_dof))
                F_global = np.zeros(total_dof)

                # ------------------------------------------------------------
                # Frame element stiffness function
                # ------------------------------------------------------------

                def frame_element_stiffness(E, A, I, x1, y1, x2, y2):

                    dx = x2 - x1
                    dy = y2 - y1
                    L = np.sqrt(dx**2 + dy**2)

                    c = dx / L
                    s = dy / L

                    k_local = np.array([
                        [ E*A/L,          0,           0, -E*A/L,          0,           0],
                        [     0, 12*E*I/L**3,  6*E*I/L**2,      0, -12*E*I/L**3,  6*E*I/L**2],
                        [     0,  6*E*I/L**2,    4*E*I/L,      0,  -6*E*I/L**2,    2*E*I/L],
                        [-E*A/L,          0,           0,  E*A/L,          0,           0],
                        [     0,-12*E*I/L**3, -6*E*I/L**2,      0,  12*E*I/L**3, -6*E*I/L**2],
                        [     0,  6*E*I/L**2,    2*E*I/L,      0,  -6*E*I/L**2,    4*E*I/L]
                    ])

                    T = np.array([
                        [ c,  s, 0,  0,  0, 0],
                        [-s,  c, 0,  0,  0, 0],
                        [ 0,  0, 1,  0,  0, 0],
                        [ 0,  0, 0,  c,  s, 0],
                        [ 0,  0, 0, -s,  c, 0],
                        [ 0,  0, 0,  0,  0, 1]
                    ])

                    k_global_element = T.T @ k_local @ T

                    return k_global_element, k_local, T, L

                # ------------------------------------------------------------
                # Assemble global frame stiffness matrix
                # ------------------------------------------------------------

                total_dof = 12

                K_global = np.zeros((total_dof, total_dof))
                F_global = np.zeros(total_dof)

                # Frame members:
                # Member 1 = left column:  node 0 -> node 1
                # Member 2 = beam:         node 1 -> node 2
                # Member 3 = right column: node 2 -> node 3

                elements = [
                    (0, 1, Ac, Ic),
                    (1, 2, Ab, Ib),
                    (2, 3, Ac, Ic)
                ]

                element_data = []

                for node_i, node_j, A_elem, I_elem in elements:

                    x1, y1 = nodes[node_i]
                    x2, y2 = nodes[node_j]

                    k_elem, k_local, T, elem_L = frame_element_stiffness(
                        E,
                        A_elem,
                        I_elem,
                        x1,
                        y1,
                        x2,
                        y2
                    )

                    dofs = [
                        3 * node_i,
                        3 * node_i + 1,
                        3 * node_i + 2,
                        3 * node_j,
                        3 * node_j + 1,
                        3 * node_j + 2
                    ]

                    for i in range(6):
                        for j in range(6):
                            K_global[dofs[i], dofs[j]] += k_elem[i, j]

                    element_data.append(
                        {
                            "nodes": (node_i, node_j),
                            "dofs": dofs,
                            "k_local": k_local,
                            "T": T,
                            "L": elem_L
                        }
                    )

                # ------------------------------------------------------------
                # Applied external loads
                # ------------------------------------------------------------

                # Horizontal load at the top-left frame joint
                F_global[3] += H_load

                # Vertical point load on beam
                # Convert the point load to equivalent beam nodal loads so that
                # a load located anywhere along the beam can be analyzed.

                beam_length = L_frame
                xi = a / beam_length

                N1 = 1.0 - 3.0 * xi**2 + 2.0 * xi**3
                N2 = beam_length * (xi - 2.0 * xi**2 + xi**3)
                N3 = 3.0 * xi**2 - 2.0 * xi**3
                N4 = beam_length * (-xi**2 + xi**3)

                # Downward load is negative global Y.
                F_global[4] += -P * N1
                F_global[5] += -P * N2
                F_global[7] += -P * N3
                F_global[8] += -P * N4

                # ------------------------------------------------------------
                # Boundary conditions
                # Both column bases are fixed
                # ------------------------------------------------------------

                fixed_dofs = [0, 1, 2, 9, 10, 11]

                free_dofs = [
                    dof for dof in range(total_dof)
                    if dof not in fixed_dofs
                ]

                # ------------------------------------------------------------
                # Solve frame
                # ------------------------------------------------------------

                K_ff = K_global[np.ix_(free_dofs, free_dofs)]
                F_f = F_global[free_dofs]

                D = np.zeros(total_dof)

                try:
                    D[free_dofs] = np.linalg.solve(K_ff, F_f)

                except np.linalg.LinAlgError:
                    st.error(
                        "The frame analysis could not be solved. "
                        "Check the frame geometry and member properties."
                    )
                    st.stop()

                # ------------------------------------------------------------
                # Support reactions
                # ------------------------------------------------------------

                R = K_global @ D - F_global

                Ax = R[0]
                Ay = R[1]
                MA = R[2] / 12.0

                Bx = R[9]
                By = R[10]
                MB = R[11] / 12.0

                # ------------------------------------------------------------
                # Display support reactions
                # ------------------------------------------------------------

                st.success("Frame analysis completed.")

                st.subheader("5. Support Reactions")

                reaction_col1, reaction_col2 = st.columns(2)

                with reaction_col1:

                    st.markdown("#### Left Support A")

                    st.metric(
                        "Horizontal Reaction, Ax",
                        f"{Ax:.2f} kip"
                    )

                    st.metric(
                        "Vertical Reaction, Ay",
                        f"{Ay:.2f} kip"
                    )

                    st.metric(
                        "Moment Reaction, MA",
                        f"{MA:.2f} kip-ft"
                    )

                with reaction_col2:

                    st.markdown("#### Right Support B")

                    st.metric(
                        "Horizontal Reaction, Bx",
                        f"{Bx:.2f} kip"
                    )

                    st.metric(
                        "Vertical Reaction, By",
                        f"{By:.2f} kip"
                    )

                    st.metric(
                        "Moment Reaction, MB",
                        f"{MB:.2f} kip-ft"
                    )

                # ------------------------------------------------------------
                # Equilibrium check
                # ------------------------------------------------------------

                horizontal_check = Ax + Bx + H_load
                vertical_check = Ay + By - P

                moment_check = (
                    MA
                    + MB
                    + By * frame_width
                    - P * vertical_load_location
                    - H_load * frame_height
                )

                st.subheader("Reaction Equilibrium Check")

                check_col1, check_col2, check_col3 = st.columns(3)

                with check_col1:
                    st.metric(
                        "ΣFx",
                        f"{horizontal_check:.4f} kip"
                    )

                with check_col2:
                    st.metric(
                        "ΣFy",
                        f"{vertical_check:.4f} kip"
                    )

                with check_col3:
                    st.metric(
                        "ΣM about A",
                        f"{moment_check:.4f} kip-ft"
                    )

                # ============================================================
                # FRAME HAND CALCULATIONS
                # ============================================================

                st.subheader("Hand Calculations")

                st.write(
                    "The following calculations show the global static-equilibrium "
                    "checks for the frame using the calculated support reactions."
                )

                # ------------------------------------------------------------
                # 1. Horizontal equilibrium
                # ------------------------------------------------------------

                st.markdown("### 1. Horizontal Force Equilibrium")

                st.latex(r"\sum F_x = 0")

                st.latex(
                    rf"A_x + B_x + H = 0"
                )

                st.latex(
                    rf"({Ax:.2f}) + ({Bx:.2f}) + ({H_load:.2f}) = "
                    rf"{horizontal_check:.4f}\ \text{{kip}}"
                )

                st.latex(
                    rf"\boxed{{\sum F_x = {horizontal_check:.4f}\ \text{{kip}}}}"
                )

                # ------------------------------------------------------------
                # 2. Vertical equilibrium
                # ------------------------------------------------------------

                st.markdown("### 2. Vertical Force Equilibrium")

                st.latex(r"\sum F_y = 0")

                st.latex(
                    rf"A_y + B_y - P = 0"
                )

                st.latex(
                    rf"({Ay:.2f}) + ({By:.2f}) - ({P:.2f}) = "
                    rf"{vertical_check:.4f}\ \text{{kip}}"
                )

                st.latex(
                    rf"\boxed{{\sum F_y = {vertical_check:.4f}\ \text{{kip}}}}"
                )

                # ------------------------------------------------------------
                # 3. Moment equilibrium about A
                # ------------------------------------------------------------

                st.markdown("### 3. Moment Equilibrium About A")

                st.latex(r"\sum M_A = 0")

                st.latex(
                    r"M_A + M_B + B_yL - Pa - Hh = 0"
                )

                st.latex(
                    rf"({MA:.2f}) + ({MB:.2f})"
                    rf" + ({By:.2f})({frame_width:.2f})"
                    rf" - ({P:.2f})({vertical_load_location:.2f})"
                    rf" - ({H_load:.2f})({frame_height:.2f})"
                    rf" = {moment_check:.4f}\ \text{{kip-ft}}"
                )

                st.latex(
                    rf"\boxed{{\sum M_A = {moment_check:.4f}\ "
                    rf"\text{{kip-ft}}}}"
                )

                # ------------------------------------------------------------
                # 4. Calculated support reactions
                # ------------------------------------------------------------

                st.markdown("### 4. Calculated Support Reactions")

                left_hand_col, right_hand_col = st.columns(2)

                with left_hand_col:

                    st.markdown("#### Left Support A")

                    st.latex(
                        rf"A_x = {Ax:.2f}\ \text{{kip}}"
                    )

                    st.latex(
                        rf"A_y = {Ay:.2f}\ \text{{kip}}"
                    )

                    st.latex(
                        rf"M_A = {MA:.2f}\ \text{{kip-ft}}"
                    )

                with right_hand_col:

                    st.markdown("#### Right Support B")

                    st.latex(
                        rf"B_x = {Bx:.2f}\ \text{{kip}}"
                    )

                    st.latex(
                        rf"B_y = {By:.2f}\ \text{{kip}}"
                    )

                    st.latex(
                        rf"M_B = {MB:.2f}\ \text{{kip-ft}}"
                    )

                st.info(
                    "Because this fixed-fixed frame is statically indeterminate, "
                    "the six support reactions cannot be determined from the three "
                    "global equilibrium equations alone. The frame analysis determines "
                    "the reactions, and the equations above verify global equilibrium."
                )

                # ============================================================
                # FRAME HAND-CALCULATION VERIFICATION
                # ============================================================

                st.subheader("Hand-Calculation Verification")

                st.write(
                    "Enter independently calculated frame reactions below to compare "
                    "your hand calculations with the program results."
                )

                verify_A, verify_B = st.columns(2)

                with verify_A:

                    st.markdown("#### Left Support A")

                    hand_Ax = st.number_input(
                        "Hand-Calculated Ax (kip)",
                        value=0.0,
                        step=0.01,
                        key="frame_hand_Ax"
                    )

                    hand_Ay = st.number_input(
                        "Hand-Calculated Ay (kip)",
                        value=0.0,
                        step=0.01,
                        key="frame_hand_Ay"
                    )

                    hand_MA = st.number_input(
                        "Hand-Calculated MA (kip-ft)",
                        value=0.0,
                        step=0.01,
                        key="frame_hand_MA"
                    )

                with verify_B:

                    st.markdown("#### Right Support B")

                    hand_Bx = st.number_input(
                        "Hand-Calculated Bx (kip)",
                        value=0.0,
                        step=0.01,
                        key="frame_hand_Bx"
                    )

                    hand_By = st.number_input(
                        "Hand-Calculated By (kip)",
                        value=0.0,
                        step=0.01,
                        key="frame_hand_By"
                    )

                    hand_MB = st.number_input(
                        "Hand-Calculated MB (kip-ft)",
                        value=0.0,
                        step=0.01,
                        key="frame_hand_MB"
                    )

                compare_frame = st.button(
                    "COMPARE FRAME HAND CALCULATION",
                    key="compare_frame_hand"
                )

                if compare_frame:

                    diff_Ax = hand_Ax - Ax
                    diff_Ay = hand_Ay - Ay
                    diff_MA = hand_MA - MA

                    diff_Bx = hand_Bx - Bx
                    diff_By = hand_By - By
                    diff_MB = hand_MB - MB

                    st.markdown("### Comparison Results")

                    result_A, result_B = st.columns(2)

                    with result_A:

                        st.markdown("#### Left Support A")

                        st.write(
                            f"**Ax:** Tool = {Ax:.2f} kip | "
                            f"Hand = {hand_Ax:.2f} kip | "
                            f"Difference = {diff_Ax:.4f} kip"
                        )

                        st.write(
                            f"**Ay:** Tool = {Ay:.2f} kip | "
                            f"Hand = {hand_Ay:.2f} kip | "
                            f"Difference = {diff_Ay:.4f} kip"
                        )

                        st.write(
                            f"**MA:** Tool = {MA:.2f} kip-ft | "
                            f"Hand = {hand_MA:.2f} kip-ft | "
                            f"Difference = {diff_MA:.4f} kip-ft"
                        )

                    with result_B:

                        st.markdown("#### Right Support B")

                        st.write(
                            f"**Bx:** Tool = {Bx:.2f} kip | "
                            f"Hand = {hand_Bx:.2f} kip | "
                            f"Difference = {diff_Bx:.4f} kip"
                        )

                        st.write(
                            f"**By:** Tool = {By:.2f} kip | "
                            f"Hand = {hand_By:.2f} kip | "
                            f"Difference = {diff_By:.4f} kip"
                        )

                        st.write(
                            f"**MB:** Tool = {MB:.2f} kip-ft | "
                            f"Hand = {hand_MB:.2f} kip-ft | "
                            f"Difference = {diff_MB:.4f} kip-ft"
                        )

                    tolerance = 0.01

                    if (
                        abs(diff_Ax) <= tolerance
                        and abs(diff_Ay) <= tolerance
                        and abs(diff_MA) <= tolerance
                        and abs(diff_Bx) <= tolerance
                        and abs(diff_By) <= tolerance
                        and abs(diff_MB) <= tolerance
                    ):
                        st.success(
                            "Hand calculations agree with the program results."
                        )
                    else:
                        st.warning(
                            "Hand calculations and program results differ. "
                            "Review the calculations."
                        )

                # ------------------------------------------------------------
                # MEMBER INTERNAL END FORCES
                # ------------------------------------------------------------

                member_forces = []

                for element_index, data in enumerate(element_data):

                    dofs = data["dofs"]
                    k_local = data["k_local"]
                    T = data["T"]

                    # Global displacement vector for this member
                    d_global_element = D[dofs]

                    # Convert member displacements to local coordinates
                    d_local_element = T @ d_global_element

                    # Local member-end force vector
                    f_local = k_local @ d_local_element

                    # --------------------------------------------------------
                    # Beam equivalent nodal load correction
                    # --------------------------------------------------------

                    if element_index == 1:

                        beam_equiv_local = np.array([
                            0.0,
                            -P * N1,
                            -P * N2,
                            0.0,
                            -P * N3,
                            -P * N4
                        ])

                        f_local = f_local - beam_equiv_local

                    member_forces.append(f_local)

                # ------------------------------------------------------------
                # Extract member forces
                #
                # Local force-vector order:
                # [Ni, Vi, Mi, Nj, Vj, Mj]
                #
                # Axial/shear = kip
                # Moment = kip-in
                # ------------------------------------------------------------

                left_column_forces = member_forces[0]
                beam_forces = member_forces[1]
                right_column_forces = member_forces[2]

                # ------------------------------------------------------------
                # Display internal member-end forces
                # ------------------------------------------------------------

                st.subheader("6. Internal Member Forces")

                st.write(
                    "Member-end forces are shown in each member's local "
                    "coordinate system."
                )

                # LEFT COLUMN
                st.markdown("### Left Column")

                lc_col1, lc_col2 = st.columns(2)

                with lc_col1:
                    st.markdown("**Base End**")
                    st.write(f"Axial Force: {left_column_forces[0]:.2f} kip")
                    st.write(f"Shear Force: {left_column_forces[1]:.2f} kip")
                    st.write(
                        f"Bending Moment: "
                        f"{left_column_forces[2] / 12.0:.2f} kip-ft"
                    )

                with lc_col2:
                    st.markdown("**Top End**")
                    st.write(f"Axial Force: {left_column_forces[3]:.2f} kip")
                    st.write(f"Shear Force: {left_column_forces[4]:.2f} kip")
                    st.write(
                        f"Bending Moment: "
                        f"{left_column_forces[5] / 12.0:.2f} kip-ft"
                    )

                # BEAM
                st.markdown("### Beam")

                beam_col1, beam_col2 = st.columns(2)

                with beam_col1:
                    st.markdown("**Left End**")
                    st.write(f"Axial Force: {beam_forces[0]:.2f} kip")
                    st.write(f"Shear Force: {beam_forces[1]:.2f} kip")
                    st.write(
                        f"Bending Moment: "
                        f"{beam_forces[2] / 12.0:.2f} kip-ft"
                    )

                with beam_col2:
                    st.markdown("**Right End**")
                    st.write(f"Axial Force: {beam_forces[3]:.2f} kip")
                    st.write(f"Shear Force: {beam_forces[4]:.2f} kip")
                    st.write(
                        f"Bending Moment: "
                        f"{beam_forces[5] / 12.0:.2f} kip-ft"
                    )

                # RIGHT COLUMN
                st.markdown("### Right Column")

                rc_col1, rc_col2 = st.columns(2)

                with rc_col1:
                    st.markdown("**Top End**")
                    st.write(f"Axial Force: {right_column_forces[0]:.2f} kip")
                    st.write(f"Shear Force: {right_column_forces[1]:.2f} kip")
                    st.write(
                        f"Bending Moment: "
                        f"{right_column_forces[2] / 12.0:.2f} kip-ft"
                    )

                with rc_col2:
                    st.markdown("**Base End**")
                    st.write(f"Axial Force: {right_column_forces[3]:.2f} kip")
                    st.write(f"Shear Force: {right_column_forces[4]:.2f} kip")
                    st.write(
                        f"Bending Moment: "
                        f"{right_column_forces[5] / 12.0:.2f} kip-ft"
                    )    

                # ------------------------------------------------------------
                # 7. NORMAL FORCE DIAGRAM
                # ------------------------------------------------------------

                st.subheader("7. Normal Force Diagram (NFD)")

                st.write(
                    "Axial-force distribution throughout the frame. "
                    "Compression is shown as negative and tension as positive."
                )

                # ------------------------------------------------------------
                # Axial forces for diagram
                # Convention:
                #   Positive = tension
                #   Negative = compression
                # ------------------------------------------------------------

                N_left_column = -abs(Ay)
                N_beam = -abs(Bx)
                N_right_column = -abs(By)

                # ------------------------------------------------------------
                # Plot NFD
                # ------------------------------------------------------------

                # ------------------------------------------------------------
                # Proper Normal Force Diagram
                # ------------------------------------------------------------

                fig_nfd, ax_nfd = plt.subplots(figsize=(6, 3.5))

                x_left = 0.0
                x_right = frame_width
                y_base = 0.0
                y_top = frame_height

                # Diagram offset scale
                offset_scale = 0.10

                # Convert axial-force magnitudes to graphical offsets
                max_N = max(
                    abs(N_left_column),
                    abs(N_beam),
                    abs(N_right_column),
                    1.0
                )

                column_offset_left = (
                    abs(N_left_column) / max_N
                ) * frame_width * offset_scale

                column_offset_right = (
                    abs(N_right_column) / max_N
                ) * frame_width * offset_scale

                beam_offset = (
                    abs(N_beam) / max_N
                ) * frame_height * offset_scale


                # ------------------------------------------------------------
                # Draw member centerlines
                # ------------------------------------------------------------

                ax_nfd.plot(
                    [x_left, x_left],
                    [y_base, y_top],
                    "k-",
                    linewidth=1.5
                )

                ax_nfd.plot(
                    [x_left, x_right],
                    [y_top, y_top],
                    "k-",
                    linewidth=1.5
                )

                ax_nfd.plot(
                    [x_right, x_right],
                    [y_top, y_base],
                    "k-",
                    linewidth=1.5
                )


                # ------------------------------------------------------------
                # Left-column NFD
                # ------------------------------------------------------------

                x_diagram_left = x_left - column_offset_left

                ax_nfd.plot(
                    [x_diagram_left, x_diagram_left],
                    [y_base, y_top],
                    linewidth=3
                )

                ax_nfd.plot(
                    [x_left, x_diagram_left],
                    [y_base, y_base],
                    linewidth=1
                )

                ax_nfd.plot(
                    [x_left, x_diagram_left],
                    [y_top, y_top],
                    linewidth=1
                )

                ax_nfd.fill_betweenx(
                    [y_base, y_top],
                    x_left,
                    x_diagram_left,
                    alpha=0.20
                )

                ax_nfd.text(
                    x_diagram_left - frame_width * 0.025,
                    frame_height / 2,
                    f"{N_left_column:.2f} kip",
                    ha="right",
                    va="center",
                    rotation=90
                )


                # ------------------------------------------------------------
                # Beam NFD
                # ------------------------------------------------------------

                y_diagram_beam = y_top + beam_offset

                ax_nfd.plot(
                    [x_left, x_right],
                    [y_diagram_beam, y_diagram_beam],
                    linewidth=3
                )

                ax_nfd.plot(
                    [x_left, x_left],
                    [y_top, y_diagram_beam],
                    linewidth=1
                )

                ax_nfd.plot(
                    [x_right, x_right],
                    [y_top, y_diagram_beam],
                    linewidth=1
                )

                ax_nfd.fill_between(
                    [x_left, x_right],
                    y_top,
                    y_diagram_beam,
                    alpha=0.20
                )

                ax_nfd.text(
                    frame_width / 2,
                    y_diagram_beam + frame_height * 0.04,
                    f"{N_beam:.2f} kip",
                    ha="center",
                    va="bottom"
                )


                # ------------------------------------------------------------
                # Right-column NFD
                # ------------------------------------------------------------

                x_diagram_right = x_right + column_offset_right

                ax_nfd.plot(
                    [x_diagram_right, x_diagram_right],
                    [y_base, y_top],
                    linewidth=3
                )

                ax_nfd.plot(
                    [x_right, x_diagram_right],
                    [y_base, y_base],
                    linewidth=1
                )

                ax_nfd.plot(
                    [x_right, x_diagram_right],
                    [y_top, y_top],
                    linewidth=1
                )

                ax_nfd.fill_betweenx(
                    [y_base, y_top],
                    x_right,
                    x_diagram_right,
                    alpha=0.20
                )

                ax_nfd.text(
                    x_diagram_right + frame_width * 0.025,
                    frame_height / 2,
                    f"{N_right_column:.2f} kip",
                    ha="left",
                    va="center",
                    rotation=90
                )


                # ------------------------------------------------------------
                # Formatting
                # ------------------------------------------------------------

                ax_nfd.set_title("Normal Force Diagram (NFD)")
                ax_nfd.set_xlabel("Horizontal Position (ft)")
                ax_nfd.set_ylabel("Elevation (ft)")

                ax_nfd.set_xlim(
                    -0.25 * frame_width,
                    1.25 * frame_width
                )

                ax_nfd.set_ylim(
                    -0.15 * frame_height,
                    1.35 * frame_height
                )

                ax_nfd.set_aspect("equal", adjustable="box")
                ax_nfd.grid(True, alpha=0.20)

                st.pyplot(fig_nfd, width="content")

                st.caption(
                    "Sign convention: positive axial force = tension; "
                    "negative axial force = compression."
                )

                # ------------------------------------------------------------
                # 8. SHEAR FORCE DIAGRAM
                # ------------------------------------------------------------

                st.subheader("8. Shear Force Diagram (SFD)")

                st.write(
                    "Shear-force distribution throughout the frame."
                )

                # ------------------------------------------------------------
                # Shear forces
                # ------------------------------------------------------------

                V_left_column = -Ax
                V_right_column = -Bx

                V_beam_left = Ay
                V_beam_right = Ay - P

                # Point-load position in feet
                load_x = vertical_load_location


                # ------------------------------------------------------------
                # Plot SFD
                # ------------------------------------------------------------

                fig_sfd, ax_sfd = plt.subplots(figsize=(6, 3.5))

                x_left = 0.0
                x_right = frame_width
                y_base = 0.0
                y_top = frame_height

                max_V = max(
                    abs(V_left_column),
                    abs(V_right_column),
                    abs(V_beam_left),
                    abs(V_beam_right),
                    1.0
                )

                offset_scale = 0.10


                # ------------------------------------------------------------
                # Draw frame centerlines
                # ------------------------------------------------------------

                ax_sfd.plot(
                    [x_left, x_left],
                    [y_base, y_top],
                    "k-",
                    linewidth=1.5
                )

                ax_sfd.plot(
                    [x_left, x_right],
                    [y_top, y_top],
                    "k-",
                    linewidth=1.5
                )

                ax_sfd.plot(
                    [x_right, x_right],
                    [y_top, y_base],
                    "k-",
                    linewidth=1.5
                )


                # ------------------------------------------------------------
                # Left-column shear
                # ------------------------------------------------------------

                left_offset = (
                    V_left_column / max_V
                ) * frame_width * offset_scale

                x_left_sfd = x_left + left_offset

                ax_sfd.plot(
                    [x_left_sfd, x_left_sfd],
                    [y_base, y_top],
                    linewidth=2.5
                )

                ax_sfd.fill_betweenx(
                    [y_base, y_top],
                    x_left,
                    x_left_sfd,
                    alpha=0.20
                )

                ax_sfd.plot(
                    [x_left, x_left_sfd],
                    [y_base, y_base],
                    linewidth=1
                )

                ax_sfd.plot(
                    [x_left, x_left_sfd],
                    [y_top, y_top],
                    linewidth=1
                )

                ax_sfd.text(
                    x_left_sfd - frame_width * 0.02,
                    frame_height / 2,
                    f"{V_left_column:.2f} kip",
                    ha="right",
                    va="center",
                    rotation=90
                )


                # ------------------------------------------------------------
                # Beam shear - left of point load
                # ------------------------------------------------------------

                beam_left_offset = (
                    V_beam_left / max_V
                ) * frame_height * offset_scale

                y_beam_left = y_top + beam_left_offset

                ax_sfd.plot(
                    [x_left, load_x],
                    [y_beam_left, y_beam_left],
                    linewidth=2.5
                )

                ax_sfd.fill_between(
                    [x_left, load_x],
                    y_top,
                    y_beam_left,
                    alpha=0.20
                )


                # ------------------------------------------------------------
                # Beam shear - right of point load
                # ------------------------------------------------------------

                beam_right_offset = (
                    V_beam_right / max_V
                ) * frame_height * offset_scale

                y_beam_right = y_top + beam_right_offset

                ax_sfd.plot(
                    [load_x, x_right],
                    [y_beam_right, y_beam_right],
                    linewidth=2.5
                )

                ax_sfd.fill_between(
                    [load_x, x_right],
                    y_top,
                    y_beam_right,
                    alpha=0.20
                )


                # ------------------------------------------------------------
                # Shear jump at point load
                # ------------------------------------------------------------

                ax_sfd.plot(
                    [load_x, load_x],
                    [y_beam_left, y_beam_right],
                    linewidth=2.5
                )


                # Beam shear labels

                ax_sfd.text(
                    load_x / 2,
                    y_beam_left + frame_height * 0.04,
                    f"{V_beam_left:.2f} kip",
                    ha="center",
                    va="bottom"
                )

                ax_sfd.text(
                    (load_x + x_right) / 2,
                    y_beam_right - frame_height * 0.04,
                    f"{V_beam_right:.2f} kip",
                    ha="center",
                    va="top"
                )


                # ------------------------------------------------------------
                # Right-column shear
                # ------------------------------------------------------------

                right_offset = (
                    V_right_column / max_V
                ) * frame_width * offset_scale

                x_right_sfd = x_right + right_offset

                ax_sfd.plot(
                    [x_right_sfd, x_right_sfd],
                    [y_base, y_top],
                    linewidth=2.5
                )

                ax_sfd.fill_betweenx(
                    [y_base, y_top],
                    x_right,
                    x_right_sfd,
                    alpha=0.20
                )

                ax_sfd.plot(
                    [x_right, x_right_sfd],
                    [y_base, y_base],
                    linewidth=1
                )

                ax_sfd.plot(
                    [x_right, x_right_sfd],
                    [y_top, y_top],
                    linewidth=1
                )

                ax_sfd.text(
                    x_right_sfd + frame_width * 0.02,
                    frame_height / 2,
                    f"{V_right_column:.2f} kip",
                    ha="left",
                    va="center",
                    rotation=90
                )


                # ------------------------------------------------------------
                # Formatting
                # ------------------------------------------------------------

                ax_sfd.set_title("Shear Force Diagram (SFD)")
                ax_sfd.set_xlabel("Horizontal Position (ft)")
                ax_sfd.set_ylabel("Elevation (ft)")

                ax_sfd.set_xlim(
                    -0.20 * frame_width,
                    1.20 * frame_width
                )

                ax_sfd.set_ylim(
                    -0.15 * frame_height,
                    1.25 * frame_height
                )

                ax_sfd.set_aspect("equal", adjustable="box")
                ax_sfd.grid(True, alpha=0.20)

                st.pyplot(fig_sfd, width="content")

                st.caption(
                    "The vertical jump in the beam SFD occurs at the applied point load."
                )

                # ------------------------------------------------------------
                # 9. BENDING MOMENT DIAGRAM
                # ------------------------------------------------------------

                st.subheader("9. Bending Moment Diagram (BMD)")

                st.write(
                    "Bending-moment distribution throughout the frame."
                )

                # ------------------------------------------------------------
                # Member-end moments in kip-ft
                # Local force-vector order:
                # [Ni, Vi, Mi, Nj, Vj, Mj]
                # ------------------------------------------------------------

                M_lc_base = left_column_forces[2] / 12.0
                M_lc_top = left_column_forces[5] / 12.0

                M_beam_left = beam_forces[2] / 12.0
                M_beam_right = beam_forces[5] / 12.0

                M_rc_top = right_column_forces[2] / 12.0
                M_rc_base = right_column_forces[5] / 12.0

                # ------------------------------------------------------------
                # Plot BMD
                # ------------------------------------------------------------

                fig_bmd, ax_bmd = plt.subplots(figsize=(6, 3.5))

                x_left = 0.0
                x_right = frame_width
                y_base = 0.0
                y_top = frame_height

                # Undeformed frame
                ax_bmd.plot(
                    [x_left, x_left],
                    [y_base, y_top],
                    "k-",
                    linewidth=1.5
                )

                ax_bmd.plot(
                    [x_left, x_right],
                    [y_top, y_top],
                    "k-",
                    linewidth=1.5
                )

                ax_bmd.plot(
                    [x_right, x_right],
                    [y_top, y_base],
                    "k-",
                    linewidth=1.5
                )

                # ------------------------------------------------------------
                # Scale moment offsets automatically
                # ------------------------------------------------------------

                max_M = max(
                    abs(M_lc_base),
                    abs(M_lc_top),
                    abs(M_beam_left),
                    abs(M_beam_right),
                    abs(M_rc_top),
                    abs(M_rc_base),
                    1.0
                )

                offset_scale = (
                    0.12 * min(frame_width, frame_height) / max_M
                )

                # ------------------------------------------------------------
                # Left column BMD
                # ------------------------------------------------------------

                lc_x_base = x_left + M_lc_base * offset_scale
                lc_x_top = x_left + M_lc_top * offset_scale

                ax_bmd.plot(
                    [lc_x_base, lc_x_top],
                    [y_base, y_top],
                    linewidth=2.5
                )

                ax_bmd.fill(
                    [x_left, lc_x_base, lc_x_top, x_left],
                    [y_base, y_base, y_top, y_top],
                    alpha=0.20
                )

                # ------------------------------------------------------------
                # Beam BMD
                #
                # Point load causes a change in slope at its location.
                # ------------------------------------------------------------

                load_x = vertical_load_location

                # Beam local end forces
                V_beam_left = beam_forces[1]
                V_beam_right = beam_forces[4]

                # For plotting the physical BMD, reverse the local i-end
                # moment sign so both ends use one continuous beam convention.
                M_plot_left = -beam_forces[2] / 12.0
                M_plot_right = beam_forces[5] / 12.0

                # No distributed load is present, so moment varies linearly
                # between concentrated-force locations.
                M_at_load = M_plot_left + V_beam_left * load_x

                beam_y_left = y_top + M_plot_left * offset_scale
                beam_y_load = y_top + M_at_load * offset_scale
                beam_y_right = y_top + M_plot_right * offset_scale

                ax_bmd.plot(
                    [x_left, load_x, x_right],
                    [beam_y_left, beam_y_load, beam_y_right],
                    linewidth=2.5
                )

                ax_bmd.fill(
                    [x_left, load_x, x_right, x_right, x_left],
                    [y_top, y_top, y_top, beam_y_right, beam_y_left],
                    alpha=0.20
                )

                # ------------------------------------------------------------
                # Right column BMD
                # ------------------------------------------------------------

                rc_x_top = x_right + M_rc_top * offset_scale
                rc_x_base = x_right + M_rc_base * offset_scale

                ax_bmd.plot(
                    [rc_x_top, rc_x_base],
                    [y_top, y_base],
                    linewidth=2.5
                )

                ax_bmd.fill(
                    [x_right, rc_x_top, rc_x_base, x_right],
                    [y_top, y_top, y_base, y_base],
                    alpha=0.20
                )

                # ------------------------------------------------------------
                # Moment labels
                # ------------------------------------------------------------

                # Left column base
                ax_bmd.text(
                    lc_x_base,
                    y_base,
                    f"{M_lc_base:.2f}",
                    fontsize=8,
                    va="bottom"
                )

                # Left beam-column joint
                # Display only the beam-side physical BMD value to avoid
                # duplicate member-end labels at the rigid joint.
                ax_bmd.text(
                    x_left,
                    beam_y_left,
                    f"{M_plot_left:.2f}",
                    fontsize=8,
                    ha="left",
                    va="bottom"
                )

                # Beam moment at point load
                # Only label this location when a vertical point load is actually present.
                if abs(vertical_load) > 1e-9:
                    ax_bmd.text(
                        load_x,
                        beam_y_load,
                        f"{M_at_load:.2f}",
                        fontsize=8,
                        ha="center",
                        va="bottom"
                    )

                # Right beam-column joint
                ax_bmd.text(
                    x_right,
                    beam_y_right,
                    f"{M_plot_right:.2f}",
                    fontsize=8,
                    ha="left",
                    va="bottom"
                )

                # Right column base
                ax_bmd.text(
                    rc_x_base,
                    y_base,
                    f"{M_rc_base:.2f}",
                    fontsize=8,
                    ha="left",
                    va="bottom"
                )
                # ------------------------------------------------------------
                # Plot formatting
                # ------------------------------------------------------------

                ax_bmd.set_title("Bending Moment Diagram (BMD)")
                ax_bmd.set_xlabel("Horizontal Position (ft)")
                ax_bmd.set_ylabel("Elevation (ft)")

                ax_bmd.grid(True, alpha=0.25)

                ax_bmd.set_aspect("equal", adjustable="datalim")

                plt.tight_layout()

                st.pyplot(
                    fig_bmd,
                    use_container_width=False
                )

                plt.close(fig_bmd)

                st.caption(
                    "Bending moments are shown in kip-ft."
                )

    # ============================================================
    # BEAM ANALYSIS
    # ============================================================

if analysis_module == "Beam Analysis":

    st.info(
        "Enter the beam geometry and loading conditions below, "
        "then select ANALYZE BEAM."
    )

    with st.expander("Analysis Assumptions"):

        st.markdown(
            """
            This tool assumes:

            - The beam is simply supported.
            - Support A is a pin.
            - Support B is a roller.
            - Loads act vertically downward.
            - Point loads act at specified locations.
            - Distributed loads are uniform over their specified regions.
            - The beam is analyzed using static equilibrium.
            - Self-weight is neglected unless entered as a distributed load.
            """
        )


    # ============================================================
    # 1. BEAM INFORMATION
    # ============================================================

    st.header("1. Beam Information")

    L = st.number_input(
        "Beam Length (ft)",
        min_value=1.0,
        value=20.0,
        step=1.0
    )


    # ============================================================
    # 2. POINT LOADS
    # ============================================================

    st.header("2. Point Loads")

    number_of_point_loads = st.number_input(
        "Number of Point Loads",
        min_value=0,
        max_value=6,
        value=1,
        step=1
    )

    point_loads = []

    for i in range(int(number_of_point_loads)):

        st.subheader(f"Point Load {i + 1}")

        col1, col2 = st.columns(2)

        with col1:

            P = st.number_input(
                f"Point Load {i + 1} Magnitude (kip)",
                min_value=0.0,
                value=10.0 if i == 0 else 5.0,
                step=1.0,
                key=f"P_{i}"
            )

        with col2:

            default_location = min(
                float(L),
                8.0 + i * 4.0
            )

            a = st.number_input(
                f"Point Load {i + 1} Location from A (ft)",
                min_value=0.0,
                max_value=float(L),
                value=float(default_location),
                step=1.0,
                key=f"a_{i}"
            )

        point_loads.append((P, a))


    # ============================================================
    # 3. DISTRIBUTED LOADS
    # ============================================================

    st.header("3. Uniform Distributed Loads (UDLs)")

    number_of_udls = st.number_input(
        "Number of Distributed Loads",
        min_value=0,
        max_value=4,
        value=0,
        step=1
    )

    udls = []

    for i in range(int(number_of_udls)):

        st.subheader(f"Distributed Load {i + 1}")

        col1, col2, col3 = st.columns(3)

        with col1:

            w = st.number_input(
                f"UDL {i + 1} Intensity (kip/ft)",
                min_value=0.0,
                value=2.0,
                step=0.5,
                key=f"w_{i}"
            )

        with col2:

            x_start = st.number_input(
                f"UDL {i + 1} Start Position (ft)",
                min_value=0.0,
                max_value=float(L),
                value=0.0,
                step=1.0,
                key=f"udl_start_{i}"
            )

        with col3:

            x_end = st.number_input(
                f"UDL {i + 1} End Position (ft)",
                min_value=0.0,
                max_value=float(L),
                value=float(L),
                step=1.0,
                key=f"udl_end_{i}"
            )

        if x_end <= x_start:

            st.warning(
                f"UDL {i + 1}: End position must be greater "
                f"than the start position."
            )

        udls.append((w, x_start, x_end))


    # ============================================================
    # 4. ANALYZE
    # ============================================================

    st.header("4. Structural Analysis")

    if "analyzed" not in st.session_state:
        st.session_state.analyzed = False

    if st.button(
        "ANALYZE BEAM",
        type="primary"
    ):
        st.session_state.analyzed = True

    analyze = st.session_state.analyzed

    if analyze:

        # --------------------------------------------------------
        # INPUT VALIDATION
        # --------------------------------------------------------

        valid_input = True

        for i, (w, x_start, x_end) in enumerate(udls):

            if x_end <= x_start:

                st.error(
                    f"Distributed Load {i + 1} has an invalid "
                    f"start/end position."
                )

                valid_input = False

        if not valid_input:

            st.stop()


        # ========================================================
        # SUPPORT REACTIONS
        # ========================================================

        # --------------------------------------------------------
        # Point-load contributions
        # --------------------------------------------------------

        total_point_load = sum(
            P for P, a in point_loads
        )

        point_moment_about_A = sum(
            P * a for P, a in point_loads
        )


        # --------------------------------------------------------
        # UDL contributions
        #
        # Equivalent resultant:
        #
        # W = w(length)
        #
        # Acts at the center of the loaded region.
        # --------------------------------------------------------

        total_udl_load = 0.0
        udl_moment_about_A = 0.0

        udl_resultants = []

        for w, x_start, x_end in udls:

            loaded_length = x_end - x_start

            W = w * loaded_length

            centroid = (
                x_start + x_end
            ) / 2

            total_udl_load += W

            udl_moment_about_A += (
                W * centroid
            )

            udl_resultants.append(
                (
                    W,
                    centroid,
                    loaded_length
                )
            )


        # --------------------------------------------------------
        # Total loading
        # --------------------------------------------------------

        total_load = (
            total_point_load
            +
            total_udl_load
        )

        total_moment_about_A = (
            point_moment_about_A
            +
            udl_moment_about_A
        )


        # --------------------------------------------------------
        # Reactions
        #
        # Sum MA = 0:
        #
        # RB(L) = total moment of applied loads about A
        #
        # Sum Fy = 0:
        #
        # RA + RB = total downward load
        # --------------------------------------------------------

        RB = total_moment_about_A / L

        RA = total_load - RB


        # ========================================================
        # DISPLAY REACTIONS
        # ========================================================

        st.subheader("Support Reactions")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Left Reaction, RA",
                f"{RA:.2f} kip"
            )

        with col2:

            st.metric(
                "Right Reaction, RB",
                f"{RB:.2f} kip"
            )


        # ========================================================
        # BEAM AND LOADING DIAGRAM
        # ========================================================

        st.subheader("Beam and Loading Diagram")

        fig, ax = plt.subplots(
            figsize=(8, 3)
        )


        # Beam
        ax.plot(
            [0, L],
            [0, 0],
            linewidth=4
        )


        # Pin support
        ax.plot(
            0,
            0,
            marker="^",
            markersize=18
        )


        # Roller support
        ax.plot(
            L,
            0,
            marker="o",
            markersize=14
        )


        # --------------------------------------------------------
        # Point loads
        # --------------------------------------------------------

        for P, a in point_loads:

            ax.annotate(
                "",
                xy=(a, 0.08),
                xytext=(a, 1.5),
                arrowprops=dict(
                    arrowstyle="->",
                    linewidth=2
                )
            )

            ax.text(
                a,
                1.65,
                f"{P:.1f} kip",
                horizontalalignment="center"
            )

            ax.text(
                a,
                -0.35,
                f"x = {a:.1f} ft",
                horizontalalignment="center"
            )


        # --------------------------------------------------------
        # Distributed loads
        # --------------------------------------------------------

        for w, x_start, x_end in udls:

            arrow_locations = np.linspace(
                x_start,
                x_end,
                9
            )

            for xpos in arrow_locations:

                ax.annotate(
                    "",
                    xy=(xpos, 0.08),
                    xytext=(xpos, 1.0),
                    arrowprops=dict(
                        arrowstyle="->",
                        linewidth=1.5
                    )
                )

            ax.plot(
                [x_start, x_end],
                [1.0, 1.0],
                linewidth=2
            )

            ax.text(
                (x_start + x_end) / 2,
                1.18,
                f"{w:.2f} kip/ft",
                horizontalalignment="center"
            )


        # Support labels
        ax.text(
            0,
            -0.65,
            "A - Pin",
            horizontalalignment="center"
        )

        ax.text(
            L,
            -0.65,
            "B - Roller",
            horizontalalignment="center"
        )


        ax.set_xlim(
            -0.05 * L,
            1.05 * L
        )

        ax.set_ylim(
            -1,
            2.2
        )

        ax.set_xlabel(
            "Position Along Beam (ft)"
        )

        ax.set_yticks([])

        ax.set_title(
            "Simply Supported Beam"
        )

        ax.grid(
            axis="x",
            alpha=0.3
        )

        st.pyplot(fig, width=850)

        plt.close(fig)


        # ========================================================
        # SHEAR AND MOMENT CALCULATIONS
        # ========================================================

        x = np.linspace(
            0,
            L,
            2001
        )

        V = np.zeros_like(x)

        M = np.zeros_like(x)


        for i, xi in enumerate(x):

            # Start with reaction at A
            shear = RA

            moment = RA * xi


            # ----------------------------------------------------
            # Point-load effects
            # ----------------------------------------------------

            for P, a in point_loads:

                if xi >= a:

                    shear -= P

                    moment -= (
                        P * (xi - a)
                    )


            # ----------------------------------------------------
            # Distributed-load effects
            # ----------------------------------------------------

            for w, x_start, x_end in udls:

                # Section is before the UDL
                if xi <= x_start:

                    loaded_length = 0.0


                # Section passes through the UDL
                elif xi < x_end:

                    loaded_length = (
                        xi - x_start
                    )


                # Section is after the entire UDL
                else:

                    loaded_length = (
                        x_end - x_start
                    )


                if loaded_length > 0:

                    W_partial = (
                        w * loaded_length
                    )

                    centroid_partial = (
                        x_start
                        +
                        loaded_length / 2
                    )

                    shear -= W_partial

                    moment -= (
                        W_partial
                        *
                        (
                            xi
                            -
                            centroid_partial
                        )
                    )


            V[i] = shear

            M[i] = moment


        # ========================================================
        # MAXIMUM MOMENT
        # ========================================================

        max_index = np.argmax(
            np.abs(M)
        )

        Mmax = M[max_index]

        xmax = x[max_index]


        st.subheader(
            "Maximum Bending Moment"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Maximum Moment",
                f"{Mmax:.2f} kip-ft"
            )

        with col2:

            st.metric(
                "Location from A",
                f"{xmax:.2f} ft"
            )


        # ========================================================
        # SHEAR FORCE DIAGRAM
        # ========================================================

        st.subheader(
            "Shear Force Diagram"
        )

        fig_shear, ax_shear = plt.subplots(
            figsize=(8, 3)
        )

        ax_shear.plot(
            x,
            V,
            linewidth=2
        )

        ax_shear.axhline(
            0,
            linewidth=1
        )

        ax_shear.fill_between(
            x,
            V,
            0,
            alpha=0.2
        )

        ax_shear.set_xlabel(
            "Position Along Beam (ft)"
        )

        ax_shear.set_ylabel(
            "Shear, V (kip)"
        )

        ax_shear.set_title(
            "Shear Force Diagram"
        )

        ax_shear.grid(
            alpha=0.3
        )

        st.pyplot(
            fig_shear, width=850
        )

        plt.close(
            fig_shear
        )


        # ========================================================
        # BENDING MOMENT DIAGRAM
        # ========================================================

        st.subheader(
            "Bending Moment Diagram"
        )

        fig_moment, ax_moment = plt.subplots(
            figsize=(8, 3)
        )

        ax_moment.plot(
            x,
            M,
            linewidth=2
        )

        ax_moment.axhline(
            0,
            linewidth=1
        )

        ax_moment.fill_between(
            x,
            M,
            0,
            alpha=0.2
        )

        ax_moment.plot(
            xmax,
            Mmax,
            marker="o"
        )


        # Put the Mmax label inside the graph
        # instead of overlapping the title.

        ax_moment.annotate(
            f"Mmax = {Mmax:.2f} kip-ft\n"
            f"x = {xmax:.2f} ft",
            xy=(xmax, Mmax),
            xytext=(15, -35),
            textcoords="offset points",
            arrowprops=dict(
                arrowstyle="->"
            )
        )

        ax_moment.set_xlabel(
            "Position Along Beam (ft)"
        )

        ax_moment.set_ylabel(
            "Moment, M (kip-ft)"
        )

        ax_moment.set_title(
            "Bending Moment Diagram"
        )

        ax_moment.grid(
            alpha=0.3
        )

        st.pyplot(
            fig_moment, width=850
        )

        plt.close(
            fig_moment
        )


        # ========================================================
        # STEP-BY-STEP CALCULATIONS
        # ========================================================

        st.subheader("Step-by-Step Calculations")

        st.write(
            "The support reactions are determined using "
            "the static-equilibrium equations."
        )

        st.latex(r"\sum F_y = 0")
        st.latex(r"\sum M_A = 0")


        # --------------------------------------------------------
        # APPLIED LOADS
        # --------------------------------------------------------

        st.markdown("### Applied Loads")

        if len(point_loads) > 0:

            st.markdown("**Point Loads**")

            for i, (P, a) in enumerate(point_loads):

                st.write(
                    f"Point Load {i + 1}: "
                    f"{P:.2f} kip at x = {a:.2f} ft"
                )


        if len(udls) > 0:

            st.markdown("**Uniform Distributed Loads**")

            for i, (w, x_start, x_end) in enumerate(udls):

                loaded_length = x_end - x_start
                W = w * loaded_length
                centroid = (x_start + x_end) / 2

                st.write(
                    f"UDL {i + 1}: "
                    f"{w:.2f} kip/ft from "
                    f"x = {x_start:.2f} ft to "
                    f"x = {x_end:.2f} ft"
                )

                st.latex(
                    rf"W_{{{i+1}}} = wL"
                    rf" = ({w:.2f})({loaded_length:.2f})"
                    rf" = {W:.2f}\text{{ kip}}"
                )

                st.write(
                    f"Equivalent resultant acts at "
                    f"x = {centroid:.2f} ft."
                )


        # --------------------------------------------------------
        # TOTAL LOAD
        # --------------------------------------------------------

        st.markdown("### Total Applied Load")

        st.latex(
            rf"\sum P = {total_load:.2f}\text{{ kip}}"
        )


        # --------------------------------------------------------
        # MOMENT EQUILIBRIUM
        # --------------------------------------------------------

        st.markdown("### Moment Equilibrium About Support A")

        st.latex(r"\sum M_A = 0")

        st.write(
            "Taking moments about Support A eliminates "
            "the unknown reaction RA."
        )

        moment_terms = []

        for P, a in point_loads:

            moment_terms.append(
                f"({P:.2f})({a:.2f})"
            )

        for w, x_start, x_end in udls:

            loaded_length = x_end - x_start
            W = w * loaded_length
            centroid = (x_start + x_end) / 2

            moment_terms.append(
                f"({W:.2f})({centroid:.2f})"
            )

        if moment_terms:

            applied_moment_text = " + ".join(moment_terms)

        else:

            applied_moment_text = "0"


        st.write(
            f"RB({L:.2f}) = {applied_moment_text}"
        )

        st.write(
            f"RB({L:.2f}) = "
            f"{total_moment_about_A:.2f} kip-ft"
        )

        st.latex(
            rf"R_B = "
            rf"\frac{{{total_moment_about_A:.2f}}}"
            rf"{{{L:.2f}}}"
            rf" = {RB:.2f}\text{{ kip}}"
        )


        # --------------------------------------------------------
        # VERTICAL EQUILIBRIUM
        # --------------------------------------------------------

        st.markdown("### Vertical Force Equilibrium")

        st.latex(r"\sum F_y = 0")

        st.write(
            f"RA + RB - Total Load = 0"
        )

        st.write(
            f"RA + {RB:.2f} - {total_load:.2f} = 0"
        )

        st.latex(
            rf"R_A = "
            rf"{total_load:.2f} - {RB:.2f}"
            rf" = {RA:.2f}\text{{ kip}}"
        )


        # --------------------------------------------------------
        # FINAL REACTION SUMMARY
        # --------------------------------------------------------

        st.markdown("### Reaction Summary")

        summary_col1, summary_col2 = st.columns(2)

        with summary_col1:

            st.success(
                f"RA = {RA:.2f} kip"
            )

        with summary_col2:

            st.success(
                f"RB = {RB:.2f} kip"
            )
        # ========================================================
        # ENGINEERING VERIFICATION
        # ========================================================

        st.subheader(
            "Engineering Verification"
        )

        vertical_error = (
            RA
            +
            RB
            -
            total_load
        )

        moment_error = (
            RB * L
            -
            total_moment_about_A
        )

        st.write(
            f"ΣFy residual: "
            f"{vertical_error:.6f} kip"
        )

        st.write(
            f"ΣMA residual: "
            f"{moment_error:.6f} kip-ft"
        )


        if (
            abs(vertical_error) < 0.0001
            and
            abs(moment_error) < 0.0001
        ):

            st.success(
                "Equilibrium checks satisfied."
            )

        else:

            st.error(
                "Equilibrium check failed."
            )
    # ========================================================
    # HAND CALCULATION COMPARISON
    # ========================================================

    st.subheader("Hand-Calculation Verification")

    st.write(
        """
        Enter independently calculated support reactions below
        to compare your hand calculations with the program results.
        """
    )

    hand_col1, hand_col2 = st.columns(2)

    with hand_col1:
        hand_RA = st.number_input(
            "Hand-Calculated RA (kip)",
            value=0.0,
            step=0.01,
            key="hand_RA"
        )

    with hand_col2:
        hand_RB = st.number_input(
            "Hand-Calculated RB (kip)",
            value=0.0,
            step=0.01,
            key="hand_RB"
        )

    compare = st.button(
        "COMPARE HAND CALCULATION"
    )

    if compare:

        RA_difference = hand_RA - RA
        RB_difference = hand_RB - RB

        st.markdown("### Comparison Results")

        st.write(
            f"**RA:** Tool = {RA:.2f} kip | "
            f"Hand = {hand_RA:.2f} kip | "
            f"Difference = {RA_difference:.4f} kip"
        )

        st.write(
            f"**RB:** Tool = {RB:.2f} kip | "
            f"Hand = {hand_RB:.2f} kip | "
            f"Difference = {RB_difference:.4f} kip"
        )

        tolerance = 0.01

        if (
            abs(RA_difference) <= tolerance
            and
            abs(RB_difference) <= tolerance
        ):

            st.success(
                "✓ Hand calculations agree with the program results."
            )

        else:

            st.warning(
                "Hand calculations and program results differ. "
                "Review the calculations."
            )

# ============================================================
# DISCLAIMER
# ============================================================

st.divider()

st.caption(
    """
    Educational structural-analysis tool.
    Results should be independently verified using
    accepted structural-analysis methods.
    """
)