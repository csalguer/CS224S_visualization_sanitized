import processing.pdf.*;

import ddf.minim.*;
Minim minim; 
AudioSample kick;

ArrayList<Starlet> starlets = new ArrayList<Starlet>();
int offset = 10;
int count = 1;
int rate = 1;
Starlet current_starlet = null;
float lover_one_new_x = 0;
float lover_one_new_y = 0;
float lover_one_previous_x = 0;
float lover_one_previous_y = height/2;
float lover_two_new_x = 0;
float lover_two_new_y = 0;
float lover_two_previous_x = width;
float lover_two_previous_y = height/2;
float lover_difference_x = 0;
float lover_difference_y = 0;
float y_progress = 0;
float x_progress = 0;
int lover_one_up = 1;
int lover_one_right = 1;
int lover_two_up = 1;
int lover_two_right = 1;
boolean lover_one_speaking = true;
int pulse = 120;
int heart_size = 0;
boolean flag = true;
float diameter = 300;
float current_radians = 0;
float chance = 0;
int willingness_one = 1;
int willingness_two = 1;
float colorCount = 0;
int a = 0, r = 100;
float nC = 36;
boolean addMode = false;
float random_one_x = 0;
float random_one_y = 0;
float random_two_x = 0;
float random_two_y = 0;
float random = 0;
float cohesion = -1.1;
float cohesion_step = 0.002352941176;
float x_ellipse = 0;
float y_ellipse = 0;
boolean center_on = false;
int fader_count = 0;
int counter_fader_past = 0;
float diff_one_x = 0;
float diff_one_y = 0;
float diff_two_x = 0;
float diff_two_y = 0;
String switch_label = "s,w,i,t,c,h";
int[] prosody_values;
int[] emotion_values;
int prosody_count = 0;
int emotion_count = 0;
int debug_count = 0;
 
//boolean recording;
//PGraphicsPDF pdf;
 

/*
 * The maximum number of particles to display at once.  Lowering this will
 * improve performance on slow systems.
 */
int PARTICLE_COUNT = 256;

/*
 * The number of events that must occur before a spark is emitted.  Increasing
 * this will improve video and sound performance as well as change the
 * aesthetics.
 */
int EMISSION_PERIOD = 0;

/*
 * The lowest ratio of vertical speed retained after a spark bounces.
 */
float LOW_BOUNCE = 0.5;

/*
 * The highest ratio of vertical speed retained after a spark bounces.
 */
float HIGH_BOUNCE = 0.8;

/*
 * The variation in velocity of newly-created sparks.
 */
float SPRAY_SPREAD = 2.0;

/*
 * Some predefined gravity settings to play with.
 */
float EARTH_GRAVITY = 1.0 / 16.0;
float MOON_GRAVITY = EARTH_GRAVITY / 6.0;
float JUPITER_GRAVITY = EARTH_GRAVITY * 2.5;

/*
 * The amount of acceleration due to gravity.
 */
float GRAVITY = EARTH_GRAVITY;

/*
 * The amount of error allowed in model coordinate measurements.  Lowering
 * this will let sparks have tiny bounces longer.
 */
float TOLERANCE = 0.3;

/**
 * The focal length from the viewer to the screen in model coordinates.
 */
float FOCAL_LENGTH = 1000.0;

/**
 * The distance in model coordinates from the viewer to where new sparks are
 * created.  Increasing this number will move the created sparks further away.
 */
float INTERACTION_DISTANCE = 4 * FOCAL_LENGTH;

/*
 * A custom 3D canvas used to draw the world.
 */
Canvas3D canvas;

/*
 * A collection of Particles that represent the spraying sparks.
 */
Particle sparks[] = new Particle[PARTICLE_COUNT];

/*
 * The index of the Particle to use for the next spark created.
 */
int nextSpark = 0;

/*
 * The number of drag events that have passed without emitting a spark.
 */
int skipCount = 0;

