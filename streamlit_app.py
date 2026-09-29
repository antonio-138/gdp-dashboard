import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Structural Beam Analyzer",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Structural Beam Analyzer")

st.write(
    """
    Analyze a simply supported beam subjected to downward point loads.

    Enter the beam length and load information below.
    The program calculates the support reactions and generates
    the shear-force and bending-moment diagrams.
    """
)


# --------------------------------------------------
# BEAM INPUT
# --------------------------------------------------

st.header("1. Beam Information")

L = st.number_input(
    "Beam Length (ft)",
    min_value=1.0,
    value=20.0,
    step=1.0
)


# --------------------------------------------------
# LOAD INPUT
# --------------------------------------------------

st.header("2. Point Loads")

number_of_loads = st.number_input(
    "Number of Point Loads",
    min_value=1,
    max_value=4,
    value=1,
    step=1
)

loads = []

for i in range(int(number_of_loads)):

    st.subheader(f"Load {i + 1}")

    col1, col2 = st.columns(2)

    with col1:

        P = st.number_input(
            f"Load {i + 1} Magnitude (kip)",
            min_value=0.0,
            value=10.0 if i == 0 else 5.0,
            step=1.0,
            key=f"P{i}"
        )

    with col2:

        default_location = min(
            L,
            8.0 + i * 4.0
        )

        a = st.number_input(
            f"Load {i + 1} Location from Left Support (ft)",
            min_value=0.0,
            max_value=float(L),
            value=float(default_location),
            step=1.0,
            key=f"a{i}"
        )

    loads.append((P, a))


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

st.header("3. Structural Analysis")

analyze = st.button(
    "ANALYZE BEAM",
    type="primary"
)


if analyze:

    # ----------------------------------------------
    # SUPPORT REACTIONS
    # ----------------------------------------------

    total_load = sum(P for P, a in loads)

    moment_about_A = sum(P * a for P, a in loads)

    RB = moment_about_A / L

    RA = total_load - RB


    # ----------------------------------------------
    # DISPLAY REACTIONS
    # ----------------------------------------------

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


    # ----------------------------------------------
    # DRAW THE BEAM
    # ----------------------------------------------

    st.subheader("Beam and Loading Diagram")

    fig, ax = plt.subplots(figsize=(12, 4))

    # Beam
    ax.plot(
        [0, L],
        [0, 0],
        linewidth=4
    )

    # Left support
    ax.plot(
        0,
        0,
        marker="^",
        markersize=18
    )

    # Right support
    ax.plot(
        L,
        0,
        marker="o",
        markersize=14
    )

    # Draw loads
    for P, a in loads:

        ax.annotate(
            "",
            xy=(a, 0.1),
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

    ax.set_xlim(-0.05 * L, 1.05 * L)

    ax.set_ylim(-1, 2.3)

    ax.set_xlabel("Position Along Beam (ft)")

    ax.set_yticks([])

    ax.set_title("Simply Supported Beam")

    ax.grid(axis="x", alpha=0.3)

    st.pyplot(fig)

    plt.close(fig)


    # ----------------------------------------------
    # CALCULATE SHEAR AND MOMENT
    # ----------------------------------------------

    x = np.linspace(
        0,
        L,
        1001
    )

    V = np.zeros_like(x)

    M = np.zeros_like(x)

    for i, xi in enumerate(x):

        # Start with left support reaction
        shear = RA

        moment = RA * xi

        # Include every load to the left
        # of the section being analyzed
        for P, a in loads:

            if xi >= a:

                shear -= P

                moment -= P * (xi - a)

        V[i] = shear

        M[i] = moment


    # ----------------------------------------------
    # MAXIMUM MOMENT
    # ----------------------------------------------

    max_index = np.argmax(np.abs(M))

    Mmax = M[max_index]

    xmax = x[max_index]


    st.subheader("Maximum Bending Moment")

    st.metric(
        "Maximum Moment",
        f"{Mmax:.2f} kip-ft"
    )

    st.write(
        f"Location of maximum moment: "
        f"{xmax:.2f} ft from Support A"
    )


    # ----------------------------------------------
    # SHEAR FORCE DIAGRAM
    # ----------------------------------------------

    st.subheader("Shear Force Diagram")

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

    ax_shear.grid(alpha=0.3)

    st.pyplot(fig_shear)

    plt.close(fig_shear)


    # ----------------------------------------------
    # BENDING MOMENT DIAGRAM
    # ----------------------------------------------

    st.subheader("Bending Moment Diagram")

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

    ax_moment.annotate(
        f"Mmax = {Mmax:.2f} kip-ft",
        xy=(xmax, Mmax),
        xytext=(10, 20),
        textcoords="offset points"
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

    ax_moment.grid(alpha=0.3)

    st.pyplot(fig_moment)

    plt.close(fig_moment)


    # ----------------------------------------------
    # EQUILIBRIUM CHECK
    # ----------------------------------------------

    st.subheader("Engineering Verification")

    vertical_error = (
        RA + RB - total_load
    )

    moment_error = (
        RB * L - moment_about_A
    )

    st.write(
        f"ΣFy check: {vertical_error:.6f} kip"
    )

    st.write(
        f"ΣMA check: {moment_error:.6f} kip-ft"
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


# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------

st.divider()

st.caption(
    """
    Educational structural-analysis tool.
    Results should be independently verified using
    accepted structural-analysis methods.
    """
)