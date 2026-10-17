from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.lang import Builder
#from kivymd.app import MDApp
import datetime
from urllib.parse import quote
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Ellipse, Line, Mesh, RoundedRectangle
from kivy.uix.slider import Slider
from kivy.animation import Animation
import math
from kivy.metrics import dp
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
#SLIDER parq crear boton slider
#**PARA LA INTERFAZ FOMFO VERDE PAATEL EL BOTON CIRCULAR CON SOMBRA, LETRAS BLANCAS BUSCAR FUENTE ATRACTIVA Y FORMAL


#PROXIMO PASO CREAR FUNCION PARA CONSULTAR REGISTRO, Y BLOQUEAR ORIENTQCION

#DropDown (DropDown):Se usa para crear menús desplegables donde se selecciona un ítem de una lista. La lista de ítems se muestra debajo de un widget principal, que suele ser un botón. (proximo item q agregar para swoeccionar dia de reunion)

# ---------------------------------------------------------------------------
# SWITCH CON ICONOS: luna = ON (tema oscuro), sol = OFF (tema claro)
# Se dibuja con el canvas, sin imagenes, asi que no suma peso al APK.
# ---------------------------------------------------------------------------
def _mezclar(a, b, t):
    # Mezcla dos colores RGBA (t=0 -> a, t=1 -> b)
    return [x + (y - x) * t for x, y in zip(a, b)]


def _luna(cx, cy, r, angulo=40):
    # Vertices (x, y, u, v) de una luna creciente para Mesh 'triangle_strip'
    d = r * 0.62
    r1 = r * 0.82
    x = (d * d + r * r - r1 * r1) / (2 * d)
    y = math.sqrt(max(r * r - x * x, 0))
    a0 = math.atan2(y, x)
    b0 = math.atan2(y, x - d)
    rot = math.radians(angulo)
    cr, sr = math.cos(rot), math.sin(rot)
    pts = []
    for i in range(25):
        t = i / 24
        ao = a0 + t * (2 * math.pi - 2 * a0)
        ai = b0 + t * (2 * math.pi - 2 * b0)
        for px, py in ((r * math.cos(ao), r * math.sin(ao)),
                       (d + r1 * math.cos(ai), r1 * math.sin(ai))):
            pts.append((px * cr - py * sr, px * sr + py * cr))
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ox = cx - (min(xs) + max(xs)) / 2
    oy = cy - (min(ys) + max(ys)) / 2
    verts = []
    for px, py in pts:
        verts += [px + ox, py + oy, 0, 0]
    return verts


