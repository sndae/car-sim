package com.jreitter.philipp.udacity.simulator;

import java.awt.Graphics2D;
import java.util.Properties;

import com.jreitter.philipp.udacity.simulator.abstracts.Car;
import com.jreitter.philipp.udacity.simulator.abstracts.SimulationObject;
import com.jreitter.philipp.util.Random;

public class SensorArray implements SimulationObject
{
	//Why not 1 global static object?
	private Random r;
	
	//Configuration
	private float gpsSensorNoise = 0.f;
	private float cameraImageNoise = 0.f;
	private float gpsUpdate = 0.f;
	private float cameraUpdate = 0.f;
	
	private int c;
	
	private Simulation simulation;
	
	public SensorArray(Simulation s)
	{
		r = new Random();
		this.simulation = s;
	}

	@Override
	public void loadProperties(Properties p) 
	{
		gpsSensorNoise 	 = Float.parseFloat(p.getProperty("gpsSensorNoise"  , "0"));
		cameraImageNoise = Float.parseFloat(p.getProperty("cameraImageNoise", "0"));	
		gpsUpdate = Integer.parseInt(p.getProperty("cameraUpdate","10"));
		cameraUpdate = Integer.parseInt(p.getProperty("gpsSensorUpdate","50"));
	}

	public int[][] getCameraImage() 
	{
		Car c = simulation.getCar();
		World w = simulation.getWorld();
				
		int i = w.getColorAtPixel(c.getX(),c.getY());
		if(r.nextFloat()>(1.f-cameraImageNoise)) //cuz [0,1[
		{
			i=(i+1)&1;
		}

		return new int[][]{{i}};
	}
	
	public float[] getGPSPosition() 
	{
		Car c = simulation.getCar();
		float gx = (float)r.nextGaussian(c.getX(), gpsSensorNoise);
		float gy = (float)r.nextGaussian(c.getY(), gpsSensorNoise);
		return new float[]{gx,gy};
	}

	@Override
	public void onPaint(Graphics2D g) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void init() 
	{
		c = 0;
	}

	@Override
	public void update(float dt) 
	{
		c++;
		if(c%gpsUpdate==0) 
		{
			simulation.getListener().onGPS(getGPSPosition());
		}
		
		if(c%cameraUpdate==0) 
		{
			simulation.getListener().onCamera(getCameraImage());
		}
	}

}