void create_sparks(float x, float y) {
  if (skipCount >= EMISSION_PERIOD) {
    /*
     * Reset the skip count.
     */
    skipCount = 0;

    /*
     * Convert the prior and current mouse screen coordinates to model coordinates.
     */
    Point3D prior = canvas.toModelCoordinates(x+random(-40,40), y+random(-40,40));
    Point3D current = canvas.toModelCoordinates(x, y);

    /*
     * The spark's initial velocity is the difference between the current and prior
     * points, randomized a bit to create a "spray" effect and scaled by the elapsed
     * time.
     */
    Vector3D velocity = current.diff(prior);
    velocity.shift(new Vector3D(random(-SPRAY_SPREAD, SPRAY_SPREAD), 0, random(-SPRAY_SPREAD, SPRAY_SPREAD) * velocity.x));
    velocity.scale(1.0 / averageElapsedMillis);

    /*
     * Set the spark's intital motion and queue up the next particle.
     */
    sparks[nextSpark].initializeMotion(current, velocity);
    nextSpark = (nextSpark + 1) % PARTICLE_COUNT;
  } 
  else {
    /*
     * Increase the skip count.
     */
    skipCount++;
  }
}

long lastFrameDrawn = millis();

float averageElapsedMillis = 20.0;
 
 
/*void keyPressed() {
  if (key == 'r') {
    beginRecord(pdf);
      println("Recording started.");
      recording = true;
      
    
  } else if (key == 'q') {
    endRecord();
      println("Recording stopped.");
      recording = false;
    exit();
  }  
}*/

void settings() {
  //width = 2560;
  //height = 1500;
  fullScreen(P3D);
}

void setup() {
  //pdf = (PGraphicsPDF) createGraphics(width, height, PDF, "pause-resume.pdf");
  frameRate(60);
  //println(frameCount);
  lover_one_previous_x = 0;
  lover_one_previous_y = height/2;
  lover_two_previous_x = width;
  lover_two_previous_y = height/2;
  strokeWeight(2);
  for(int i = offset; i < width - offset; i += 25) {
    for(int j = offset; j < height - offset; j += 25) {
      Starlet starlet = new Starlet(new PVector(i+random(-5,5), j+random(-5,5)));
      starlets.add(starlet);
    }
  }
  
  canvas = new Canvas3D(FOCAL_LENGTH, INTERACTION_DISTANCE);
  for (int i = 0; i < PARTICLE_COUNT; i++) {
    sparks[i] = new Particle(255, 255, 255);
  }
  
  String[] lines = loadStrings("demo6_prosody_prediction.txt");
  prosody_values = new int[lines.length];
  for (int i = 0 ; i < lines.length; i++) {
    if (lines[i].equals(switch_label) == false) {
      prosody_values[i] = Integer.parseInt(lines[i]);
    } else {
      prosody_values[i] = -1;
    }
  }
  
  lines = loadStrings("demo6_emotion_prediction.txt");
  emotion_values = new int[lines.length];
  for (int i = 0 ; i < lines.length; i++) {
    if (lines[i].equals(switch_label) == false) {
      emotion_values[i] = Integer.parseInt(lines[i]);
    } else {
      emotion_values[i] = -1;
    }
  }
  
  //file = new SoundFile(this, audioName);
  //file.play();
  //file.rate(0.25);
  minim = new Minim(this); 
  kick = minim.loadSample("sound6.wav", 512); 
  kick.trigger(); 
}

