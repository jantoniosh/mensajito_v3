// mensajito.mx
// Idea Original : Diego Aguirre
// Código: Antonio Salinas

void receive( byte[] data, String ip, int port ) {  // <-- extended handler
  String message = new String( data );
  String[] list = split(message, "#");
  //println(list[0]);
  //println(list[1]);
  char tipo = list[0].charAt(0);
  switch (tipo) {
      case 'n':
        println("nombre");
        nombre = list[1];
	      nombre = nombre.toLowerCase();
        println(nombre);
        break;
      case 'u':
        println("ubicación");
        ubicacion = list[1];
	      ubicacion = ubicacion.toLowerCase();
        println(ubicacion);
        break;
      case 'e':
        println("escuchas");
        escuchas = list[1];
        println(escuchas);
        break;
      case 'p':
        println("parar");
	      boton1.change_label("transmitir");
        trsm = false;
        break;
  }
  println( "receive: \""+message+"\" from "+ip+" on port "+port );
}