class IconSwitch(ButtonBehavior, Widget):
    active = BooleanProperty(True)    # True = luna (oscuro), False = sol (claro)
    pos_norm = NumericProperty(1)     # 0 = sol, 1 = luna (posicion animada)

    ANCHO = dp(84)
    ALTO = dp(40)
    FONDO_CLARO = (0.91, 0.92, 0.94, 1)
    FONDO_OSCURO = (0.12, 0.13, 0.17, 1)
    BOTON_CLARO = (1, 1, 1, 1)
    BOTON_OSCURO = (0.27, 0.29, 0.36, 1)
    INACTIVO_CLARO = (0.62, 0.64, 0.69, 1)
    INACTIVO_OSCURO = (0.45, 0.47, 0.54, 1)
    SOL = (0.96, 0.66, 0.08, 1)
    LUNA = (0.86, 0.89, 1, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_norm = 1.0 if self.active else 0.0
        self.bind(pos=self._dibujar, size=self._dibujar,
                  pos_norm=self._dibujar)
        self.bind(active=self._animar)
        self._dibujar()

    def collide_point(self, x, y):
        # Solo responde al toque sobre el switch, no sobre toda la fila
        m = dp(8)
        return (abs(x - self.center_x) <= self.ANCHO / 2 + m and
                abs(y - self.center_y) <= self.ALTO / 2 + m)

    def on_release(self):
        self.active = not self.active

    def _animar(self, *_):
        Animation.cancel_all(self, 'pos_norm')
        Animation(pos_norm=1.0 if self.active else 0.0,
                  d=0.22, t='out_quad').start(self)

    def _dibujar(self, *_):
        t = self.pos_norm
        w, h = self.ANCHO, self.ALTO
        x0 = self.center_x - w / 2
        y0 = self.center_y - h / 2
        cy = self.center_y
        izq = x0 + h / 2           # centro del icono del sol
        der = x0 + w - h / 2       # centro del icono de la luna
        pad = h * 0.09
        d_boton = h - 2 * pad
        r = h * 0.22               # mismo radio para los dos iconos

        fondo = _mezclar(self.FONDO_CLARO, self.FONDO_OSCURO, t)
        boton = _mezclar(self.BOTON_CLARO, self.BOTON_OSCURO, t)
        apagado = _mezclar(self.INACTIVO_CLARO, self.INACTIVO_OSCURO, t)
        c_sol = _mezclar(self.SOL, apagado, t)
        c_luna = _mezclar(apagado, self.LUNA, t)

        self.canvas.clear()
        with self.canvas:
            Color(*fondo)
            RoundedRectangle(pos=(x0, y0), size=(w, h), radius=[h / 2])
            Color(*boton)
            Ellipse(pos=(izq - d_boton / 2 + t * (der - izq), cy - d_boton / 2),
                    size=(d_boton, d_boton))
            # sol: circulo + 8 rayos
            Color(*c_sol)
            nucleo = r * 0.8
            Ellipse(pos=(izq - nucleo / 2, cy - nucleo / 2),
                    size=(nucleo, nucleo))
            for k in range(8):
                a = k * math.pi / 4
                Line(points=[izq + math.cos(a) * r * 0.68,
                             cy + math.sin(a) * r * 0.68,
                             izq + math.cos(a) * r,
                             cy + math.sin(a) * r],
                     width=dp(1.3), cap='round')
            # luna creciente
            Color(*c_luna)
            v = _luna(der, cy, r)
            Mesh(vertices=v, indices=list(range(len(v) // 4)),
                 mode='triangle_strip')


# Establecer el tamaño de la ventana
# medida anterior era 1080, 720 1440
#Window.size = (720, 1440)
Window.fullscrean = 'auto'
#Window_color = (1, 2, 0, 1)  
#color_clear = (1, 0, 0, 1)
# Cargar el código kv
Builder.load_string('''
<ContadorApp>:
    orientation: 'vertical' 
    padding: 20
    spacing: 10
    color: (1, 1, 0, 0)
    #CODIGO NUEVO 
    #canvas.before:
   #     Rectangle:           
           # source: 'jj.png'
 #           source: 'fondc.png'
           # size: self.size
    #        size: (720, 1440)
 #           pos: self.pos
           
    #CODIGO NUEVO corregir tamaño de imagen de fondo, la siguiente linea es un swich
   
 
    BoxLayout: #AQUI EMPIEZA EL SWICH
        orientation: 'horizontal'
        size_hint: (1, 0.1)
        spacing: 30

        #Label:
     #       text: 'Tema claro:'
   #         font_size: 22
 #           color: (0, 0, 0, 1)

        IconSwitch:
            id: switch_tema
            on_active: root.activar_tema_oscuro(self.active)
            
            
#    Button:    #tema  claro
#        text: 'tema claro'
#        size_hint : (0.3, 0.3)
#        on_press: root.tema_claro()       
         
    Label:
        id: contador_label
        text: 'PREPARADO PARA CONTAR'
        font_size: 52
     #   color: (0,  0, 0, 1)
        
    Button:
        id: toque_cont
        text: 'Toque para contar' 
        background_normal: 'botonb2.png'
        background_down: 'botondownb.png'  
        #cambiar imafen down
        size_hint: (1, 1.55)   
     #   background_color: (0, 0.02, 1.3, 0.35)
        # 1, 1, 2, 0.4
      #  color: (0, 0, 0, 1)                
        on_press: root.incrementar_contador()
        font_size: 56
                         
     
    Button:
        id: guardar_datos
        #text: 'GUARDAR DATOS'
      #  pos_hint: ({'center_x': 0.5, 'center_y': 0.5}) 
        pos_hint: ({'right':1, 'top':2})
        background_color: (1, 1, 1, 0.8)
#back color pqra transparencia -1
# (1, 1, 1, 08) color anterior 
        size_hint : (0.3, 0.3)       
        background_normal: 'g1w.png'
        background_down: 'g2w.png'       
        size_hint: (0.3, 0.4)
      #  style: 'filled'
        on_press: root.guardar_datos()
        font_size: 16
        color: (0, 0, 0, 1)
        
    Button:     
        id: limpiar_r
        pos_hint: ({'center_x': 0.2, 'center_y': 0.5})    
     #   background_color: (1, 2, 1, 0.5)
        background_normal: 'b1w.png'
        background_down: 'b2w.png'       
        size_hint: (0.3, 0.3)
       # size_hint : (0.5, 0.2)      
        on_press: root.borrar_datos()
        font_size: 22
        color: (0, 0, 0, 1)      

    Button:
        id: enviar_wa
        pos_hint: ({'right':1, 'top':2})
        #text: 'ENVIAR POR WHATSAPP'
        size_hint: (0.3, 0.4)
        background_normal: 'wht.png'
        background_color: (1, 1, 1, 0.5)
        color: (1, 1, 1, 1)
        font_size: 22
        on_press: root.enviar_whatsapp()
          
                
              
        
''')

#DAR FORMATO EN ESPAÑOL A FECHA
#PUDE SER CON UNA FUNCION (INVESTIGAR); puede crear variable que cambie dias a español
now = datetime.datetime.now()
fecha = now.strftime("%a-%d-%m-%y ")


class ContadorApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contador = 0
        
        with self.canvas.before:
            color: (1, 1, 1, 1)
            self.fondo_rect = Rectangle (source= 'fondc.png', size= Window.size, pos=self.pos)
            
       # self.bind (size=self.actualizar_fondo, pos=self.actualizar_fondo)  
 #   def _actualizar_fondo(self, *args):
      #  self.fondo_rect.size = self.size
   #     self.fondo_rect.pos = self.pos        
        
    def incrementar_contador(self):
        self.contador += 1
        self.ids.contador_label.text = f'ASISTENTES: {self.contador}'
        self.ids.contador_label.font_size: 88
         
#self.id... conecta con el label y modifica su text mediante la funcion incrememtar
                  
       # if  self.contador > 0 :
     #       with open ('datos2.txt', 'w' )  as f:
  #              f.write (str (self.contador) + " " "personas" + " " + fecha  )
          
    def enviar_whatsapp(self):
        # Abre WhatsApp con el mensaje listo y la lista de contactos/chats
        # para que el usuario elija el destinatario
        hoy = datetime.datetime.now().strftime("%d-%m-%y")
        mensaje = f"Asistentes: {self.contador} - {hoy}"
        try:
            from jnius import autoclass, cast
            Intent = autoclass('android.content.Intent')
            String = autoclass('java.lang.String')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            texto = cast('java.lang.CharSequence', String(mensaje))

            # WhatsApp normal y WhatsApp Business
            for paquete in ('com.whatsapp', 'com.whatsapp.w4b'):
                try:
                    intent = Intent(Intent.ACTION_SEND)
                    intent.setType('text/plain')
                    intent.putExtra(Intent.EXTRA_TEXT, texto)
                    intent.setPackage(paquete)
                    activity.startActivity(intent)
                    return
                except Exception:
                    continue

            # Si no hay WhatsApp instalado, muestra el selector de Android
            intent = Intent(Intent.ACTION_SEND)
            intent.setType('text/plain')
            intent.putExtra(Intent.EXTRA_TEXT, texto)
            activity.startActivity(Intent.createChooser(intent, 'Enviar con'))
        except ImportError:
            # En PC (pruebas) abre WhatsApp Web / selector de chat en el navegador
            import webbrowser
            webbrowser.open(f"https://wa.me/?text={quote(mensaje)}")

    def guardar_datos(self):
        if  self.contador > 0 :
            with open ('datos2.txt', 'a' )  as f:
                f.write ("\n" + (str (self.contador) + " " "personas" + " " + fecha  ) + "\n" )
                self.ids.contador_label.text = f'Asistentes: {0}'
                self.contador = 0
  
    def borrar_datos(self):
       if self.contador == self.contador:
        with open ('datos2.txt', 'w' )  as f:
           f.write ( "ESTE REGISTRO FUE BORRADO EL DIA" + " " + fecha)
           self.ids.contador_label.text = f'Asistentes: {0}'
           self.contador = 0
           
    def activar_tema_oscuro(self, estado):
        # estado True = luna (oscuro), False = sol (claro)
        if estado:
            self.tema_oscuro()
            
        else:
            self.tema_claro()
             
        
    def tema_claro (self):
            self.ids.toque_cont.background_normal= 'btb.png'
            self.ids.toque_cont.background_normal.size_hint: (1, 1)
            self.ids.toque_cont.background_down= 'btb2.png'
            size_hint: (4, 4)
            self.ids.guardar_datos.background_normal= 'g1b.png'
            self.ids.guardar_datos.background_down= 'g2b.png' #de aqui
            self.ids.limpiar_r.background_normal= 'b1b.png'
            self.ids.limpiar_r.background_down= 'b2b.png'
            self.fondo_rect.source = 'fondb.png'
         #   self.ids.Contado_App.Rectangle.source= 'fondo.png' #(CREAR FUNCUON PARA CQMBIAR IMAGEN DE FONDO)

    def tema_oscuro (self):
            self.ids.toque_cont.background_normal= 'botonb2.png'
            self.ids.toque_cont.background_down= 'botondownb.png'
            self.ids.guardar_datos.background_normal= 'g1w.png'
            self.ids.guardar_datos.background_down= 'g2w.png' #de aqui
            self.ids.limpiar_r.background_normal= 'b1w.png'
            self.ids.limpiar_r.background_down= 'b2w.png'
            self.fondo_rect.source = 'fondc.png'                                      
                    
                          
                 
 
        
        
        
        

class MainApp(App):
    def build(self):
        return ContadorApp()
        
        


if __name__ == '__main__':
    MainApp().run()