void draw() {
  //println(frameCount);
  //background(0);
  fill(0,0,0,10);
  noStroke();
  fill(0,0,0,10);
  rect(0,0,width,height);
  if(colorCount <= 190) {
    lover_difference_x = lover_two_previous_x - lover_one_previous_x;
    lover_difference_y = lover_two_previous_y - lover_one_previous_y; 
    if(abs(lover_difference_x) < 30 && abs(lover_difference_y) < 30) {
      create_sparks(lover_one_previous_x + lover_difference_x/2, lover_one_previous_y + lover_difference_y/2); 
      colorCount += 5*0.2;
      if (cohesion < 1) {
        cohesion += 5*cohesion_step;
      }
    }
    strokeWeight(4);
  
    if(lover_difference_y >= 0) {
      lover_one_up = -1;
      lover_two_up = 1;
    } else {
      lover_one_up = 1;
      lover_two_up = -1;
    }
    if(lover_difference_x <= 0) {
      lover_one_right = -1;
      lover_two_right = 1;
    } else {
      lover_one_right = 1;
      lover_two_right = -1;
    }
    
    //WILLINGNESS
    
    if (frameCount % 15 == 0 && colorCount <= 165) {
      //println(debug_count);
      debug_count++;
      if (lover_one_speaking) {
        if (prosody_values[prosody_count] == -1) {
          lover_one_speaking = false;
          //println("switch");
          prosody_count++;
        } else if (prosody_values[prosody_count] == 0) {
          willingness_one = 1;
          prosody_count++;
        } else {
          willingness_one = 1;
          prosody_count++;
        }
      } else {
        if (prosody_values[prosody_count] == -1) {
          lover_one_speaking = true;
          prosody_count++;
          //println("switch");
        } else if (prosody_values[prosody_count] == 0) {
          willingness_two = 1;
          prosody_count++;
        } else {
          willingness_two = 1;
          prosody_count++;
        }
      }
    }
    
    if (frameCount % 150 >= 0 && frameCount % 150 <= random(0,2)) {
      random_one_x = random(-4,4);
      random_one_y = random(-4,4);
      random_two_x = random(-4,4);
      random_two_y = random(-4,4);
    } 
    
    //lover_one_new_x = lover_one_previous_x  + lover_one_right*1*willingness_one;
    //lover_one_new_y = lover_one_previous_y  - 5*cos(frameCount/10)*lover_one_up*1*willingness_one;
    //lover_two_new_x = lover_two_previous_x  + lover_two_right*1*willingness_two;
    //lover_two_new_y = lover_two_previous_y  - 5*sin(frameCount/10)*lover_two_up*1*willingness_two;
    
    lover_one_new_x = lover_one_previous_x  + random_one_x + lover_one_right*2*willingness_one;
    lover_one_new_y = lover_one_previous_y  + random_one_y - 5*cos(frameCount/10)*lover_one_up*rate*willingness_one;
    lover_two_new_x = lover_two_previous_x  + random_two_x + lover_two_right*2*willingness_two;
    lover_two_new_y = lover_two_previous_y  + random_two_y - 5*sin(frameCount/10)*lover_two_up*rate*willingness_two;
    
  } else {
    willingness_one = 1;
    willingness_two = 1;
    diff_one_x = lover_one_previous_x - width/2;
    diff_one_y = lover_one_previous_y - height/2;
    diff_two_x = lover_two_previous_x - width/2;
    diff_two_y = lover_two_previous_y - height/2;

    if(abs(diff_one_x) < 10 && abs(diff_one_y) < 10 && abs(diff_two_x) < 10 && abs(diff_two_y) < 10) {
      fader_count++;
      if(abs(diff_one_x) < 1 && abs(diff_one_y) < 1 && abs(diff_two_x) < 1 && abs(diff_two_y) < 1) {
        center_on = true;
      }
    }
    
    strokeWeight(4);
    
    lover_one_new_x = lover_one_previous_x - diff_one_x/30;
    lover_one_new_y = lover_one_previous_y - diff_one_y/20;
    lover_two_new_x = lover_two_previous_x - diff_two_x/20;
    lover_two_new_y = lover_two_previous_y - diff_two_y/30;
    
  }
  strokeWeight(4);
  
  if(lover_one_new_x <= 0 + 20) {
    lover_one_new_x = 0 + 20; 
    random_one_x = random(-5,5);
  }
  if(lover_one_new_x >= width - 20) {
    lover_one_new_x = width - 20;  
    random_one_x = random(-5,5);
  }
  if(lover_one_new_y <= 0 + 20) {
    lover_one_new_y = 0 + 20;  
    random_one_y = random(-5,5);
  }
  if(lover_one_new_y >= height - 20) {
    lover_one_new_y = height - 20;  
    random_one_y = random(-5,5);
  }
  
  if(lover_two_new_x <= 0 + 20) {
    lover_two_new_x = 0 + 20;  
    random_two_x = random(-5,5);
  }
  if(lover_two_new_x >= width - 20) {
    lover_two_new_x = width - 20;  
    random_two_x = random(-5,5);
  }
  if(lover_two_new_y <= 0 + 20) {
    lover_two_new_y = 0 + 20; 
    random_two_y = random(-5,5);
  }
  if(lover_two_new_y >= height - 20) {
    lover_two_new_y = height - 20; 
    random_two_y = random(-5,5);
  }
  
  lover_one_previous_x = lover_one_new_x;
  lover_one_previous_y = lover_one_new_y;
  lover_two_previous_x = lover_two_new_x;
  lover_two_previous_y = lover_two_new_y;
  //stroke(235, 20);  
  //line(lover_one_previous_x, lover_one_previous_y, lover_one_new_x, lover_one_new_y);
 
  /*
  arc(a, b, c, d, start, stop)
  Parameters  
  a  float: x-coordinate of the arc's ellipse
  b  float: y-coordinate of the arc's ellipse
  c  float: width of the arc's ellipse by default
  d  float: height of the arc's ellipse by default
  start  float: angle to start the arc, specified in radians
  stop  float: angle to stop the arc, specified in radians
  */

  //line(lover_one_previous_x, lover_one_previous_y, lover_one_new_x, lover_one_new_y);
  //curve(lover_one_previous_x, lover_one_previous_y, lover_one_previous_x + random(-200,200), lover_one_previous_y + random(-200,200), lover_one_previous_x + random(-200,200), lover_one_previous_y + random(-200,200), lover_one_new_x, lover_one_new_y);
  if (frameCount % pulse > 0 && frameCount % pulse < 8) {
    heart_size = pulse/2;
  }
  smooth();
  noStroke();
  //fill(139,0,0, 255);
  //beginShape();
  //vertex(width/2, height/2 + 50 + heart_size/2); 
  //bezierVertex(width/2 + 10 + heart_size, height - height/2 + 10 - heart_size/2, width/2 + 100 + heart_size/2, height/2 - 50 - heart_size/2, width/2, height/2 - heart_size/4); 
  //vertex(width/2, height/2 + 50 + heart_size/2); 
  //bezierVertex(width/2 - 10 - heart_size, height - height/2 + 10 - heart_size/2, width/2 - 100 - heart_size/2, height/2 - 50 - heart_size/2, width/2, height/2 - heart_size/4); 
  //endShape();
  //heart_size = 0;
  strokeWeight(2);
  for(int i = 0; i < starlets.size(); i++) {
    current_starlet = starlets.get(i);
    if (((current_starlet.location.x > lover_one_new_x - 10 && current_starlet.location.x < lover_one_new_x + 10) 
    && (current_starlet.location.y > lover_one_new_y - 10 && current_starlet.location.y < lover_one_new_y + 10))
    || ((current_starlet.location.x > lover_two_new_x - 10 && current_starlet.location.x < lover_two_new_x + 10) 
    && (current_starlet.location.y > lover_two_new_y - 10 && current_starlet.location.y < lover_two_new_y + 10))) {
      current_starlet.displace("x");
      current_starlet.displace("y");
    }
    current_starlet.jitter();
    stroke(255- colorCount*random(1,1.5),random(255)- colorCount*random(1,1.5), random(20)- colorCount*random(1,1.5), random(20));
    fill(255 - colorCount*random(1,1.5),20- colorCount*random(1,1.5),147- colorCount*random(1,1.5), 20);
    if (diameter < 0) {
      diameter = random(60);
    }
    diameter -= 5;
    current_radians = 2*PI;
    arc(current_starlet.location.x, current_starlet.location.y, diameter, diameter, 0, current_radians);
  }
  //fill(250,10,10, 200);
  //chance = random(0,10);
  //if(chance > 8) {
  //  stroke(255,20,20, 100);
  //}
  count++;
  
  /*
   * Determine how long it has been since we last drew a frame.
   */
  long now = millis();
  long elapsedMillis = now - lastFrameDrawn;
  lastFrameDrawn = now;
  averageElapsedMillis = .90 * averageElapsedMillis + .10 * elapsedMillis; 

  /*
   * Fade the screen's current contents a bit more toward black.
   */
  noStroke();    
  //fill(0, 0, 0, constrain(2 * elapsedMillis, 0, 255));
  //rect(0, 0, width, height);

  /*
   * Draw any active sparks and evolve them one time step.
   */
  for (Particle spark : sparks) {
    if (spark.isActive()) {
      spark.paint(elapsedMillis);
      spark.evolve(elapsedMillis);
    }
  }
  
  
  noStroke();
  //fill(max(255 - colorCount*random(1,1.5), 220), max(255 - colorCount*random(1,1.5), 20), max(255 - colorCount*random(1,1.5), 60), 200);
  //ellipse(lover_one_new_x, lover_one_new_y, 30, 30);
  for (int i = 1; i <= nC; i++)
  {
    //fill(255,200+sin(radians(a+(360/nC)*i))*55,200+cos(a+(360/nC)*i)*55);
    fill(255,200-fader_count);
    ellipse(lover_one_new_x+sin(radians(a+(360/nC)*i))*20,lover_one_new_y+cos(radians(a+(360/nC)*i))*20,3,3);
  }
  
  for (int i = 1; i <= nC; i++)
  {
    //fill(255,200+sin(radians(a+(360/nC)*i))*55,200+cos(a+(360/nC)*i)*55);
    ellipse(lover_two_new_x+sin(radians(a+(360/nC)*i))*20,lover_two_new_y+cos(radians(a+(360/nC)*i))*20,3,3);
  }
  
  a++;
  
  if (nC > 2 && !mousePressed && addMode)
  {
    nC -= .1;
  }
  
  for (int j = 1; j <= nC; j += 20)
  {
    if (center_on == true) {
      fill(255,counter_fader_past);
      counter_fader_past++;
    } else {
      fill(255,0);
    }
    x_ellipse = width/2 + sin(radians(a+(360/nC)*j))*100;
    y_ellipse = height/2 + cos(radians(a+(360/nC)*j))*100;
    for (int i = 1; i <= nC; i++)
    {
      ellipse(x_ellipse+sin(radians(a+(360/nC)*i))*20,y_ellipse+cos(radians(a+(360/nC)*i))*20,4,4);
    }
    
    //for (int i = 1; i <= nC; i++)
    //{
     // ellipse(width/2+sin(radians(a+(360/nC)*i))*20+sin(radians(a+(360/nC)*j))*50,height/2+cos(radians(a+(360/nC)*j))*20+cos(radians(a+(360/nC)*j))*50,4,4);
    //}
  }
    
  if (nC > 2 && !mousePressed && addMode)
  {
    nC -= .1;
  }
  
  //fill(65,105,225, 200);
  //if(chance > 8) {
  //  stroke(20,20,255, 100);
  //}
  //fill(max(255 - colorCount*random(1,1.5), 220), max(255 - colorCount*random(1,1.5), 20), max(255 - colorCount*random(1,1.5), 60), 200);
  //ellipse(lover_two_new_x, lover_two_new_y, 30, 30);
  translate(width/2, height/2);
  for(int x = -110; x <= 110; x+=10){
    for(int y = -110; y <= 110; y+=10){
      float d = dist(x, y, 0, 0);
      float d2 = sin(radians(d))*d;
      //fill(255- colorCount*random(1,1.5), 230- colorCount*random(1,1.5), 230- colorCount*random(1,1.5));
      if (colorCount == 255) { 
        fill(random(255), random(255), random(255), random(255));
      } else {
        fill(255,255,255);
      }
      pushMatrix();
      translate(x, y);
      rotate(radians(d + frameCount));
      if(random(1,100) <= 3) {
        ellipse(x, y, 5, 5);
      }
      ellipse(x, cohesion * y, 3, 3);
      popMatrix();
    } 
  }
}

