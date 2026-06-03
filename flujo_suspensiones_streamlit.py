import streamlit as st
import math
from pathlib import Path

st.set_page_config(
    page_title="Flujo sólido-líquido en tuberías",
    layout="wide"
)

# Diseño general de la página
# Esto es solo para modificar tamaños de letra, espaciados, etc.
st.markdown("""
<style>
    .block-container {
        padding-top: 0.8rem;
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0.2rem;
    }

    section[data-testid="stSidebar"] hr {
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
    }

    section[data-testid="stSidebar"] h4 {
        margin-top: 0.4rem;
        margin-bottom: 0.4rem;
    }

    section[data-testid="stSidebar"] p {
        margin-bottom: 0.4rem;
    }

    .small-note {
        font-size: 14px;
        color: gray;
        line-height: 1.35;
    }
    
    .subtitulo-ecuacion {
        font-size: 20px;
        font-weight: 600;
        color: #000000;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }
    
    /* Hace más pequeños los números de st.metric */
    div[data-testid="stMetricValue"] {
        font-size: 18px !important;
    }
    
</style>
""", unsafe_allow_html=True)

# Imágenes régimen de flujo
# Es para la sección de visualización

BASE_DIR = Path(__file__).parent

IMG_HOMOGENEO = BASE_DIR / "flujo_homogeneo.png"
IMG_HETEROGENEO = BASE_DIR / "flujo_heterogeneo.png"
IMG_SALTACION = BASE_DIR / "flujo_saltacion.png"

# Otras funciones
def to_float(nombre: str, valor: str) -> float:
    """Convierte texto a número y avisa cuál dato falta."""
    if valor.strip() == "":
        raise ValueError(f"Falta el dato: {nombre}")
    return float(valor)


def mostrar_imagen(path: Path, caption: str, ayuda: str = ""):
    """Muestra una imagen si existe. Si no existe, deja una guía clara."""
    if path.exists():
        st.image(path, caption=caption, width="stretch")
    else:
        st.warning(f"No encontré la imagen: {path.name}")
        if ayuda:
            st.markdown(ayuda)


# Título y secciones
st.title("Flujo sólido-líquido en tuberías horizontales")
st.caption("Separación, dispersión y condición crítica de suspensión en suspensiones sólido-líquido diluidas.")

Seccion = st.segmented_control(
    "Seleccione una sección",
    ["Ecuaciones", "Cálculos", "Visualización"],
    default="Ecuaciones"
)

# Sidebar según la sección que se escoja

