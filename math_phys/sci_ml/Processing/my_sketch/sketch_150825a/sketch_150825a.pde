ArrayList<Walker> wkrs;
float time = 0;

float ratio = 200;  //pixel length / meter length
double G = 6.67e-11;
double m_E = 5.977e24;
double center_r_E = 6371000;
double m_M = 5e9;
float interval = 1/32f;
int maxTrackPointNum = 250;

int center_wid;
int center_hei;
int currentLine = 0;

void setup(){
  //test();
  
  size(900, 550);
  background(255);
  textSize(14);
  mouseX = m2p_coord(0, true);
  mouseY = m2p_coord(0, false);
  
  stroke(0);
  fill(100);
  center_wid = width/2;
  center_hei = height/2;
  
  wkrs = new ArrayList<Walker>();
  Walker gb = new Walker(1, (float)p2m(width), (float)p2m(20));
  gb.track.remove(0);
  gb.x = 0;
  gb.y = -1.37;
  gb.earthAffected = false;
  gb.color_white = 0;
  wkrs.add(gb);  //ground border
  
  Walker w1 = new Walker(1, (float)p2m(width/10));
  w1.track.remove(0);
  w1.x = 1;
  w1.y = 1.5;
  w1.earthAffected = false;
  w1.mouseAffected = true;
  w1.color_white = 25;
  wkrs.add(w1);  //ground border
  
  //wkrs.add(new Walker(1, 0.1));
  ArrayList<Point> ps = new ArrayList<Point>();
  ps.add(new Point(0,1));
  ps.add(new Point(1,1));
  ps.add(new Point(1,-1));
  ps.add(new Point(0,-1));
  Walker w2 = new Walker(2, ps);
  w2.ratio = 0.1;
  w2.earthAffected = false;
  w2.mouseAffected = true;
  wkrs.add(w2);
  
  frameRate(1/interval);
}

void draw(){
  currentLine = 0;
  background(255);
  
  apply();
  
  for(Walker w : wkrs){
    for(int i=1; i<w.track.size(); i++){
      line(m2p_coord(w.track.get(i-1).x, true)
      , m2p_coord(w.track.get(i-1).y, false)
      , m2p_coord(w.track.get(i).x, true)
      , m2p_coord(w.track.get(i).y, false));
    }
    w.display();
  }
}

void apply(){
  time += interval;
  
  checkContact();
  
  int n = 0;
  for(Walker w : wkrs){
    nextText("");
    nextText("Walker" + ++n + ":");
    nextText("  m=" + w.mass + "kg");
    nextText("  X="+w.x+"m");
    nextText("  Y="+w.y+"m");
    nextText("  v="+w.speed.mag()+"m/s");
    
    if(w.earthAffected){
      PVector g;
      w.applyForce(w.mass, g = gravityAcceleration(m_E, 0, -center_r_E, w.x, w.y));
      nextText("  g=" + g.mag() + "m/s^2");
    }
    if(w.mouseAffected){
      PVector mouse;
      w.applyForce(w.mass, mouse = gravityAcceleration(m_M, p2m_coord(mouseX, true), p2m_coord(mouseY, false), w.x, w.y));
      nextText("  mouse=" + mouse.mag() + "m/s^2");
    }
      
    w.update();
  }
}

void nextText(String text){
  text(text, 30, 30 + ++currentLine*15);
}

double p2m(int pixelLength){
  return pixelLength / ratio;
}

int m2p(double meterLength){
  return (int)(meterLength * ratio + 0.5) ;
}

double p2m_coord(int pixel_coord, boolean isX){
  if(isX)
  return p2m(pixel_coord - center_wid);
  else
  return -p2m(pixel_coord - center_hei);
}

int m2p_coord(double meter_coord, boolean isX){
  if(isX)
  return center_wid + m2p(meter_coord);
  else
  return center_hei - m2p(meter_coord);
}

