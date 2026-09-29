import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="Structural Beam Analyzer",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Structural Beam Analysis Tool")

st.markdown(
    """
    **AI-Assisted Structural Analysis Project**

    Analyze a simply supported beam subjected to point loads
    and uniform distributed loads. The tool calculates support
    reactions, shear forces, bending moments, and automatically
    generates structural diagrams.
    """
)

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
        figsize=(12, 4)
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

    st.pyplot(fig)

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
        figsize=(12, 4)
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
        fig_shear
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
        figsize=(12, 4)
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
        fig_moment
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