with st.sidebar:
    if Seccion == "Ecuaciones":
        st.markdown("## Mecánica de fluidos II")

        st.divider()
        st.markdown(
            """
            <p style='font-size: 14px; color: black;'>
            En esta sección se encuentran las ecuaciones de flujo en suspensiones sólido-líquido.<br>
            Estas ecuaciones fueron obtenidas del documento: <i>Fundamentals of Multiphase Flows</i>.
            <a href="https://doi.org/10.1017/CBO9780511807169" target="_blank">Enlace DOI</a><br>
            ISBN: 0521 848040
            </p>
            """,
            unsafe_allow_html=True
        )
        
        st.divider()
        st.markdown(
            """
            <p style='font-size: 14px; color: black;'>
            Las expresiones presentadas son criterios aproximados para analizar la separación
            y suspensión de partículas en flujo horizontal.<br>
            Algunas ecuaciones provienen de balances físicos, mientras que otras incluyen
            constantes y correlaciones empíricas usadas para estimar la transición entre
            saltación, flujo heterogéneo y suspensión.
            </p>
            """,
            unsafe_allow_html=True
        )

        st.divider()
        st.markdown(
            """
            <p style='font-size: 14px; color: black;'>
            Mecánica de Fluidos II<br>
            Profesor: Pedro Orozco Cury<br>
            Realizado por: Grupo 6
            </p>
            """,
            unsafe_allow_html=True
        )

    elif Seccion == "Cálculos":
        st.markdown("## Configuración del cálculo")
        st.caption("Seleccione el régimen usado para calcular la velocidad de separación")
        st.divider()

        Regimen_Wp = st.selectbox(
            "Régimen para calcular Wp",
            [
                "Dominan efectos inerciales",
                "Domina efecto viscoso"
            ]
        )

        st.markdown("#### Ecuación seleccionada")

        if Regimen_Wp == "Domina efecto viscoso":
            st.latex(r"""
            W_p=\frac{2R^2g}{9\nu_C}\left(\frac{\Delta\rho}{\rho_C}\right)
            """)
            st.caption(r"Se recomienda cuando $2W_pR/\nu_C \ll 1$.")
        else:
            st.latex(r"""
            W_p=\left[\frac{2Rg}{3C_D}\left(\frac{\Delta\rho}{\rho_C}\right)\right]^{1/2}
            """)
            st.caption(r"Se recomienda cuando $2W_pR/\nu_C \gg 1$.")

        st.divider()
        st.markdown("#### Criterio de interpretación")
        st.latex(r"""
        \frac{W_p}{W_t}=K
        """)
        st.markdown(
            r"Si $W_p/W_t<K$, predomina la mezcla turbulenta. "
            r"Si $W_p/W_t>K$, predomina la separación/sedimentación."
        )

    elif Seccion == "Visualización":
        st.markdown("## Guía visual")

        st.divider()
        st.markdown(
            """
            <p style='font-size: 14px; color: black;'>
            En esta sección se muestran los principales regímenes de flujo en una suspensión sólido-líquido
            dentro de una tubería horizontal.
            </p>
            """,
            unsafe_allow_html=True
        )

        st.divider()
        st.markdown(
            """
            <p style='font-size: 14px; color: #000000;'>
            Regímenes de flujo en suspensiones sólido-líquido
            <ul style='font-size: 14px; color: #000000; padding-left: 20px;'>
            <li><b>Homogéneo:</b> partículas distribuidas en toda la tubería.</li>
            <li><b>Heterogéneo:</b> mayor concentración de partículas cerca del fondo.</li>
            <li><b>Saltación:</b> partículas acumuladas en el fondo, con movimiento por pequeños saltos.</li>
            </ul>
            """,
            unsafe_allow_html=True
        )
        


# Sección 1: Ecuaciones

