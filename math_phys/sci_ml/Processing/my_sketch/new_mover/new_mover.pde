float interval = 1/32f;
float ratio = 200;
double G = 6.67e-11;
int center_px;
int center_py;
ArrayList<Mover> movers = new ArrayList();

class Vector{
  double x = 0;
  double y = 0;
  
  Vector(){}
  
  Vector(double X, double Y){
    x = X;
    y = Y;
  }
  
  Vector(Vector v1, Vector v2){
    x = v2.x - v1.x;
    y = v2.y - v1.y;
  }
  
  boolean equals(Vector v){
      return x == v.x && y == v.y;
  }
  
  Vector reserve(){
    x = -x;
    y = -y;
    return this;
  }
  
  Vector reflect(Vector normalLinePointA, Vector normalLinePointB){
    Vector mp = mirrorPoint(x, y, normalLinePointA.x, normalLinePointA.y, normalLinePointB.x, normalLinePointB.y);
    x = mp.x;
    y = mp.y;
    return this;
  }
  
  void add(Vector v){
    x += v.x;
    y += v.y;
  }
  
  void sub(Vector v){
    x -= v.x;
    y -= v.y;
  }
  
  Vector mult(double a){
    x *= a;
    y *= a;
    return this;
  }
  
  void div(double a){
    x /= a;
    y /= a;
  }
  
  double mag(){
    return Math.sqrt(x*x + y*y);
  }
  
  Vector normalize(){
    div(mag());
    return this;
  }
  
  void zero(){
    x = 0;
    y = 0;
  }
  
  String toString(){
    return "( " + x + " , " + y + " )";
  }
}

Vector mirrorPoint(double j, double k, double xa, double ya, double xb, double yb){
    double p = (ya - yb) / (xa - xb);
    double q = ya - p * xa;
    double m = (j + p*(2*q + p*j) ) / (p*p + 1);
    double n = (j + p*k - m) / p;
    return new Vector(m, n);
}

Vector sub(Vector v1, Vector v2){
  return new Vector(v1.x - v2.x, v1.y - v2.y);
}

Vector mult(Vector v, double a){
  return new Vector(v.x * a, v.y * a);
}

Vector div(Vector v, double a){
  return new Vector(v.x / a, v.y / a);
}

class Mover{
  Vector location = new Vector();
  Vector velocity = new Vector();
  double mass;
  float r;
  boolean keyAffected = false;
  
  Mover(double mass, float r){
    this.mass = mass;
    this.r = r;
  }
  
  void display(){
    noStroke();
    fill(150);
    ellipse(mx2px(location.x), my2py(location.y), m2p(r * 2), m2p(r * 2));
  }
  
  void update(){
    location.add(mult(velocity, interval));
  }
  
  boolean equals(Mover m){
    return location.equals(m.location);
  }
}

void applyForce(Mover mover, Vector force){
  mover.velocity.add(div(force, mover.mass));
}

void setup(){
  size(900, 500);
  frameRate(1 / interval);
  center_px = width / 2;
  center_py = height / 2;
  
  //movers.add(new Mover(1, 0.5));
}

void draw(){
  background(255);
  drawAxis();
  
  checkGravity();
  checkContact();
  
  int i = 0;
  for(Mover m : movers){
    i++;
    nextLine("Mover" + i + ":");
    nextLine("  location=(" + m.location.x + "," + m.location.y + ")");
    //nextLine("  velocity=(" + m.velocity.x + "," + m.velocity.y + ")");
    nextLine("  speed=" + m.velocity.mag() + "m/s");
    m.update();
    m.display();
  }
  currentLine = 0;
}

int currentLine = 0;
void nextLine(String str){
  textSize(14);
  stroke(0);
  text(str, 30, 15 + ++currentLine *15);
}

int mx2px(double mx){
  return (int)Math.round(center_px + mx * ratio);
}

int my2py(double my){
  return (int)Math.round(center_py + -my * ratio);
}

double px2mx(int px){
  return (px - center_px) / ratio;
}

double py2my(int py){
  return -(py - center_py) / ratio;
}

int m2p(double meters){
  return (int)Math.round(meters * ratio);
}

double p2m(int pixels){
  return pixels / ratio;
}

double distanceOf(Mover m1, Mover m2){
  double x = m1.location.x - m2.location.x;
  double y = m1.location.y - m2.location.y;
  return Math.sqrt(x*x + y*y);
}

