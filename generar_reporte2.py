import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import pandas as pd
import numpy as np
from datetime import datetime
import os

# Paleta de colores moderna y profesional
COLORS = {
    'primary': '#2D3250',      # Azul oscuro moderno
    'secondary': '#424769',    # Azul grisáceo elegante
    'accent': '#7077A1',       # Lavanda suave
    'highlight': '#F6B17A',    # Naranja coral cálido
    'text': '#2D3250',         # Azul oscuro para texto
    'light_gray': '#B8B8D1',   # Gris lavanda claro
    'bg': '#F5F5F7',           # Fondo gris claro moderno
    'white': '#FFFFFF',        # Blanco puro
    'success': '#5AB2A8',      # Verde azulado moderno
    'warning': '#FF9A76',      # Coral
    'gradient_1': '#667BC6',   # Azul vibrante
    'gradient_2': '#DA7297',   # Rosa suave
}

def configurar_estilo():
    """Configura el estilo general de matplotlib con tema moderno"""
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['figure.facecolor'] = COLORS['bg']
    plt.rcParams['axes.facecolor'] = COLORS['white']
    plt.rcParams['axes.edgecolor'] = COLORS['accent']
    plt.rcParams['axes.labelcolor'] = COLORS['text']
    plt.rcParams['text.color'] = COLORS['text']
    plt.rcParams['xtick.color'] = COLORS['secondary']
    plt.rcParams['ytick.color'] = COLORS['secondary']
    plt.rcParams['grid.color'] = COLORS['light_gray']
    plt.rcParams['grid.alpha'] = 0.25
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['font.size'] = 10
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Helvetica Neue', 'Arial', 'Helvetica', 'DejaVu Sans']

def formatear_moneda(valor):
    """Formatea valores como moneda colombiana"""
    return f"${valor:,.0f} COP".replace(",", ".")