if Seccion == "Ecuaciones":
    st.markdown(
    "<h2 style='text-align: center; margin-top: 0.2rem; margin-bottom: 0.2rem;'>Ecuaciones principales</h2>",
    unsafe_allow_html=True
    )
    
    st.markdown(
        "<div class='subtitulo-ecuacion'>1. Criterio general de separación y mezcla</div>",
        unsafe_allow_html=True
        )
    c1, c2 = st.columns([1, 2])

    with c1:
        st.latex(r"""
        \frac{W_p}{W_t}
        """)

    with c2:
        st.markdown(
            r"$W_p$: velocidad de separación de la fase dispersa.  "
            r"$W_t$: velocidad turbulenta o velocidad típica de mezcla del fluido."
        )
        st.markdown(
            "Este criterio permite evaluar si predomina la tendencia a separarse "
            "o la capacidad de la turbulencia para mantener las partículas suspendidas."
        )

    st.divider()

    st.markdown(
        "<div class='subtitulo-ecuacion'>2. Condición crítica de transición</div>",
        unsafe_allow_html=True
        )
    st.latex(r"""
    \frac{W_p}{W_t}=K
    """)
    st.markdown(
        r"Cuando la relación alcanza el valor crítico $K$, el sistema está cerca del límite "
        r"entre suspensión y sedimentación."
    )

    st.divider()

    st.markdown(
        "<div class='subtitulo-ecuacion'>3. Velocidad de separación de la partícula</div>",
        unsafe_allow_html=True
        )
    c1, barra, c2 = st.columns([1, 0.05, 1])

    with c1:
        st.markdown("<p style='font-size: 18px; font-weight: 600; color: black;'>Caso viscoso</p>", unsafe_allow_html=True)
        st.latex(r"""
        W_p=\frac{2R^2g}{9\nu_C}\left(\frac{\Delta\rho}{\rho_C}\right)
        """)
        st.markdown(r"Se usa cuando:")
        st.latex(r"""
        \frac{2W_pR}{\nu_C}\ll 1
        """)
        st.caption("La partícula se mueve lento o el fluido ofrece una resistencia viscosa dominante.")

    with barra:
        st.markdown(
        """
        <div style="
            border-left: 2px solid #6109c0;
            height: 310px;
            margin: 10px auto;
        "></div>
        """,
        unsafe_allow_html=True
        )

    with c2:
        st.markdown("<p style='font-size: 18px; font-weight: 600; color: black;'>Caso inercial</p>", unsafe_allow_html=True)
        st.latex(r"""
        W_p=\left[\frac{2Rg}{3C_D}\left(\frac{\Delta\rho}{\rho_C}\right)\right]^{1/2}
        """)
        st.markdown(r"Se usa cuando:")
        st.latex(r"""
        \frac{2W_pR}{\nu_C}\gg 1
        """)
        st.caption("La partícula se separa con mayor influencia de la inercia y del coeficiente de arrastre.")

    st.divider()

    st.markdown(
        "<div class='subtitulo-ecuacion'>4. Velocidad turbulenta</div>",
        unsafe_allow_html=True
        )
    st.latex(r"""
    W_t\approx\left(\frac{\tau_w}{\rho_C}\right)^{1/2}
    """)
    st.markdown("También puede expresarse como:")
    st.latex(r"""
    W_t\approx\left[\frac{d}{4\rho_C}\left(-\frac{dp}{ds}\right)\right]^{1/2}
    """)
    st.markdown(
        "A mayor turbulencia, mayor capacidad del fluido para mantener las partículas suspendidas."
    )

    st.divider()

    st.markdown(
        "<div class='subtitulo-ecuacion'>5. Velocidad superficial crítica</div>",
        unsafe_allow_html=True
        )
    st.latex(r"""
    j_c=\left[\frac{17.2}{K^2C_D}\frac{gR d^{1/4}}{\nu_C^{1/4}}\left(\frac{\Delta\rho}{\rho_C}\right)\right]^{4/7}
    """)

    c1, c2 = st.columns(2)
    with c1:
        st.success(r"Si $j>j_c$: hay suficiente intensidad para pasar de saltación a flujo heterogéneo.")
    with c2:
        st.warning(r"Si $j<j_c$: las partículas tienden a formar o mantener un lecho en el fondo.")

    st.info(
        r"Nota importante: $j_c$ no es un caudal volumétrico en $m^3/s$. "
        r"Es un flujo volumétrico por unidad de área, por eso sus unidades son $m/s$. "
        r"También puede llamarse velocidad superficial crítica."
    )

# Sección 2: Cálculos