void fade(int trans)
{
  noStroke();
  fill(100,trans);
  rect(0,0,width,height);
}

class Starlet {
  PVector location;

  Starlet(PVector location) {
    this.location = location;
  }

  void jitter() {
    //stroke(0, 150, 255, map(life, 0, maxLife, 1, 255));
    stroke(212- colorCount*random(1,1.5),175- colorCount*random(1,1.5),55- colorCount*random(1,1.5));
    point(location.x + random(-2, 2), location.y + random(-2, 2));
  }
  
  void displace(String coordinate) {
    //if (coordinate == "x") {
      location.x += random(100,-100);
    //} else {
      location.y += random(100,-100);
    //}
  }
}

/*******************************************************************************
 * SparkChime: Drag the mouse to release a colorful spray of sparks that produce
 * musical tones as they bounce.
 *
 * Sound is not enabled in this version.
 *
 * @author Gregory Bush
 */

/******************************************************************************
 * A rudimentary 3D graphics library.
 *
 * I realized recently that Processing already has 3D graphics capabilities,
 * so much of this could be done natively.  However, this way does load quite
 * quickly comparatively.
 *
 * @author Gregory Bush
 */

/**
 * A point in 2D screen coordinates.
 *
 * @author Gregory Bush
 */
public static class Point2D {
  public final float x;
  public final float y;

