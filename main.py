from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.lang import Builder
import datetime
from urllib.parse import quote
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.slider import Slider
from kivy.animation import Animation
#SLIDER parq crear boton slider
#**PARA LA INTERFAZ FOMFO VERDE PAATEL EL BOTON CIRCULAR CON SOMBRA, LETRAS BLANCAS BUSCAR FUENTE ATRACTIVA Y FORMAL


#PROXIMO PASO CREAR FUNCION PARA CONSULTAR REGISTRO, Y BLOQUEAR ORIENTQCION

#DropDown (DropDown):Se usa para crear menús desplegables donde se selecciona un ítem de una lista. La lista de ítems se muestra debajo de un widget principal, que suele ser un botón. (proximo item q agregar para swoeccionar dia de reunion)

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

        Switch:
            id: switch_tema
            active: False
            on_active: root.activar_tema_claro(self.active)
            
            
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
           
    def activar_tema_claro(self, estado):
        if estado:
            self.tema_claro()
            
        else:
            self.tema_oscuro()
             
        
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