PVector gravityAcceleration(double attrackerMass, double attrackerX, double attrackerY, double x, double y){
  double distance = sqrt((float)( (attrackerX - x) * (attrackerX - x) + (attrackerY - y) * (attrackerY - y) )) ;
  double modd =  G * attrackerMass / (distance*distance) ;
  return new PVector( (float)( modd/distance * (attrackerX - x)  ), (float)( modd/distance * (attrackerY - y) ));
}

class Point{
  double x;
  double y;
  
  Point(double x, double y){
    this.x = x;
    this.y = y;
  }
  
  float distanceTo(Point p){
    return (float) sqrt((float)( (this.x - p.x) * (this.x - p.x) + (this.y - p.y) * (this.y - p.y) ));
  }
}
enum Shape{
  circle, ellipse, rectangular, polygon
}

class Walker{
  double x = 0;
  double y = 0;
  float angle = 0;
  
  float ratio = 1;
  Shape shape;
  float rotate;
  float wid;
  float hei;
  ArrayList<Point> points;
  int color_white = 100;
  int currentBounceFrame = 0;
  
  float mass;
  PVector speed;
  float aSpeed = 0;
  float elastic_coefficient = 1;
  boolean earthAffected = true;
  boolean mouseAffected = false;
  ArrayList<Point> track;
  
  Walker(float mass, float r){
    shape = Shape.circle;
    hei = wid = r;
    points = new ArrayList<Point>();
    this.mass = mass;
    speed = new PVector();
    track = new ArrayList<Point>();
    track.add(new Point(x, y));
  }
  
  Walker(float mass, float wid, float hei){
    shape = Shape.rectangular;
    this.wid = wid;
    this.hei = hei;
    points = new ArrayList<Point>();
    points.add(new Point(-wid/2, hei/2));
    points.add(new Point(wid/2, hei/2));
    points.add(new Point(-wid/2, -hei/2));
    points.add(new Point(wid/2, -hei/2));
    this.mass = mass;
    speed = new PVector();
    track = new ArrayList<Point>();
    track.add(new Point(x, y));
  }
  
  Walker(float mass, ArrayList<Point> points){
    shape = Shape.polygon;
    this.points = points;
    this.mass = mass;
    speed = new PVector();
    track = new ArrayList<Point>();
    track.add(new Point(x, y));
  }
  
  Point outerLocation(Point point){
    println(point.x + x);
    return new Point(point.x + x, point.y + y);
  }
  
  void display(){
    noStroke();
    fill(color_white);
    if(shape == Shape.circle || shape == Shape.ellipse){
      ellipse(m2p_coord(x, true), m2p_coord(y, false), m2p(wid * ratio), m2p(hei * ratio));
    }else if(shape == Shape.rectangular){
      rect(m2p_coord(x, true)-m2p(wid/2), m2p_coord(y, false)-m2p(hei/2), m2p(wid * ratio), m2p(hei * ratio));
    }else if(shape == Shape.polygon){
      ArrayList<Point> points = new ArrayList();
      int size = this.points.size();
      for(int i=0; i<size; i++){
        points.add(new Point(this.points.get(i).x * ratio + x, this.points.get(i).y * ratio + y));
      }
      int i;
      for(i=2; i<points.size(); i++){
        noStroke();
        triangle(m2p_coord(points.get(0).x, true), m2p_coord(points.get(0).y, false)
        , m2p_coord(points.get(i-1).x, true), m2p_coord(points.get(i-1).y, false)
        , m2p_coord(points.get(i).x, true), m2p_coord(points.get(i).y, false));
        stroke(0);
      }
   }
   stroke(0);
  }
  
  void applyForce(float mass, PVector acceleration){
    speed.add(PVector.mult(PVector.div(PVector.mult(acceleration, mass), this.mass), interval));
  }
  
  void update(){
    x += speed.x * interval;
    y += speed.y * interval;
    
    if(track.size() >= maxTrackPointNum){
      track.remove(0);
    }
    track.add(new Point(x, y));
  }
  