  public Point2D(float x, float y) {
    this.x = x;
    this.y = y;
  }
}

/**
 * A vector in 3D model coordinates.
 *
 * @author Gregory Bush
 */
public static class Vector3D {
  public float x;
  public float y;
  public float z;

  public Vector3D(float x, float y, float z) {
    this.x = x;
    this.y = y;
    this.z = z;
  }

  public void shift(Vector3D v) {
    x += v.x;
    y += v.y;
    z += v.z;
  }

  public Vector3D add(Vector3D v) {
    return new Vector3D(x + v.x, y + v.y, z + v.z);
  }

  public void scale(float c) {
    x *= c;
    y *= c;
    z *= c;
  }

  public Vector3D mul(float c) {
    return new Vector3D(c * x, c * y, c * z);
  }
}

/**
 * A point in 3D model coordinates.
 *
 * @author Gregory Bush
 */
public static class Point3D {
  public float x;
  public float y;
  public float z;

  public Point3D(float x, float y, float z) {
    this.x = x;
    this.y = y;
    this.z = z;
  }

  public void shift(Vector3D v) {
    x += v.x;
    y += v.y;
    z += v.z;
  }

  public Point3D add(Vector3D v) {
    return new Point3D(x + v.x, y + v.y, z + v.z);
  }

