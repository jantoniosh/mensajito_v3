// mensajito.mx
// Idea Original : Diego Aguirre
// Código: Antonio Salinas

void mousePressed()
{
  String ip       = "localhost";
  int port        = 6100; 
  
  if (boton1.MouseIsOver()) {
    // print some text to the console pane if the button is clicked
    trsm = !trsm;
    udp.send(str(trsm), ip, port);
    if(trsm) {
      boton1.change_label("parar");
    }
    else {
      boton1.change_label("transmitir");
    }
  }
}