def generar_reporte_visual(df, ruta_salida="reporte_facturas.png"):
    """
    Genera un reporte visual profesional estilo dashboard
    
    Args:
        df: DataFrame con las facturas procesadas
        ruta_salida: Ruta donde guardar el reporte
    """
    # Validar que el DataFrame no esté vacío
    if df is None or df.empty:
        print("⚠️  No hay datos para generar el reporte visual")
        return None
    
    # Validar columnas mínimas requeridas
    columnas_requeridas = ['proveedor', 'importe']
    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
    
    if columnas_faltantes:
        print(f"⚠️  Faltan columnas requeridas en el DataFrame: {columnas_faltantes}")
        return None
    
    configurar_estilo()
    
    # Crear figura con diseño de grid personalizado
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3,
                  left=0.08, right=0.95, top=0.92, bottom=0.08)
    
    # ========== ENCABEZADO ==========
    fig.text(0.5, 0.96, 'REPORTE DE FACTURAS PROCESADAS', 
             ha='center', va='top', fontsize=20, fontweight='bold',
             color=COLORS['primary'])
    
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    fig.text(0.5, 0.935, f'Generado el {fecha_actual}', 
             ha='center', va='top', fontsize=11, 
             color=COLORS['light_gray'], style='italic')
    
    # ========== MÉTRICAS CLAVE (Parte superior) ==========
    total_facturas = len(df)
    total_importe = df['importe'].sum()
    promedio_factura = df['importe'].mean()
    
    # Tarjetas de métricas
    metricas = [
        ('FACTURAS\nPROCESADAS', total_facturas, '📄'),
        ('IMPORTE\nTOTAL', formatear_moneda(total_importe), '💰'),
        ('PROMEDIO\nPOR FACTURA', formatear_moneda(promedio_factura), '📊'),
    ]
    
    for i, (titulo, valor, icono) in enumerate(metricas):
        ax = fig.add_subplot(gs[0, i])
        ax.axis('off')
        
        # Fondo de la tarjeta con sombra moderna
        rect = mpatches.FancyBboxPatch((0.05, 0.1), 0.9, 0.8,
                                       boxstyle="round,pad=0.08",
                                       facecolor=COLORS['white'],
                                       edgecolor=COLORS['gradient_1'] if i == 0 else 
                                                (COLORS['highlight'] if i == 1 else COLORS['gradient_2']),
                                       linewidth=3)
        ax.add_patch(rect)
        
        # Icono
        ax.text(0.5, 0.75, icono, ha='center', va='center',
                fontsize=30, transform=ax.transAxes)
        
        # Título
        ax.text(0.5, 0.5, titulo, ha='center', va='center',
                fontsize=9, fontweight='bold', color=COLORS['text'],
                transform=ax.transAxes)
        
        # Valor
        valor_texto = str(valor) if isinstance(valor, int) else valor
        fontsize_valor = 16 if len(valor_texto) < 15 else 12
        ax.text(0.5, 0.25, valor_texto, ha='center', va='center',
                fontsize=fontsize_valor, fontweight='bold',
                color=COLORS['primary'], transform=ax.transAxes)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    
    # ========== GRÁFICO DE BARRAS: Top Proveedores ==========
    ax1 = fig.add_subplot(gs[1, :2])
    
    # Agrupar por proveedor
    top_proveedores = df.groupby('proveedor')['importe'].sum().sort_values(ascending=False).head(8)
    
    # Crear gradiente de colores para las barras
    colors_bars = [COLORS['gradient_1'], COLORS['accent'], COLORS['highlight'], 
                   COLORS['warning'], COLORS['gradient_2'], COLORS['success'],
                   COLORS['light_gray'], COLORS['secondary']]
    
    bars = ax1.barh(range(len(top_proveedores)), top_proveedores.values,
                    color=colors_bars[:len(top_proveedores)], 
                    edgecolor=COLORS['white'], linewidth=2, alpha=0.9)
    
    ax1.set_yticks(range(len(top_proveedores)))
    ax1.set_yticklabels(top_proveedores.index, fontsize=9)
    ax1.set_xlabel('Importe Total (COP)', fontweight='bold', color=COLORS['text'])
    ax1.set_title('TOP PROVEEDORES POR IMPORTE', fontsize=13, fontweight='bold',
                  color=COLORS['primary'], pad=15)
    
    # Añadir valores en las barras
    for i, (idx, valor) in enumerate(top_proveedores.items()):
        ax1.text(valor, i, f' {formatear_moneda(valor)}', 
                va='center', ha='left', fontsize=8, fontweight='bold',
                color=COLORS['text'])
    
    ax1.grid(axis='x', alpha=0.3)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # ========== GRÁFICO CIRCULAR: Distribución por Moneda ==========
    ax2 = fig.add_subplot(gs[1, 2])
    
    # Verificar si existe la columna moneda
    if 'moneda' in df.columns:
        monedas_count = df['moneda'].value_counts()
        
        # Colores modernos para el pie chart
        pie_colors = [COLORS['gradient_1'], COLORS['highlight'], COLORS['gradient_2']]
        
        wedges, texts, autotexts = ax2.pie(monedas_count.values, 
                                            labels=monedas_count.index,
                                            autopct='%1.1f%%',
                                            startangle=45,
                                            colors=pie_colors[:len(monedas_count)],
                                            wedgeprops={'edgecolor': COLORS['white'], 
                                                       'linewidth': 3},
                                            explode=[0.05] * len(monedas_count))
        
        for autotext in autotexts:
            autotext.set_color(COLORS['white'])
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        
        for text in texts:
            text.set_fontsize(10)
            text.set_fontweight('bold')
            text.set_color(COLORS['text'])
        
        ax2.set_title('DISTRIBUCIÓN\nPOR MONEDA', fontsize=12, fontweight='bold',
                      color=COLORS['primary'], pad=15)
    else:
        # Si no hay columna moneda, mostrar distribución de cantidad por proveedor
        proveedores_count = df['proveedor'].value_counts().head(5)
        
        pie_colors = [COLORS['gradient_1'], COLORS['accent'], COLORS['highlight'], 
                      COLORS['warning'], COLORS['gradient_2']]
        
        wedges, texts, autotexts = ax2.pie(proveedores_count.values, 
                                            labels=proveedores_count.index,
                                            autopct='%1.0f',
                                            startangle=45,
                                            colors=pie_colors[:len(proveedores_count)],
                                            wedgeprops={'edgecolor': COLORS['white'], 
                                                       'linewidth': 3},
                                            explode=[0.05] * len(proveedores_count))
        
        for autotext in autotexts:
            autotext.set_color(COLORS['white'])
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        
        for text in texts:
            text.set_fontsize(9)
            text.set_fontweight('bold')
            text.set_color(COLORS['text'])
        
        ax2.set_title('TOP 5\nPROVEEDORES', fontsize=12, fontweight='bold',
                      color=COLORS['primary'], pad=15)
    
    # ========== TIMELINE: Evolución temporal ==========
    ax3 = fig.add_subplot(gs[2, :])
    
    # Convertir fecha a datetime si no lo es
    if 'fecha' in df.columns:
        df_temp = df.copy()
        df_temp['fecha'] = pd.to_datetime(df_temp['fecha'], errors='coerce')
        df_temp = df_temp.dropna(subset=['fecha'])
        
        if len(df_temp) > 0:
            # Agrupar por fecha
            timeline = df_temp.groupby(df_temp['fecha'].dt.date)['importe'].sum().sort_index()
            
            ax3.plot(timeline.index, timeline.values, 
                    color=COLORS['gradient_1'], linewidth=3, marker='o',
                    markersize=10, markerfacecolor=COLORS['highlight'],
                    markeredgecolor=COLORS['white'], markeredgewidth=2.5,
                    alpha=0.9, zorder=3)
            
            ax3.fill_between(timeline.index, timeline.values, alpha=0.2,
                            color=COLORS['gradient_1'])
            
            ax3.set_xlabel('Fecha', fontweight='bold', color=COLORS['text'])
            ax3.set_ylabel('Importe Total (COP)', fontweight='bold', color=COLORS['text'])
            ax3.set_title('EVOLUCIÓN DE FACTURAS EN EL TIEMPO', fontsize=13,
                         fontweight='bold', color=COLORS['primary'], pad=15)
            
            # Formatear eje Y
            ax3.yaxis.set_major_formatter(plt.FuncFormatter(
                lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'
            ))
            
            # Rotar etiquetas del eje X
            plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            ax3.grid(True, alpha=0.3)
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
        else:
            ax3.text(0.5, 0.5, 'No hay datos de fecha válidos para mostrar timeline',
                    ha='center', va='center', transform=ax3.transAxes,
                    fontsize=12, color=COLORS['light_gray'], style='italic')
            ax3.axis('off')
    else:
        # Si no hay columna fecha, mostrar distribución de facturas por proveedor
        dist_proveedores = df['proveedor'].value_counts().head(10)
        colors_bars_alt = [COLORS['gradient_1'], COLORS['accent'], COLORS['highlight'], 
                          COLORS['warning'], COLORS['gradient_2'], COLORS['success'],
                          COLORS['accent'], COLORS['gradient_1'], COLORS['highlight'], 
                          COLORS['secondary']]
        ax3.bar(range(len(dist_proveedores)), dist_proveedores.values,
               color=colors_bars_alt[:len(dist_proveedores)], 
               edgecolor=COLORS['white'], linewidth=2, alpha=0.9)
        
        ax3.set_xticks(range(len(dist_proveedores)))
        ax3.set_xticklabels(dist_proveedores.index, rotation=45, ha='right', fontsize=9)
        ax3.set_ylabel('Cantidad de Facturas', fontweight='bold', color=COLORS['text'])
        ax3.set_title('CANTIDAD DE FACTURAS POR PROVEEDOR', fontsize=13,
                     fontweight='bold', color=COLORS['primary'], pad=15)
        ax3.grid(axis='y', alpha=0.3)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
    
    # ========== PIE DE PÁGINA ==========
    fig.text(0.5, 0.02, 
             f'ETL-AI • Análisis de {total_facturas} facturas • Total procesado: {formatear_moneda(total_importe)}',
             ha='center', va='bottom', fontsize=9, color=COLORS['light_gray'],
             style='italic')
    
    # Guardar el reporte
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight', facecolor=COLORS['bg'])
    print(f"✅ Reporte visual guardado en: {ruta_salida}")
    
    return ruta_salida