  public Vector3D diff(Point3D p) {
    return new Vector3D(x - p.x, y - p.y, z - p.z);
  }
}

/**
 * A Canvas3D allows drawing graphics primitives in a 3D coordinate system.
 *
 * @author Gregory Bush
 */
public class Canvas3D {
  private final float focalLength;

  private final float interactionPlane;

  public Canvas3D(float focalLength, float interactionPlane) {
    this.focalLength = focalLength;
    this.interactionPlane = interactionPlane * 0.5;
  }

  /**
   * Convert a point in the 3D model to a point on the 2D screen.
   */
  public Point2D toScreenCoordinates(Point3D p) {
    float scale = focalLength / p.z;

    return new Point2D(p.x * scale + width / 2, p.y * scale + height / 2);
  }

  /**
   * Convert a point on the 2D screen to a point in the 3D model, projected on
   * the interaction plane.
   */
  public Point3D toModelCoordinates(float x, float y) {
    float scale = interactionPlane / focalLength;

    return new Point3D((x - width / 2) * scale, (y - height / 2) * scale, interactionPlane);
  }

  /**
   * Scale the diameter of a sphere whose center is at a particular Z distance to
   * its diameter on the screen.
   */
  public float scaleToScreen(float diameter, float distance) {
    return diameter * focalLength / distance;
  }