elif Seccion == "Cálculos":
    st.subheader("Cálculo de suspensión sólido-líquido en tubería horizontal")

    st.markdown(
        "Ingrese los datos en sus respectivas unidades. En estos cálculos se obtiene la velocidad de separación, "
        "la velocidad turbulenta, la relación crítica y la velocidad superficial crítica."
    )

    with st.form("Datos_suspension"):
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### Propiedades y partícula")
            K_txt = st.text_input(r"Constante crítica $K$ (adimensional)",
                                placeholder="Ej: 1")
            CD_txt = st.text_input(r"Coeficiente de arrastre $C_D$ (adimensional)", 
                                placeholder="Ej: 1")
            R_mm_txt = st.text_input(r"Radio de partícula $R$ (mm)",
                                placeholder="Ej: 3")
            rho_s_txt = st.text_input(r"Densidad del sólido $\rho_s$ (kg/m³)",
                                placeholder="Ej: 2650")
            rho_c_txt = st.text_input(r"Densidad del fluido continuo $\rho_C$ (kg/m³)",
                                placeholder="Ej: 1000")
            nu_c_txt = st.text_input(r"Viscosidad cinemática $\nu_C$ (m²/s)",
                                placeholder="Ej: 1e-6")

        with c2:
            st.markdown("#### Tubería y flujo")
            d_txt = st.text_input(r"Diámetro interno de tubería $d$ (m)",
                                placeholder="Ej: 0.05")
            gradp_txt = st.text_input(r"Gradiente de presión $-dp/ds$ (Pa/m)", 
                                placeholder="Ej: 5000")
            j_txt = st.text_input(r"Velocidad superficial real $j$ (m/s)",
                                placeholder="Ej: 5")

        calcular = st.form_submit_button("Calcular")

    if calcular:
        try:
            K = to_float("K", K_txt)
            CD = to_float("CD", CD_txt)
            R_mm = to_float("R", R_mm_txt)
            rho_s = to_float("rho_s", rho_s_txt)
            rho_c = to_float("rho_c", rho_c_txt)
            nu_c = to_float("nu_c", nu_c_txt)
            d = to_float("d", d_txt)
            gradp = to_float("-dp/ds", gradp_txt)
            j = to_float("j", j_txt)

            R = R_mm / 1000
            g = 9.81
            delta_rho = rho_s - rho_c

            if delta_rho <= 0:
                st.error("La diferencia de densidad debe ser positiva para sedimentación de sólido en líquido.")
                st.stop()

            # Cálculo de Wp según la selección del sidebar
            if Regimen_Wp == "Domina efecto viscoso":
                Wp = (2 * R**2 * g / (9 * nu_c)) * (delta_rho / rho_c)
            else:
                Wp = math.sqrt((2 * R * g / (3 * CD)) * (delta_rho / rho_c))

            # Velocidad turbulenta
            Wt = math.sqrt((d / (4 * rho_c)) * gradp)

            # Relación crítica
            relacion = Wp / Wt

            # Número usado para revisar si la selección de régimen tiene sentido
            criterio_regimen = (2 * Wp * R) / nu_c

            # Velocidad superficial crítica jc
            jc = (
                (17.2 / (K**2 * CD))
                * ((g * R * d**0.25) / (nu_c**0.25))
                * (delta_rho / rho_c)
            ) ** (4 / 7)

            st.markdown("### Resultados")
            r1, r2, r3, r4 = st.columns(4)
            with r1:
                st.metric(r"$\Delta\rho$", f"{delta_rho:,.2f} kg/m³")
                st.metric(r"$W_p$", f"{Wp:.4f} m/s")
            with r2:
                st.metric(r"$W_t$", f"{Wt:.4f} m/s")
                st.metric(r"$W_p/W_t$", f"{relacion:.4f}")
            with r3:
                st.metric(r"$j_c$", f"{jc:.4f} m/s")
                st.metric(r"$j$", f"{j:.4f} m/s")
            with r4:
                st.metric(r"$2W_pR/\nu_C$", f"{criterio_regimen:.2f}")
                

            st.markdown("### Interpretación")

            if relacion < K:
                st.success(
                    r"Como $W_p/W_t<K$, la mezcla turbulenta supera la tendencia de separación. "
                    r"Las partículas pueden mantenerse suspendidas."
                )
            elif math.isclose(relacion, K, rel_tol=0.05):
                st.warning(
                    r"Como $W_p/W_t\approx K$, el sistema está cerca de la condición crítica "
                    r"entre suspensión y sedimentación."
                )
            else:
                st.error(
                    r"Como $W_p/W_t>K$, la tendencia de separación es mayor que la mezcla turbulenta. "
                    r"Las partículas tienden a sedimentarse."
                )

            if j > jc:
                st.success(
                    r"Como $j>j_c$, el flujo tiene suficiente intensidad para pasar de saltación "
                    r"a flujo heterogéneo."
                )
            else:
                st.warning(
                    r"Como $j<j_c$, las partículas tienden a formar o mantener un lecho en el fondo."
                )

            # Aviso de consistencia del régimen seleccionado
            st.markdown("### Revisión del régimen usado para $W_p$")
            if criterio_regimen < 1 and Regimen_Wp == "Dominan efectos inerciales":
                st.warning(
                    r"El criterio $2W_pR/\nu_C$ es menor que 1. "
                    r"Puede que el caso viscoso sea más apropiado."
                )
            elif criterio_regimen > 1 and Regimen_Wp == "Domina efecto viscoso":
                st.warning(
                    r"El criterio $2W_pR/\nu_C$ es mayor que 1. "
                    r"Puede que el caso inercial sea más apropiado."
                )
            else:
                st.info("La selección del régimen es razonable según el criterio calculado.")

            st.markdown("### Desarrollo usado")
            st.latex(r"""
            \Delta\rho=\rho_s-\rho_C
            """)

            if Regimen_Wp == "Domina efecto viscoso":
                st.latex(r"""
                W_p=\frac{2R^2g}{9\nu_C}\left(\frac{\Delta\rho}{\rho_C}\right)
                """)
            else:
                st.latex(r"""
                W_p=\left[\frac{2Rg}{3C_D}\left(\frac{\Delta\rho}{\rho_C}\right)\right]^{1/2}
                """)

            st.latex(r"""
            W_t\approx\left[\frac{d}{4\rho_C}\left(-\frac{dp}{ds}\right)\right]^{1/2}
            """)

            st.latex(r"""
            \frac{W_p}{W_t}=\text{relación entre separación y mezcla turbulenta}
            """)

            st.latex(r"""
            j_c=\left[\frac{17.2}{K^2C_D}\frac{gR d^{1/4}}{\nu_C^{1/4}}\left(\frac{\Delta\rho}{\rho_C}\right)\right]^{4/7}
            """)

        except ValueError as e:
            st.error(str(e))
        except Exception:
            st.error("Hay un dato inválido. Usa solo números y punto decimal, por ejemplo: 5, 0.05 o 1e-6.")


