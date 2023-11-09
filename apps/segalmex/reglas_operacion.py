

#####################################################################
########################## Reglas de operación ######################
####################################################################
import dash          
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html



######################################################################
##########################   2019 - Maíz  ############################
######################################################################
ro_2019_maiz = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, align="justify", style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """Todos los productores de maíz poseedores de una superficie de cultivo de hasta 5 (cinco) hectáreas de temporal."""
                                    , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    html.Center(
                                        dmc.Table(
                                        [html.Thead(html.Tr([
                                                    html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                    html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                        html.Tbody([html.Tr([html.Td("5,610"), html.Td("20 Ton")])])],
                                        striped=False,
                                        highlightOnHover=False,
                                        withBorder=True,
                                        horizontalSpacing=4,
                                        withColumnBorders=True,
                                        
                                        style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                    ), 
                                    dmc.Text(
                                        """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo."""
                                    , color='white', align="justify", style={"fontSize": 11, 'padding':'1rem'}),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                    
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    # dmc.List(
                                    #     dmc.ListItem([
                                    #         dmc.Text(
                                    #             """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                    #         , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                    #         html.Br(),
                                    #         # table
                                    #         html.Center(
                                    #             dmc.Table(
                                    #             [html.Thead(html.Tr([
                                    #                         html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                    #                         html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                    #             html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                    #             striped=False,
                                    #             highlightOnHover=False,
                                    #             withBorder=True,
                                    #             horizontalSpacing=4,
                                    #             withColumnBorders=True,
                                                
                                    #             style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                    #         ),          
                                    #     ]),
                                    # ),
                                    html.Br(),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se emiten los Lineamientos de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos a cargo Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2019. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5551718&fecha=01/03/2019#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """Aviso por el que se da a conocer la Modificación al Acuerdo por el que se emiten los Lineamientos de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, disponible en: """
                                            ,html.A("Liga", 
                                                href='https://www.gob.mx/agricultura/documentos/convocatorias-avisos-y-documentos-del-programa-de-precios-de-garantia-a-productos-alimentarios-basicos-2019', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'})

##########################   2019 - Frijol  ####################
ro_2019_frijol = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """Todos los productores poseedores de una superficie de cultivo de hasta 30 hectáreas de temporal o hasta 5 hectáreas de riego. Cuando estas superficies excedan hasta en media hectárea, la misma será redondeada a la superficie de 30 hectáreas de temporal o 5 hectáreas de riego, autorizados para el pago del precio de garantía."""
                                    , color='white', align="justify",  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    html.Center(
                                        dmc.Table(
                                        [html.Thead(html.Tr([
                                                    html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                    html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                        html.Tbody([html.Tr([html.Td("14,500"), html.Td("15 Ton")])])],
                                        striped=False,
                                        highlightOnHover=False,
                                        withBorder=True,
                                        horizontalSpacing=4,
                                        withColumnBorders=True,
                                        
                                        style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                    ), 
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo."""
                                    # , color='white',  style={"fontSize": 11, 'padding':'1rem'}),
                                    # # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                    
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    # dmc.List(
                                    #     dmc.ListItem([
                                    #         dmc.Text(
                                    #             """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                    #         , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                    #         html.Br(),
                                    #         # table
                                    #         html.Center(
                                    #             dmc.Table(
                                    #             [html.Thead(html.Tr([
                                    #                         html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                    #                         html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                    #             html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                    #             striped=False,
                                    #             highlightOnHover=False,
                                    #             withBorder=True,
                                    #             horizontalSpacing=4,
                                    #             withColumnBorders=True,
                                                
                                    #             style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                    #         ),          
                                    #     ]),
                                    # ),
                                    html.Br(),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se emiten los Lineamientos de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos a cargo Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2019. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5551718&fecha=01/03/2019#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """Aviso por el que se da a conocer la Modificación al Acuerdo por el que se emiten los Lineamientos de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, disponible en: """
                                            ,html.A("Liga", 
                                                href='https://www.gob.mx/agricultura/documentos/convocatorias-avisos-y-documentos-del-programa-de-precios-de-garantia-a-productos-alimentarios-basicos-2019', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),                            
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'})

############             2019 - Trigo
ro_2019_trigo = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores de trigo con la limitante del volumen máximo por productor."""
                                    , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    html.Center(
                                        dmc.Table(
                                        [html.Thead(html.Tr([
                                                    html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                    html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                        html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                        striped=False,
                                        highlightOnHover=False,
                                        withBorder=True,
                                        horizontalSpacing=4,
                                        withColumnBorders=True,
                                        
                                        style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                    ), 
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo."""
                                    # , color='white',  style={"fontSize": 11, 'padding':'1rem'}),
                                    # # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),   
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    # dmc.List(
                                    #     dmc.ListItem([
                                    #         dmc.Text(
                                    #             """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                    #         , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                    #         html.Br(),
                                    #         # table
                                    #         html.Center(
                                    #             dmc.Table(
                                    #             [html.Thead(html.Tr([
                                    #                         html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                    #                         html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                    #             html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                    #             striped=False,
                                    #             highlightOnHover=False,
                                    #             withBorder=True,
                                    #             horizontalSpacing=4,
                                    #             withColumnBorders=True,
                                                
                                    #             style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                    #         ),          
                                    #     ]),
                                    # ),
                                    html.Br(),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se emiten los Lineamientos de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos a cargo Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2019. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5551718&fecha=01/03/2019#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """Aviso por el que se da a conocer la Modificación al Acuerdo por el que se emiten los Lineamientos de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, disponible en: """
                                            ,html.A("Liga", 
                                                href='https://www.gob.mx/agricultura/documentos/convocatorias-avisos-y-documentos-del-programa-de-precios-de-garantia-a-productos-alimentarios-basicos-2019', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),                            
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'})


############             2019 - Arroz
ro_2019_arroz = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores de arroz con la limitante del volumen máximo por productor."""
                                    , color='white', align="justify",  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    html.Center(
                                        dmc.Table(
                                        [html.Thead(html.Tr([
                                                    html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                    html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                        html.Tbody([html.Tr([html.Td("6,120"), html.Td("120 Ton")])])],
                                        striped=False,
                                        highlightOnHover=False,
                                        withBorder=True,
                                        horizontalSpacing=4,
                                        withColumnBorders=True,
                                        
                                        style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                    ), 
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo."""
                                    # , color='white',  style={"fontSize": 11, 'padding':'1rem'}),
                                    # # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),   
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    # dmc.List(
                                    #     dmc.ListItem([
                                    #         dmc.Text(
                                    #             """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                    #         , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                    #         html.Br(),
                                    #         # table
                                    #         html.Center(
                                    #             dmc.Table(
                                    #             [html.Thead(html.Tr([
                                    #                         html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                    #                         html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                    #             html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                    #             striped=False,
                                    #             highlightOnHover=False,
                                    #             withBorder=True,
                                    #             horizontalSpacing=4,
                                    #             withColumnBorders=True,
                                                
                                    #             style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                    #         ),          
                                    #     ]),
                                    # ),
                                    html.Br(),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se emiten los Lineamientos de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos a cargo Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2019. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5551718&fecha=01/03/2019#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """Aviso por el que se da a conocer la Modificación al Acuerdo por el que se emiten los Lineamientos de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, disponible en: """
                                            ,html.A("Liga", 
                                                href='https://www.gob.mx/agricultura/documentos/convocatorias-avisos-y-documentos-del-programa-de-precios-de-garantia-a-productos-alimentarios-basicos-2019', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),             
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'})



############             2019 - Leche
ro_2019_leche = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.List([
                                        dmc.ListItem(dmc.Text("Pequeños productores: de 1 a 35 vacas", color='white', style={"fontSize": 18, 'padding':'1rem'})),
                                        dmc.ListItem(dmc.Text("Medianos productos: de 36 a 100 vacas", color='white', style={"fontSize": 18, 'padding':'1rem'})),
                                    ], style={'marginBottom':'1rem'}),
                                     dmc.Text(
                                        """*LICONSA podrá comprar leche fluida a productores que rebasen el límite de vacas antes señalado, en tal caso, lo hará a precio de mercado."""
                                    , color='white', align="justify", style={"fontSize": 12, 'marginBottom':'2rem'}),
                                    # dmc.Text(
                                    #     """La totalidad de los productores de arroz con la limitante del volumen máximo por productor."""
                                    # , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    # html.Br(),
                                    # Tabla
                                    html.Center(
                                        dmc.Table(
                                        [html.Thead(html.Tr([
                                                    html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                    html.Th("Volumen máximo (Ltrs) ", style={'color':'white'}),])),
                                        html.Tbody([html.Tr([html.Td("8.20/Ltr"), html.Td("15 Ltrs/vaca")])])],
                                        striped=False,
                                        highlightOnHover=False,
                                        withBorder=True,
                                        horizontalSpacing=4,
                                        withColumnBorders=True,
                                        
                                        style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                    ), 
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo."""
                                    # , color='white',  style={"fontSize": 11, 'padding':'1rem'}),
                                    # # Pie
                                   
                                    # html.Br(),   
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    # dmc.List(
                                    #     dmc.ListItem([
                                    #         dmc.Text(
                                    #             """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                    #         , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                    #         html.Br(),
                                    #         # table
                                    #         html.Center(
                                    #             dmc.Table(
                                    #             [html.Thead(html.Tr([
                                    #                         html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                    #                         html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                    #             html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                    #             striped=False,
                                    #             highlightOnHover=False,
                                    #             withBorder=True,
                                    #             horizontalSpacing=4,
                                    #             withColumnBorders=True,
                                                
                                    #             style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                    #         ),          
                                    #     ]),
                                    # ),
                                    html.Br(),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se emiten los Lineamientos de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos a cargo Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2019. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5551718&fecha=01/03/2019#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """Aviso por el que se da a conocer la Modificación al Acuerdo por el que se emiten los Lineamientos de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, disponible en: """
                                            ,html.A("Liga", 
                                                href='https://www.gob.mx/agricultura/documentos/convocatorias-avisos-y-documentos-del-programa-de-precios-de-garantia-a-productos-alimentarios-basicos-2019', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),   
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'})
######################################################################
##########################   2020 - Maíz  ############################
######################################################################
ro_2020_maiz = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    # html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Todos los pequeños productores poseedores de una superficie de cultivo de hasta 5 (cinco) hectáreas de temporal. En este límite, las fracciones de hectárea hasta 0.5 se redondearán al número inferior."""
                                            , color='white', align="justify",  style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # Tabla
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,610"), html.Td("20 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                            ), 
                                            dmc.Text(
                                                """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo."""
                                            , color='white', align="justify",  style={"fontSize": 11, 'padding':'1rem'}),
                                            
                                            dmc.Text(
                                                """Maíz comercializado por medianos productores. Los medianos productores de maíz de riego y los de temporal de más de 5 (cinco) hectáreas, que comercialicen su producción, con hasta 50 hectáreas sembradas."""
                                            , color='white', align="justify",  style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # Tabla
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("4,150"), html.Td("600 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                            ), 
                                            dmc.Text(
                                                """Para los medianos productores de maíz de riego y los de temporal de más de cinco hectáreas, que comercialicen su producción, con hasta 50 (cincuenta) hectáreas sembradas, únicamente se pagará la diferencia entre el Precio de Garantía y un Precio de Mercado de Referencia que establecerá SEGALMEX."""
                                            , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}), 
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    
                                    # break
                                    html.Br(),
                                    
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, Sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2020, Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5587270&fecha=24/02/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """PRIMER Acuerdo Modificatorio de las Reglas de Operación del Programa de precios de garantía a productos alimentarios básicos a cargo seguridad alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural (SADER), para el ejercicio fiscal 2020. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5591535&fecha=13/04/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),                                          html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'})

##########################   2020 - Frijol  ####################
ro_2020_frijol = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """Todos los productores poseedores de una superficie de cultivo de hasta 30 (treinta) hectáreas de temporal o 5 (cinco) hectáreas de riego. En estos límites, las fracciones de hectárea hasta 0.5 se redondearán al número inferior."""
                                    , color='white', align="justify",  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    html.Center(
                                        dmc.Table(
                                        [html.Thead(html.Tr([
                                                    html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                    html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                        html.Tbody([html.Tr([html.Td("14,500"), html.Td("15 Ton")])])],
                                        striped=False,
                                        highlightOnHover=False,
                                        withBorder=True,
                                        horizontalSpacing=4,
                                        withColumnBorders=True,
                                        
                                        style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                    ), 
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo."""
                                    # , color='white',  style={"fontSize": 11, 'padding':'1rem'}),
                                    # # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                    
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    # dmc.List(
                                    #     dmc.ListItem([
                                    #         dmc.Text(
                                    #             """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                    #         , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                    #         html.Br(),
                                    #         # table
                                    #         html.Center(
                                    #             dmc.Table(
                                    #             [html.Thead(html.Tr([
                                    #                         html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                    #                         html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                    #             html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                    #             striped=False,
                                    #             highlightOnHover=False,
                                    #             withBorder=True,
                                    #             horizontalSpacing=4,
                                    #             withColumnBorders=True,
                                                
                                    #             style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                    #         ),          
                                    #     ]),
                                    # ),
                                    html.Br(),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, Sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2020, Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5587270&fecha=24/02/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """PRIMER Acuerdo Modificatorio de las Reglas de Operación del Programa de precios de garantía a productos alimentarios básicos a cargo seguridad alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural (SADER), para el ejercicio fiscal 2020. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5591535&fecha=13/04/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),                              
                            
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'})

############             2020 - Trigo
ro_2020_trigo = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                   html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, Sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2020, Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5587270&fecha=24/02/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """PRIMER Acuerdo Modificatorio de las Reglas de Operación del Programa de precios de garantía a productos alimentarios básicos a cargo seguridad alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural (SADER), para el ejercicio fiscal 2020. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5591535&fecha=13/04/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),                             
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),  
                #], className="col-12"),

############             2020 - Arroz
ro_2020_arroz = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el arroz. En arroz palay destinado a la industria molinera nacional y para semilla, el apoyo para alcanzar el precio de garantía y otros estímulos adicionales, se aplicarán como sigue:"""
                                            , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 120 toneladas por productor elegible, recibirán el incentivo completo, equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 180 toneladas adicionales a las primeras 120 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido en dos categorías (para arroz grueso y para el largo), y para las diferentes regiones productoras. Su cálculo se determinará considerando los precios del arroz en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT), el promedio del tipo de cambio, y los precios sugeridos por la industria molinera y los productores, en el seno del Consejo Mexicano del Arroz y del Sistema Producto Arroz.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            # dmc.Text(
                                            #     """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            # , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("6,120"), html.Td("120 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, Sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2020, Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5587270&fecha=24/02/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """PRIMER Acuerdo Modificatorio de las Reglas de Operación del Programa de precios de garantía a productos alimentarios básicos a cargo seguridad alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural (SADER), para el ejercicio fiscal 2020. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5591535&fecha=13/04/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),                              
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),

############             2020 - Leche
ro_2020_leche = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.List([
                                        dmc.ListItem(dmc.Text("Pequeños productores: de 1 a 35 vacas", color='white', style={"fontSize": 18, 'padding':'1rem'})),
                                        dmc.ListItem(dmc.Text("Medianos productos: de 36 a 100 vacas", color='white', style={"fontSize": 18, 'padding':'1rem'})),
                                    ], style={'marginBottom':'1rem'}),
                                     dmc.Text(
                                        """*LICONSA podrá comprar leche fluida a productores que rebasen el límite de vacas antes señalado, en tal caso, lo hará a precio de mercado."""
                                    , color='white', align="justify", style={"fontSize": 12, 'marginBottom':'2rem'}),
                                    # dmc.Text(
                                    #     """La totalidad de los productores de arroz con la limitante del volumen máximo por productor."""
                                    # , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    # html.Br(),
                                    # Tabla
                                    html.Center(
                                        dmc.Table(
                                        [html.Thead(html.Tr([
                                                    html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                    html.Th("Volumen máximo (Ltrs) ", style={'color':'white'}),])),
                                        html.Tbody([html.Tr([html.Td("8.20/Ltr"), html.Td("25 Ltrs/vaca")])])],
                                        striped=False,
                                        highlightOnHover=False,
                                        withBorder=True,
                                        horizontalSpacing=4,
                                        withColumnBorders=True,
                                        
                                        style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                    ), 
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo."""
                                    # , color='white',  style={"fontSize": 11, 'padding':'1rem'}),
                                    # # Pie
                                   
                                    # html.Br(),   
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    # dmc.List(
                                    #     dmc.ListItem([
                                    #         dmc.Text(
                                    #             """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                    #         , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                    #         html.Br(),
                                    #         # table
                                    #         html.Center(
                                    #             dmc.Table(
                                    #             [html.Thead(html.Tr([
                                    #                         html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                    #                         html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                    #             html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                    #             striped=False,
                                    #             highlightOnHover=False,
                                    #             withBorder=True,
                                    #             horizontalSpacing=4,
                                    #             withColumnBorders=True,
                                                
                                    #             style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                    #         ),          
                                    #     ]),
                                    # ),
                                    html.Br(),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, Sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2020, Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5587270&fecha=24/02/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """PRIMER Acuerdo Modificatorio de las Reglas de Operación del Programa de precios de garantía a productos alimentarios básicos a cargo seguridad alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural (SADER), para el ejercicio fiscal 2020. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5591535&fecha=13/04/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),                             
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'})
######################################################################
##########################   2021 - Maíz  ############################
######################################################################
ro_2021_maiz = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    # html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Maíz de pequeños productores: todos los productores poseedores de una superficie de cultivo de hasta 5 (cinco) hectáreas de temporal. En este límite, las fracciones de hectárea hasta 0.5 se redondeará al número inferior."""
                                            , color='white', align="justify",  style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # Tabla
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("6,060"), html.Td("20 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                            ), 
                                            dmc.Text(
                                                """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo."""
                                            , color='white', align="justify",  style={"fontSize": 11, 'padding':'1rem'}),
                                            
                                            dmc.Text(
                                                """Maíz de medianos productores: todos los productores de maíz con tierras de temporal y/o de riego con hasta 50 (cincuenta) hectáreas en propiedad y/o usufructo que comercialicen formalmente. En este límite, las fracciones de hectárea hasta 0.5 se redondeará al número inferior."""
                                            , color='white', align="justify",  style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # Tabla
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("Solo incentivo"), html.Td("600 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                            ),
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # break
                                    html.Br(),
                                    
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2021. Disponible: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """PRIMER Acuerdo Modificatorio al similar por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2021, publicado el 28 de diciembre de 2020. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://www.dof.gob.mx/nota_detalle.php?codigo=5633514&fecha=22/10/2021#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),   
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'})


##########################   2020 - Frijol  ####################
ro_2021_frijol = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """Todos los productores poseedores de una superficie de cultivo de hasta 30 (treinta) hectáreas de temporal o (cinco) 5 hectáreas de riego. En estos límites, las fracciones de hectárea hasta 0.5 se redondeará al número inferior."""
                                    , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    html.Center(
                                        dmc.Table(
                                        [html.Thead(html.Tr([
                                                    html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                    html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                        html.Tbody([html.Tr([html.Td("16,000"), html.Td("15 Ton")])])],
                                        striped=False,
                                        highlightOnHover=False,
                                        withBorder=True,
                                        horizontalSpacing=4,
                                        withColumnBorders=True,
                                        
                                        style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                    ), 
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo."""
                                    # , color='white',  style={"fontSize": 11, 'padding':'1rem'}),
                                    # # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                    
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    # dmc.List(
                                    #     dmc.ListItem([
                                    #         dmc.Text(
                                    #             """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                    #         , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                    #         html.Br(),
                                    #         # table
                                    #         html.Center(
                                    #             dmc.Table(
                                    #             [html.Thead(html.Tr([
                                    #                         html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                    #                         html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                    #             html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                    #             striped=False,
                                    #             highlightOnHover=False,
                                    #             withBorder=True,
                                    #             horizontalSpacing=4,
                                    #             withColumnBorders=True,
                                                
                                    #             style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                    #         ),          
                                    #     ]),
                                    # ),
                                    html.Br(),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2021. Disponible: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """PRIMER Acuerdo Modificatorio al similar por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2021, publicado el 28 de diciembre de 2020. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://www.dof.gob.mx/nota_detalle.php?codigo=5633514&fecha=22/10/2021#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),   
                            
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'})


############             2020 - Trigo
ro_2021_trigo = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white', align="justify",  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                            , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                            dmc.Text(
                                                """Modalidad 1. Si el precio de referencia es mayor o igual al precio de garantía el productor sólo será elegible para el apoyo que se determine para la adquisición del Instrumento de Administración de Riesgos."""
                                            , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                            dmc.Text(
                                                """Modalidad 2. Si el precio de referencia, que establecerá SEGALMEX, es menor al precio de garantía el productor adicionalmente será elegible para un complemento basado en la diferencia entre dichos precios)."""
                                            , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                            dmc.Text(
                                                """Apoyo básico: Hasta 100 toneladas por productor elegible recibirán el apoyo que se determine para la adquisición del Instrumento de Administración de Riesgos (Modalidad 1), o este apoyo y el complemento, basado en la diferencia entre el precio de garantía y el precio de referencia que establecerá SEGALMEX (Modalidad 2)."""
                                            , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                            dmc.Text(
                                                """Apoyo por productividad: Hasta 200 toneladas adicionales a las primeras 100 por productor recibirán, quienes se encuentren en la Modalidad 1, el apoyo que SEGALMEX determine para la adquisición del Instrumento de Administración de Riesgos. Quienes se encuentren en la Modalidad 2 recibirán el apoyo que SEGALMEX determine para la adquisición del IAR y además el 50% del apoyo básico, establecido por la diferencia entre el precio de garantía y el precio de referencia que establecerá SEGALMEX."""
                                            , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                            dmc.Text(
                                                """Precio de referencia: El precio de referencia será definido cuando SEGALMEX declare, mediante un comunicado, la finalización del periodo de comercialización para cada región o entidad y su cálculo se efectuará considerando los posibles valores de los Instrumento de Administración de Riesgos, referenciados a los precios de futuro de la Bolsa de Chicago (CBOT), las bases de comercialización y las condiciones de mercado prevalecientes en el periodo de la cosecha en cada región. Los medios de publicación serán: la página oficial de SEGALMEX y correos electrónicos a los involucrados."""
                                            , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ",  style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton)",  style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white'}),
                                            ),
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se beneficiarán hasta 150 toneladas por productor únicamente con el apoyo que se determine para la adquisición del Instrumento de Administración de Riesgos. Este apoyo sólo se aplicará en Baja California, Sonora y el Bajío."""
                                            , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ",  style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton)",  style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("Solo incentivo"), html.Td("150 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white'}),
                                            ), 
                                            dmc.Text(
                                                """*Un mismo productor puede recibir al mismo tiempo los apoyos descritos Precio de Garantía para el trigo panificable y el incentivo para el trigo cristalino."""
                                            , color='white', align="justify", style={"fontSize": 11, 'padding':'1rem'}),
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2021. Disponible: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """PRIMER Acuerdo Modificatorio al similar por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2021, publicado el 28 de diciembre de 2020. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://www.dof.gob.mx/nota_detalle.php?codigo=5633514&fecha=22/10/2021#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),   
                                    
                                    html.Br(),
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),   
                #], className="col-12"),

############             2020 - Arroz
ro_2021_arroz = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el arroz. En arroz palay destinado a la industria molinera nacional y para semilla, el apoyo para alcanzar el precio de garantía y otros estímulos adicionales, se aplicarán como sigue:"""
                                            , color='white', align="justify", style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [#html.Thead(html.Tr([html.Th(""),
                                                 #           html.Th("", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Tipo de apoyo"), html.Td("Toneladas"), html.Td("Incentivo que recibe el productor")]),
                                                            html.Tr([html.Td("Básico"), html.Td("Hasta 120"), html.Td("100%")]),
                                                            html.Tr([html.Td("A La Productividad"), html.Td("120.1 A 300"), html.Td("50%")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white', 'marginBottom':'1rem'}),
                                                
                                                ),
                                            html.Center(
                                                dmc.Table(
                                                    [html.Tbody([html.Tr([html.Td("Precio de referencia"), html.Td("El precio de referencia será definido en dos categorías (para arroz grueso y para el largo), por ciclo agrícola (O.I. / P.V.) y para las diferentes regiones productoras. Su cálculo se determinará considerando los precios del arroz en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT), el promedio del tipo de cambio, los precios prevalecientes en el mercado nacional y los precios sugeridos y concertados entre la industria arrocera y los productores.")])])],
                                                    highlightOnHover=False,
                                                    withBorder=True,
                                                    horizontalSpacing=4,
                                                    withColumnBorders=True, 
                                                    style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            # dmc.Text(
                                            #     """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            # , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("6,120"), html.Td("120 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2021. Disponible: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """PRIMER Acuerdo Modificatorio al similar por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2021, publicado el 28 de diciembre de 2020. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://www.dof.gob.mx/nota_detalle.php?codigo=5633514&fecha=22/10/2021#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),   
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),

############             2019 - Leche
ro_2021_leche = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.List([
                                        dmc.ListItem(dmc.Text("Pequeños productores: de 1 a 35 vacas", color='white', style={"fontSize": 18, 'padding':'1rem'})),
                                        dmc.ListItem(dmc.Text("Medianos productos: de 36 a 100 vacas", color='white', style={"fontSize": 18, 'padding':'1rem'})),
                                    ], style={'marginBottom':'1rem'}),
                                    #  dmc.Text(
                                    #     """*LICONSA podrá comprar leche fluida a productores que rebasen el límite de vacas antes señalado, en tal caso, lo hará a precio de mercado."""
                                    # , color='white', style={"fontSize": 12, 'marginBottom':'2rem'}),
                                    # # dmc.Text(
                                    #     """La totalidad de los productores de arroz con la limitante del volumen máximo por productor."""
                                    # , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    # html.Br(),
                                    # Tabla
                                    html.Center(
                                        dmc.Table(
                                        [html.Thead(html.Tr([
                                                    html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                    html.Th("Volumen máximo (Ltrs) ", style={'color':'white'}),])),
                                        html.Tbody([html.Tr([html.Td("8.20/Ltr"), html.Td("25 Ltrs/vaca")])])],
                                        striped=False,
                                        highlightOnHover=False,
                                        withBorder=True,
                                        horizontalSpacing=4,
                                        withColumnBorders=True,
                                        
                                        style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                    ), 
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo."""
                                    # , color='white',  style={"fontSize": 11, 'padding':'1rem'}),
                                    # # Pie
                                   
                                    # html.Br(),   
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    # dmc.List(
                                    #     dmc.ListItem([
                                    #         dmc.Text(
                                    #             """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                    #         , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                    #         html.Br(),
                                    #         # table
                                    #         html.Center(
                                    #             dmc.Table(
                                    #             [html.Thead(html.Tr([
                                    #                         html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                    #                         html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                    #             html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                    #             striped=False,
                                    #             highlightOnHover=False,
                                    #             withBorder=True,
                                    #             horizontalSpacing=4,
                                    #             withColumnBorders=True,
                                                
                                    #             style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                    #         ),          
                                    #     ]),
                                    # ),
                                    html.Br(),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        dmc.Text([
                                                """ACUERDO por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2021. Disponible: """
                                            ,html.A("Liga", 
                                                href='https://dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),
                                        
                                        dmc.Text([
                                                """PRIMER Acuerdo Modificatorio al similar por el que se dan a conocer las Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos, a cargo de Seguridad Alimentaria Mexicana, SEGALMEX, sectorizada en la Secretaría de Agricultura y Desarrollo Rural, para el ejercicio fiscal 2021, publicado el 28 de diciembre de 2020. Disponible en: """
                                            ,html.A("Liga", 
                                                href='https://www.dof.gob.mx/nota_detalle.php?codigo=5633514&fecha=22/10/2021#gsc.tab=0', 
                                                target="_blank", 
                                                style={'color':'#07B8F1'}),
                                            ], color='white', align="justify", style={"fontSize": 12, 'padding':'1rem'}),           
                                    ], style={'paddingLeft':'1rem'}),   
                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'})
#####################################################################

def resumen_reglas_operacion(Anio, Producto):
    '''
    Función para retornar el resumen de las reglas de operación
        dados el año y el tipo de producto
        
    Input : 
        Anio     : (int) Año correspondiente a las reglas de operación
                   2019, 2020, 2021
        Producto : (str) Producto considerado; Maíz, Frijol, Trigo,
                   Arroz, y leche.
    Outputs:
        Div : Texto html con el resumen de las reglas de operación  
    '''
    
    #############         Año 2019          ###################
    if Anio == '2019' and Producto == 'Maíz':
        result = ro_2019_maiz
    elif Anio == '2019' and Producto == 'Frijol':
        result = ro_2019_frijol
    elif Anio == '2019' and Producto == 'Trigo':
        result = ro_2019_trigo
    elif Anio == '2019' and Producto == 'Arroz':
        result = ro_2019_arroz
    elif Anio == '2019' and Producto == 'Leche':
        result = ro_2019_leche
    #############         Año 2020          ###################
    elif Anio == '2020' and Producto == 'Maíz':
        result = ro_2020_maiz
    elif Anio == '2020' and Producto == 'Frijol':
        result = ro_2020_frijol
    elif Anio == '2020' and Producto == 'Trigo':
        result = ro_2020_trigo
    elif Anio == '2020' and Producto == 'Arroz':
        result = ro_2020_arroz
    elif Anio == '2020' and Producto == 'Leche':
        result = ro_2020_leche
    #############         Año 2020          ###################
    elif Anio == '2021' and Producto == 'Maíz':
        result = ro_2021_maiz
    elif Anio == '2021' and Producto == 'Frijol':
        result = ro_2021_frijol
    elif Anio == '2021' and Producto == 'Trigo':
        result = ro_2021_trigo
    elif Anio == '2021' and Producto == 'Arroz':
        result = ro_2021_arroz
    elif Anio == '2021' and Producto == 'Leche':
        result = ro_2021_leche
    else:
        result = "No information"
    
    return result