  private void drawLine(Point2D from, Point2D to) {
    line(from.x, from.y, to.x, to.y);
  }

  private void drawPoint(Point2D p) {
    point(p.x, p.y);
  }

  /**
   * Draw a line between 3D points.
   */
  public void drawLine(Point3D from, Point3D to, float weight) {
    strokeWeight(scaleToScreen(weight, to.z)/4);
    drawLine(toScreenCoordinates(from), toScreenCoordinates(to));
  }

  /**
   * Draw a point in 3D.
   */
  public void drawPoint(Point3D p, float weight) {
    strokeWeight(scaleToScreen(weight, p.z)/4);
    drawPoint(toScreenCoordinates(p));
  }

  /**
   * Draw a circle with vertical normal vector.
   */
  public void drawHorizontalCircle(Point3D center, float radius) {
    float screenRadius = canvas.scaleToScreen(radius, center.z);
    Point2D p = toScreenCoordinates(center);
    /*
     * This is a cheat, but it looks fine and is faster than
     * doing it right.
     */
    ellipse(p.x, p.y, screenRadius, screenRadius * .3);
  }
}

/**
 * Increase the intensity of a color value.
 */
float amplify(float n) {
  return constrain(4 * n, 0, 255);
}

/******************************************************************************
 * A Particle is a representation of a bouncing, colored spark that plays a
 * sound when it strikes the ground.
 *
 * @author Gregory Bush
 */
public class Particle {
  /*
   * The coordinates of the particle's current location.
   */
  private Point3D location;

  /*
   * The particle's velocity.
   */
  private Vector3D velocity;

  /*
   * The particle's color.
   */
  private float red;
  private float green;
  private float blue;

  /*
   * The sound that will be played when the particle strikes the ground.
   */

  /*
   * Was the particle drawn off the left of the screen?
   */
  private boolean pastLeftWall;

  /*
   * Was the particle drawn off the right of the screen?
   */
  private boolean pastRightWall;

  /**
   * Create a Particle with a specified color and characteristic sound.
   */
  public Particle(float red, float green, float blue) {
    this.red = red;
    this.green = green;
    this.blue = blue;
  }

  /**
   * Initialize or reset all variables describing the motion of the particle to
   * the specified values.
   */
  public void initializeMotion(Point3D location, Vector3D velocity) {
    this.location = location;
    this.velocity = velocity;
  }

  /**
   * Returns true if the Particle should still be actively evolving in time.
   */
  public boolean isActive() {
    /*
     * We will consider the Particle active as long as it is on the other side
     * of the screen than the viewer. 
     */
    return location != null && location.z >= FOCAL_LENGTH;
  }

  /*
   * Draw a motion-blurred trajectory of a particular stroke weight and opacity.
   * The stroke weight will be scaled based on the Particle's distance from the
   * viewer.
   */
  private void drawMotion(Point3D from, Point3D to, float weight, float opacity) {
    stroke(red, green, blue, opacity);
    canvas.drawLine(from, to, weight);
  }