# Sección 3: Visualización

elif Seccion == "Visualización":
    st.subheader("Visualización de regímenes de flujo en suspensiones sólido-líquido")

    Regimen_visual = st.selectbox(
        "Seleccione el régimen que desea visualizar",
        [
            "Seleccione una opción",
            "Flujo homogéneo",
            "Flujo heterogéneo",
            "Flujo con saltación"
        ]
    )

    if Regimen_visual == "Flujo homogéneo":
        st.markdown("### Flujo homogéneo")
        st.markdown(
            "Las partículas están distribuidas uniformemente. "
            "La mezcla se comporta como una suspensión más uniforme."
        )
        mostrar_imagen(
            IMG_HOMOGENEO,
            "Flujo homogéneo: partículas distribuidas en toda la tubería.",
        )

    elif Regimen_visual == "Flujo heterogéneo":
        st.markdown("### Flujo heterogéneo")
        st.markdown(
            "Las partículas siguen suspendidas, pero su concentración es mayor en la zona inferior "
            "de la tubería por efecto de la gravedad."
        )
        mostrar_imagen(
            IMG_HETEROGENEO,
            "Flujo heterogéneo: mayor concentración de partículas en la parte inferior.",
        )

    elif Regimen_visual == "Flujo con saltación":
        st.markdown("### Flujo con saltación")
        st.markdown(
            "Las partículas más pesadas tienden a acumularse en el fondo de la tubería. "
            "Algunas son levantadas temporalmente por el flujo y avanzan dando pequeños saltos, "
            "mientras otras permanecen cerca del fondo."
        )
        mostrar_imagen(
            IMG_SALTACION,
            "Saltación: partículas acumuladas en el fondo y movimiento por saltos.",
        )

    else:
        st.info("Seleccione un régimen para ver su explicación e imagen.")

# cd "Fluidos II"
# py -3.13 -m streamlit run flujo_suspensiones_streamlit.py