  float distanceTo(double x, double y){
    return (float) sqrt((float)( (this.x - x) * (this.x - x) + (this.y - y) * (this.y - y) ));
  }
  
  /*void bounce(){
    
  }*/
}

void checkContact(){
  for(Walker w1 : wkrs){
    for(Walker w2 : wkrs){
      if(w1 != w2){
        if(w1.shape == Shape.ellipse){
          if(w2.shape == Shape.ellipse){
            if(w1.wid == w1.hei){
              double dist;
              if((dist = w1.distanceTo(w2.x, w2.y)) <= w1.wid + w2.wid){
                //handleContact(w1, w2, new Point(, ));
              }
            }
          }else{
            
          }
        }else{
          if(w2.shape == Shape.ellipse){
            
          }else{
            for(int i=1; i<w1.points.size(); i++){
              for(int n=1; n<w2.points.size(); n++){
                Point p = ifIntersect(w1.outerLocation(w1.points.get(i-1))
                , w1.outerLocation(w1.points.get(i))
                , w2.outerLocation(w2.points.get(n-1))
                , w2.outerLocation(w2.points.get(n)) );
                if(p != null){
                  handleContact(w1, w2, p);
                }
              }
            }
          }
        }
      }
    }
  }
}

void handleContact(Walker w1, Walker w2, Point contactPoint){
  
}

double min(double a, double b){
  return a<b ? a : b;
}

double max(double a, double b){
  return a>b ? a : b;
}

Point ifIntersect(Point startPoint1, Point endPoint1, Point startPoint2, Point endPoint2){
  PVector m = new PVector( (float)(startPoint1.x - endPoint1.x), (float)(startPoint1.y - endPoint1.y) );
  PVector n = new PVector( (float)(startPoint2.x - endPoint2.x), (float)(startPoint2.y - endPoint2.y) );
  m.cross(n);
  if(m.mag() > 0){
    double a = (endPoint1.y - startPoint1.y) / (endPoint1.x - startPoint1.x);
    double b = startPoint1.y - startPoint1.x * a;
    double a_ = (endPoint2.y - startPoint2.y) / (endPoint2.x - startPoint2.x);
    double b_ = startPoint2.y - startPoint2.x * a_;
    double x = (b_ - b) / (a_ - a);
    double y = a * x + b;
    line(m2p_coord(startPoint1.x, true), m2p_coord(startPoint1.y, false), m2p_coord(endPoint1.x, true), m2p_coord(endPoint1.y, false));
    text("line1", m2p_coord(startPoint1.x, true), m2p_coord(startPoint1.y, false));
    line(m2p_coord(startPoint2.x, true), m2p_coord(startPoint2.y, false), m2p_coord(endPoint2.x, true), m2p_coord(endPoint2.y, false));
    text("line2", m2p_coord(startPoint2.x, true), m2p_coord(startPoint2.y, false));
    ellipse(m2p_coord(x, true), m2p_coord(y, true), 5, 5);
    if(x >= min(startPoint1.x, endPoint1.x) && x <= max(startPoint1.x, endPoint1.x)){
      if(y >= min(startPoint1.y, endPoint1.y) && y <= max(startPoint1.x, endPoint1.y)){
        if(x >= min(startPoint2.x, endPoint2.x) && x <= max(startPoint2.x, endPoint2.x)){
          if(y >= min(startPoint2.y, endPoint2.y) && y <= max(startPoint2.x, endPoint2.y)){
            
            nextText(x + "  " + y);
            
            return new Point(x, y);
          }
        }
      }
    }
  }
  //println("null");
  return null;
}

void mouseClicked(){
  Walker w = new Walker(random(2), random(0.2));
  w.track.remove(0);
  w.x = p2m_coord(mouseX, true);
  w.y = p2m_coord(mouseY, false);
  w.color_white = 100 + (int) random(120);
  
  wkrs.add(w);
}