  /**
   * Draw the Particle on the screen.
   */
  public void paint(float elapsedMillis) {
    Point3D from = location;
    Point3D to = location.add(velocity.mul(elapsedMillis));

    /*
     * Draw three motion blurs, successively narrower and brighter.
     */
    drawMotion(from, to, 64, 8);
    drawMotion(from, to, 32, 32);
    drawMotion(from, to, 8, 255);

    /*
     * Draw a splash and play the Particle's characteristic note if it has
     * struck the ground.
     */
    //if (isUnderground(elapsedMillis)) {
    //  splash(to);
    //}

    /*
     * Remember if we drew off of the left or right of the screen.  This is
     * a bit awkward.  Bouncing off geometry in the model coordinates would
     * be better.
     */
    Point2D p = canvas.toScreenCoordinates(to);
    pastLeftWall = p.x < 0;
    pastRightWall = p.x >= width;
  }

  /*
   * Draw the splash when the Particle strikes the ground and play the
   * Particle's characteristic note if sound is enabled.
   */
  private void splash(Point3D to) {
    /*
     * The splash is a circle on the ground with dim illumination in its
     * interior and a bright ring on its circumference.
     */
    stroke(red, green, blue, 128);
    fill(red, green, blue, 64);
    canvas.drawHorizontalCircle(to, 128);

    /*
     * At the point where the Particle touched the ground, draw a small
     * but bright flash of light.
     */
    stroke(amplify(red), amplify(green), amplify(blue), 255);
    canvas.drawPoint(to, 16);

    /*
     * Play the splash sound at a volume relative to how fast the
     * particle collided.
     */
  }

  /*
   * Is the Particle's next position beneath the surface of the ground?
   */
  private boolean isUnderground(float elapsedMillis) {
    return location.y + velocity.y * elapsedMillis > height;
  }

  /*
   * Various functions to determine the direction of the Particle's motion.
   */

  private boolean isMovingLeft() {
    return velocity.x <= -TOLERANCE;
  }

  private boolean isMovingRight() {
    return velocity.x >= TOLERANCE;
  }

  private boolean isMovingUp() {
    return velocity.y <= -TOLERANCE;
  }

  private boolean isMovingDown() {
    return velocity.y >= TOLERANCE;
  }

  private boolean isMovingVertically() {
    return isMovingUp() || isMovingDown();
  }

  /*
   * Reverse the horizontal motion of the Particle.
   */
  private void bounceHorizontal() {
    velocity.x = -velocity.x;
  }

  /*
   * Reverse the vertical motion of the Particle.
   */
  private void bounceVertical() {
    /*
     * The Particle's kinetic energy will be scaled down randomly.  It
     * will lose energy with every bounce.
     */
    velocity.y = -velocity.y * random(LOW_BOUNCE, HIGH_BOUNCE);
  }

  /*
   * Give the particle an inactive status, indicating it no longer needs to be
   * evolved in time.
   */
  private void deactivate() {
    location.z = 0;
  }

  /**
   * Evolve the Particle's motion over the specified amount of time in millis.
   */
  public void evolve(float elapsedMillis) {
    /*
     * Bounce off of the left or right borders of the screen if the Particle
     * has gone off.
     */
    if ((pastLeftWall && isMovingLeft()) || (pastRightWall && isMovingRight())) {
      bounceHorizontal();
    } 

    /*
     * If the Particle has struck the ground, bounce vertically.  Deactivate
     * the particle if it has lost so much energy it is no longer
     * really bouncing.
     */
    //if (isUnderground(elapsedMillis) && isMovingDown()) {
    //  bounceVertical();
    //  if (!isMovingVertically()) {
    //    deactivate();
    //  }
    //} 

    /*
     * Add the Particle's velocity times elapsed time to its current location.
     */
    location.shift(velocity.mul(elapsedMillis));

    /*
     * Apply the accleration due to gravity.
     */
    velocity.y += GRAVITY;
  }
}