def generar_reporte_compacto(df, ruta_salida="reporte_compacto.png"):
    """Genera un reporte más compacto para vista rápida"""
    # Validar que el DataFrame no esté vacío
    if df is None or df.empty:
        print("⚠️  No hay datos para generar el reporte compacto")
        return None
    
    # Validar columnas mínimas requeridas
    if 'proveedor' not in df.columns or 'importe' not in df.columns:
        print("⚠️  Faltan columnas requeridas para el reporte compacto")
        return None
    
    configurar_estilo()
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor(COLORS['bg'])
    
    # Título principal
    fig.suptitle('RESUMEN EJECUTIVO DE FACTURAS', 
                 fontsize=16, fontweight='bold', color=COLORS['primary'])
    
    # Gráfico 1: Barras de proveedores con gradiente de colores
    top_5 = df.groupby('proveedor')['importe'].sum().sort_values(ascending=False).head(5)
    colors_gradient = [COLORS['gradient_1'], COLORS['accent'], COLORS['highlight'], 
                      COLORS['warning'], COLORS['gradient_2']]
    axes[0].barh(range(len(top_5)), top_5.values, 
                 color=colors_gradient[:len(top_5)],
                 edgecolor=COLORS['primary'], linewidth=1.2, alpha=0.9)
    axes[0].set_yticks(range(len(top_5)))
    axes[0].set_yticklabels(top_5.index, fontsize=9)
    axes[0].set_title('Top 5 Proveedores', fontweight='bold', color=COLORS['primary'], pad=12)
    axes[0].spines['top'].set_visible(False)
    axes[0].spines['right'].set_visible(False)
    axes[0].spines['left'].set_color(COLORS['light_gray'])
    axes[0].spines['bottom'].set_color(COLORS['light_gray'])
    
    # Gráfico 2: Distribución de monedas o proveedores con colores modernos
    if 'moneda' in df.columns:
        monedas = df['moneda'].value_counts()
        colors_pie = [COLORS['gradient_1'], COLORS['highlight'], COLORS['gradient_2']]
        axes[1].pie(monedas.values, labels=monedas.index, autopct='%1.1f%%',
                   colors=colors_pie[:len(monedas)],
                   wedgeprops={'edgecolor': COLORS['white'], 'linewidth': 3},
                   startangle=45, textprops={'fontsize': 10, 'weight': 'bold'})
        axes[1].set_title('Distribución por Moneda', fontweight='bold', 
                         color=COLORS['primary'], pad=12)
    else:
        # Mostrar distribución por cantidad de proveedores
        prov_count = df['proveedor'].value_counts().head(5)
        colors_pie = [COLORS['gradient_1'], COLORS['accent'], COLORS['highlight'], 
                     COLORS['warning'], COLORS['gradient_2']]
        axes[1].pie(prov_count.values, labels=prov_count.index, autopct='%1.0f',
                   colors=colors_pie[:len(prov_count)],
                   wedgeprops={'edgecolor': COLORS['white'], 'linewidth': 3},
                   startangle=45, textprops={'fontsize': 9, 'weight': 'bold'})
        axes[1].set_title('Top 5 Proveedores', fontweight='bold', 
                         color=COLORS['primary'], pad=12)
    
    # Gráfico 3: Estadísticas clave
    axes[2].axis('off')
    stats_text = f"""
    📊 ESTADÍSTICAS CLAVE
    
    Total Facturas: {len(df)}
    
    Importe Total:
    {formatear_moneda(df['importe'].sum())}
    
    Promedio:
    {formatear_moneda(df['importe'].mean())}
    
    Mediana:
    {formatear_moneda(df['importe'].median())}
    """
    axes[2].text(0.1, 0.5, stats_text, fontsize=11, verticalalignment='center',
                fontfamily='monospace', color=COLORS['text'],
                bbox=dict(boxstyle='round', facecolor=COLORS['white'], 
                         edgecolor=COLORS['accent'], linewidth=2))
    
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight', facecolor=COLORS['bg'])
    print(f"✅ Reporte compacto guardado en: {ruta_salida}")
    
    return ruta_salida
