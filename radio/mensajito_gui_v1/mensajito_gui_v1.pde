// mensajito.mx
// Idea Original : Diego Aguirre
// Código: Antonio Salinas

import hypermedia.net.*;

Button boton1; 
int clk = 1;
UDP udp;
boolean trsm;
PFont main_font;
String nombre, ubicacion, escuchas;
PImage estacion, logo, fondo;

void setup() {
  nombre = "";
  ubicacion = "";
  escuchas = "";
  fullScreen();
  //size(480,320);
  main_font = createFont("CircularStd-Medium.otf", 28);
  noCursor();
  textFont(main_font);
  smooth();
  udp = new UDP(this, 6000);
  udp.listen(true);
  textSize(18);
  boton1 = new Button("transmitir", 10, 220, 140, 60);
  trsm = false;
  logo = loadImage("logo.jpg");
  fondo = loadImage("/home/pi/grafica/fondo.jpg");
}

void draw() {
  if (trsm) {
    background(175);
    fill(0);
    textSize(28);
    textAlign(LEFT);
    text(nombre, 10, 60);
    text("transmitiendo desde", 10, 100);
    text(ubicacion, 10, 140);
    text("escuchas: " + escuchas, 10, 180);
    textSize(28);
    boton1.Draw();
    fill(255, 0, 0);
    noStroke();
    ellipse(260, 253, 20, 20);
    text("en vivo", 200, 250);
    image(logo, 300, 120, 170, 170);
  }
  else {
    background(fondo);
    textSize(28);
    boton1.Draw();
  }
}