Vector middlePointOf(Mover m1, Mover m2){
  double min_x = Math.min(m1.location.x, m2.location.x);
  double min_y = Math.min(m1.location.y, m2.location.y);
  double half_x_dist = Math.abs(m1.location.x - m2.location.x) / 2;
  double half_y_dist = Math.abs(m1.location.y - m2.location.y) / 2;
  return new Vector(min_x + half_x_dist, min_y + half_y_dist);
}

void getApart(Mover m1, Mover m2, double distance){
  Vector a = new Vector(m2.location, m1.location).normalize().mult(distance / 2);
  m1.location.add(a);
  a.reserve();
  m2.location.add(a);
}

void checkContact(){
  int movers_num;
  if((movers_num = movers.size()) >= 2)
  for(int i=0; i<movers_num; i++){
    for(int n=i+1; n<movers_num; n++){
      Mover m1 = movers.get(i), m2 = movers.get(n);
      double h = m1.r + m2.r;
      if(distanceOf(m1, m2) <= h && h != 0){
        double x = Math.abs(m1.location.x - m2.location.x);
        println("x=" + x);
        double y = Math.abs(m1.location.y - m2.location.y);
        println("y=" + y);
        double ratio_r1_h = m1.r / h;
        println("ratio_r1_h=" + ratio_r1_h);
        double min_x = Math.min(m1.location.x, m2.location.x);
        println("min_x=" + min_x);
        double min_y = Math.min(m1.location.y, m2.location.y);
        println("min_y=" + min_y);
        handleContact(m1, m2, new Vector(min_x + x * ratio_r1_h, min_y + y * ratio_r1_h));
      }
    }
  }
}

void handleContact(Mover m1, Mover m2, Vector contactPoint){
  Mover faster, slowlier;
  if(m1.velocity.mag() > m2.velocity.mag()){
    faster = m1;
    slowlier = m2;
  }else{
    faster = m2;
    slowlier = m1;
  }
  Vector passed = div(mult(faster.velocity, faster.mass), slowlier.mass);
  double size = passed.mag();
  slowlier.velocity.add(passed);
  faster.velocity.reflect(contactPoint,faster.location).sub(passed.normalize().mult(size));
}

void checkGravity(){
  int movers_num;
  if((movers_num = movers.size()) >= 2)
  for(int i=0; i<movers_num; i++){
    for(int n=i+1; n<movers_num; n++){
      Mover m1 = movers.get(i), m2 = movers.get(n);
      applyForce(m1, mult(gravity(m2, m1), interval));
      applyForce(m2, mult(gravity(m1, m2), interval));
    }
  }
}

Vector gravity(Mover attracker, Mover attracked){
  Vector direction = new Vector(attracked.location, attracker.location).normalize();
  double distance = distanceOf(attracker, attracked);
  double size = G * attracker.mass * attracked.mass / (distance * distance);
  return mult(direction, size);
}

int tempCount = 0;
void mouseClicked(){
  Mover m = new Mover(1, 0.18);
  if(tempCount++ == 0){
    m.keyAffected = true;
    //m.r = 0.4;
    //m.mass = 8e9;
  }
  m.location.x = px2mx(mouseX);
  m.location.y = py2my(mouseY);
  movers.add(m);
}

void keyPressed(){
  for(Mover m : movers){
    if(m.keyAffected){
      switch(key){
        case 'a':
        applyForce(m, new Vector(-0.1, 0).mult(m.mass));
        break;
        case 'd':
        applyForce(m, new Vector(0.1, 0).mult(m.mass));
        break;
        case 'w':
        applyForce(m, new Vector(0, 0.1).mult(m.mass));
        break;
        case 's':
        applyForce(m, new Vector(0, -0.1).mult(m.mass));
        break;
      }
    }
  }
}
void keyReleased(){
  for(Mover m : movers){
    if(m.keyAffected){
      m.velocity.div(10);
    }
  }
}

void drawAxis(){
  stroke(175);
  line(0, center_py, width, center_py);
  line(center_px, 0, center_px, height);
  int interval = m2p(0.1);
  int x_mod = center_px % interval;
  int y_mod = center_py % interval;
  
  for(int i = x_mod; i<width; i+=interval){
    long d = Math.round(px2mx(i) * 10);
    int n;
    if(d % 10 == 0){
      n = 10;
    }else if(d % 5 == 0){
      n = 7;
    }else{
      n = 3;
    }
    line(i, center_py - n, i, center_py + n);
  }
  for(int i = y_mod; i<height; i+=interval){
    long d = Math.round(py2my(i) * 10);
    int n;
    if(d % 10 == 0){
      n = 10;
    }else if(d % 5 == 0){
      n = 7;
    }else{
      n = 3;
    }
    line(center_px - n, i, center_px + n, i);
  }
}