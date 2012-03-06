package com.jreitter.philipp.udacity.simulator;

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.RenderingHints;
import java.io.File;
import java.util.Properties;

import javax.imageio.ImageIO;

import com.jreitter.philipp.controller.Element;
import com.jreitter.philipp.controller.Link;
import com.jreitter.philipp.controller.PT1;
import com.jreitter.philipp.udacity.simulator.abstracts.Car;
import com.jreitter.philipp.udacity.simulator.abstracts.CarController;
import com.jreitter.philipp.udacity.simulator.abstracts.Configurable;
import com.jreitter.philipp.util.Random;

public class DefaultCar implements Car, Configurable
{
	private Image carImage;
	
	/**
	 * CarController class is used for data encapsulation.
	 * While user gets noisy values from the controller, 
	 * the simulation can get real values from Car class.
	 * As long as we don't give the CarController to user we are fine.
	 */
	public class DefaultCarController implements CarController
	//give me friend classes java, so i can put this in another file...!
	{
		private DefaultCarController()
		{
		}
		
		public float getSpeed(){return retSpeed;}
		public float getSteer(){return retSteer;}
		public float getGyro(){return retGyro;}
		
		public void setSpeed(float s)
		{
			if(s>1.f)s=1.f;
			else if(s<-1.f)s=-1.f;
		
			speed.input(s * maxSpeed);
		}

		public void setSteer(float s)
		{
			if(s>1.f)s=1.f;
			else if(s<-1.f)s=-1.f;
		
			steer.input(s * maxSteer);
		}
	}
	
	//Configuration Variables
	private float steerSensorError = 0.f;
	private float speedSensorError = 0.f;
	private float gyroSensorError = 0.f;
	
	private float steerError = 0.f;
	private float speedError = 0.f;
	
	private float maxSpeed = 0.f;
	private float maxSteer = 0.f;
	
	//Other suff
	private Random r;
	private CarController controller;

	//Car State variables
	private float x;
	private float y;
	private float startX;
	private float startY;
	private float angle;
	
	private Element speed;
	private Element steer;
	
	//Randomized Values 
	private float retSteer;
	private float retSpeed;
	private float retGyro;
	
	//Constructor
	public DefaultCar( )
	{
		controller = new DefaultCarController();
		r = new Random( );
		
		x = 200.0f;
		y = 200.0f;
		angle = 0.f;	
		try
		{
			if( getClass().getResource("/img/car.png") == null )
				carImage = ImageIO.read(new File("img/car.png")); //really fast hotfix
			else
				carImage = ImageIO.read(getClass().getResource("/img/car.png"));
		}catch(Exception e)
		{
			e.printStackTrace();
			System.err.println("Couldn't load img/car.png");
		}
	}
	
	//Getter&Setter
	public float getX(){return x;}
	public float getY(){return y;}
	public float getAngle(){return angle;}
	public float getSteer(){return steer.value();}
	public float getSpeed(){return speed.value();}
	public CarController getController(){return controller;};
	
	//Update Method
	public void update(float dt)
	{
		steer.update(dt);
		speed.update(dt);

		float rndSteer = (float)r.nextGaussian(steer.value(), steerError);
		float rndSpeed = (float)r.nextGaussian(speed.value(), speedError);
		retSteer = (float)r.nextGaussian(rndSteer, steerSensorError);
		retSpeed = (float)r.nextGaussian(rndSpeed, speedSensorError);
		
		angle += rndSteer * dt;
		retGyro = (float)r.nextGaussian(rndSteer, gyroSensorError);
		
		x += Math.cos(angle)*rndSpeed*dt;
		y += Math.sin(angle)*rndSpeed*dt;	
	}

	@Override
	public void loadProperties(Properties p) 
	{
		steerSensorError = Float.parseFloat(p.getProperty("carSteerSensorError", "0"));
		speedSensorError = Float.parseFloat(p.getProperty("carSpeedSensorError", "0"));
		gyroSensorError  = Float.parseFloat(p.getProperty("carGyroSensorError" , "0"));
		steerError 		 = Float.parseFloat(p.getProperty("carSteerError"	   , "0"));
		speedError 		 = Float.parseFloat(p.getProperty("carSpeedError"	   , "0"));
		maxSpeed 		 = Float.parseFloat(p.getProperty("carMaxSpeed"		   , "0"));
		maxSteer 		 = Float.parseFloat(p.getProperty("carMaxSteer"		   , "0"));	
		startX 			 = Float.parseFloat(p.getProperty("carStartX"		   , "200"));
		startY			 = Float.parseFloat(p.getProperty("carStartY"		   , "200"));	
		
		float T = Float.parseFloat(p.getProperty("carSpeedT", "0"));
		if(T > 0.f) speed = new PT1(T);
		else speed = new Link();
		
		T = Float.parseFloat(p.getProperty("carSteerT", "0"));
		if(T > 0.f) steer = new PT1(T);
		else steer = new Link();
	}

	@Override
	public void onPaint(Graphics2D g) 
	{
	    Graphics2D gg = (Graphics2D) g.create();
	    gg.setColor(Color.BLUE);
	    gg.rotate(angle+Math.PI/2, x, y);
	    gg.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
	    gg.drawImage(carImage, (int)(x-22.5), (int)(y-50), null);
	    gg.dispose();
	}

	@Override
	public void init() 
	{
		x = startX;
		y = startY;
		angle = 0.f;
		speed.input(0); 
		speed.value(0);
		steer.input(0); 
		steer.value(0);
	}
	
}
